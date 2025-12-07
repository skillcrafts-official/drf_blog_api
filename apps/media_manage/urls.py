from django.urls import re_path

from apps.media_manage.views import serve_protected_media


urlpatterns = [
    re_path(
        r'^media/(?P<path>.+)$', serve_protected_media
    )
]
