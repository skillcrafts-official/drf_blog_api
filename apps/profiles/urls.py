from django.urls import path

from apps.profiles.views import UserProfileView
from apps.profiles.viewsets import WorkFormatView, ProfilesView


urlpatterns = [
    path(
        'displays/education-levels/',
        ProfilesView.as_view({'get': 'education_levels'}),
        name='update_user_profile'
    ),
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
