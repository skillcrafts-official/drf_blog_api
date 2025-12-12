from django.urls import path

from apps.profiles.views import UserProfileView
from apps.profiles.viewsets import WorkFormatView


urlpatterns = [
    path(
        '<int:pk>/', UserProfileView.as_view(),
        name='update_user_profile'
    ),
    path(
        '<int:profile>/work_formats/',
        WorkFormatView.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
        name='update_user_work_formats'
    ),
]
