"""
URL configuration for drf_blog_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponseForbidden
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.http import require_GET
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
import os


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/schema/', SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path('', include('apps.accounts.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('posts/', include('apps.posts.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


import os
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import mimetypes


@csrf_exempt
def serve_media_debug_false(request, path):
    """
    View для отдачи медиафайлов при DEBUG=False
    """
    # Полный путь к файлу
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Проверяем существование файла
    if not os.path.exists(file_path):
        return HttpResponse('File not found', status=404)
    
    # Проверяем, что файл находится внутри MEDIA_ROOT (безопасность)
    file_path = os.path.normpath(file_path)
    media_root = os.path.normpath(settings.MEDIA_ROOT)
    
    if not file_path.startswith(media_root):
        return HttpResponse('Access denied', status=403)
    
    # Проверяем, что это файл, а не директория
    if not os.path.isfile(file_path):
        return HttpResponse('Not a file', status=403)
    
    # Определяем Content-Type
    content_type, encoding = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Открываем файл в бинарном режиме
    try:
        file = open(file_path, 'rb')
        response = FileResponse(file, content_type=content_type)
        
        # Если нужно скачивание, а не просмотр
        # response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        
        # Для изображений - inline (просмотр в браузере)
        if content_type.startswith('image/'):
            response['Content-Disposition'] = 'inline'
            
        return response
    except Exception as e:
        return HttpResponse(f'Error reading file: {str(e)}', status=500)


# Добавляем маршрут для media
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve_media_debug_false, name='serve_media'),
]


from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def check_auth(request):
    return Response({
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None,
        'user_id': request.user.id if request.user.is_authenticated else None,
    })


urlpatterns += [
    path('api/check-auth/', check_auth),
]
