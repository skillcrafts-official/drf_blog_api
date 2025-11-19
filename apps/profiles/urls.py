from django.urls import path

from apps.profiles.views import UserProfileView, SelfUserProfileView


urlpatterns = [
    path(
        'self/', SelfUserProfileView.as_view(),
        name='user_profile'
    ),
    path(
        '<pk>', UserProfileView.as_view({'get': 'retrieve'}),
        name='other_profile'
    ),
]
