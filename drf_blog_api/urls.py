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
from django.contrib.auth.decorators import login_required
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


import os
from django.http import FileResponse, HttpResponseForbidden, HttpResponseNotFound

def protected_media(request, path):
    """
    path будет содержать всё после /media/
    Пример: /media/wallpapers/user_2/wallpaper.jpg → path = "wallpapers/user_2/wallpaper.jpg"
    """
    print(f"DEBUG: Got request for /media/{path}")  # Увидим в логах контейнера
    
    # 1. Проверяем заголовок Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        print("DEBUG: No Authorization header")
        return HttpResponseForbidden('Token required')
    
    # 2. Проверяем что токен начинается с "Token "
    # (пока не проверяем валидность токена, только формат)
    if not auth_header.startswith('Token '):
        print(f"DEBUG: Invalid Authorization format: {auth_header[:20]}...")
        return HttpResponseForbidden('Invalid token format')
    
    # 3. Формируем физический путь
    # path уже содержит "wallpapers/user_2/wallpaper.jpg"
    file_path = os.path.join('/app/media', path)
    print(f"DEBUG: Looking for file: {file_path}")
    
    # 4. Проверяем существует ли файл
    if not os.path.exists(file_path):
        print(f"DEBUG: File not found: {file_path}")
        return HttpResponseNotFound('File not found')
    
    # 5. Отдаём файл
    print(f"DEBUG: Serving file: {file_path}")
    return FileResponse(open(file_path, 'rb'))

def test_endpoint(request, path):
    """Просто показывает что запрос дошёл"""
    from django.http import JsonResponse
    return JsonResponse({
        'status': 'OK',
        'path': path,
        'method': request.method,
        'headers': dict(request.headers),
    })

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        path('test/<path:path>', test_endpoint),
        re_path(r'^media/(?P<path>.+)$', protected_media),
    ]


from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def check_auth(request):
    return Response({
        'authenticated': request.user.is_authenticated,
        'username': request.user if request.user.is_authenticated else None,
        'user_id': request.user.id if request.user.is_authenticated else None,
    })


urlpatterns += [
    path('api/check-auth/', check_auth),
]
