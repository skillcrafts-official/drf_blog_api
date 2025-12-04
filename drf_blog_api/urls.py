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
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


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


# Медиафайлы через Django (для продакшена)
def protected_serve(request, path):
    # Логика проверки авторизации
    if not request.user.is_authenticated:
        # Проверяем токен из заголовка
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Access denied')

        # Здесь можно добавить проверку токена
        # token = auth_header.split(' ')[1]
        # ... проверка токена ...

    return serve(request, path, document_root=settings.MEDIA_ROOT)


# Добавляем защищенный доступ к медиафайлам
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', protected_serve),
]
