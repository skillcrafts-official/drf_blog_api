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


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import os
from django.http import FileResponse, HttpResponseNotFound

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_media(request, path):
    file_path = os.path.join('/app/media', path)
    
    if not os.path.exists(file_path):
        return HttpResponseNotFound('File not found')
    
    # Определяем content-type по расширению
    import mimetypes
    content_type, encoding = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    
    # Добавляем заголовки для кэширования
    response['Cache-Control'] = 'public, max-age=86400'  # 24 часа
    
    return response

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
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


@api_view(['GET'])
def debug_media(request, path):
    """Просто показывает информацию без проверки"""
    from rest_framework.response import Response
    import os
    
    return Response({
        'view_called': True,
        'path': path,
        'full_path': os.path.join('/app/media', path),
        'exists': os.path.exists(os.path.join('/app/media', path)),
        'user': str(request.user) if hasattr(request, 'user') else 'no user',
        'auth': str(request.auth) if hasattr(request, 'auth') else 'no auth',
        'headers': dict(request.headers),
    })

urlpatterns += [
    re_path(r'^debug-media/(?P<path>.+)$', debug_media),
]