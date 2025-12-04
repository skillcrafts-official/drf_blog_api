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


@require_GET
def protected_serve(request, path):
    # Простая проверка: пользователь должен быть аутентифицирован
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Access denied: Authentication required')

    # Проверка существования файла (опционально, но рекомендуется)
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(full_path):
        from django.http import Http404
        raise Http404("File not found")

    # Обслуживаем файл
    response = serve(request, path, document_root=settings.MEDIA_ROOT)

    # Добавляем CORS заголовки
    origin = request.headers.get('Origin')
    if origin:
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Credentials'] = 'true'

    return response


# Добавляем защищенный доступ к медиафайлам
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', protected_serve),
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
