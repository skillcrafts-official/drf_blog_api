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


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import FileResponse


@api_view(['GET'])
@authentication_classes([JWTAuthentication])  # ← Включаем JWT
@permission_classes([IsAuthenticated])        # ← Требуем аутентификацию
def protected_media_view(request, path):
    """DRF view с JWT аутентификацией для медиафайлов"""
    
    # Полный путь к файлу
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Проверка существования файла
    if not os.path.exists(full_path):
        from rest_framework.exceptions import NotFound
        raise NotFound("File not found")
    
    # Открываем файл
    file = open(full_path, 'rb')
    
    # Определяем Content-Type
    import mimetypes
    content_type, encoding = mimetypes.guess_type(full_path)
    if not content_type:
        content_type = 'application/octet-stream'
    
    # Создаем response
    response = FileResponse(file, content_type=content_type)
    
    # CORS заголовки
    origin = request.headers.get('Origin')
    if origin:
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Credentials'] = 'true'
    
    return response


# Добавляем защищенный доступ к медиафайлам
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', protected_media_view),
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
