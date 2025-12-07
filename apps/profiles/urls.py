from django.urls import path

from apps.profiles.views import UserProfileView, UpdateUserProfileView


urlpatterns = [
    path(
        '<int:pk>/', UserProfileView.as_view(),
        name='get_user_profile'
    ),
    path(
        '<int:pk>/', UpdateUserProfileView.as_view(),
        name='update_user_profile'
    ),
]
