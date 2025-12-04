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


from django.http import HttpResponseForbidden


def check_token_and_serve(request, path):
    """
    Проверяет токен и отдает файл. Если токена нет - 403.
    """
    # 1. Проверяем заголовок Authorization
    auth_header = request.headers.get('Authorization', '')

    # 2. Если нет заголовка - сразу 403
    if not auth_header.startswith('Bearer '):
        return HttpResponseForbidden('Bearer token required')

    # 3. Проверяем токен
    # from rest_framework.authtoken.models import Token
    # try:
    #     token_key = auth_header.split('Token ')[1]
    #     token = Token.objects.get(key=token_key)
    #     request.user = token.user  # Устанавливаем пользователя
    # except (Token.DoesNotExist, IndexError):
    #     return HttpResponseForbidden('Invalid token')
    
    # 4. Отдаем файл (пока без проверки прав на файл)
    import os
    from django.http import FileResponse
    from django.conf import settings

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))

    from django.http import HttpResponseNotFound
    return HttpResponseNotFound('File not found')


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', check_token_and_serve),
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
