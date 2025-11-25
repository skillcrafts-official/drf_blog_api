from django.urls import path

from apps.profiles.views import UserProfileView


urlpatterns = [
    path(
        '<int:pk>/', UserProfileView.as_view(),
        name='user_profile'
    ),
]
