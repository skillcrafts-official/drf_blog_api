from django.urls import path

from apps.profiles.views import (
    UserProfileView, UpdateUserProfileView, ProfilesView
)


urlpatterns = [
    path(
        '', ProfilesView.as_view({'get': 'list'}),
        name='get_profile_list'
    ),
    path(
        '<int:pk>/get/', UserProfileView.as_view(),
        name='get_user_profile'
    ),
    path(
        '<int:pk>/update/', UpdateUserProfileView.as_view(),
        name='update_user_profile'
    ),
]
