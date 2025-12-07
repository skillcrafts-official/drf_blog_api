"""The url routing for app $PATH_TO_APP"""
from django.urls import path

from apps.privacy_settings.views import (
    ProfilePrivacySettingsView, UpdateProfilePrivacySettingsView,
    ProfileUserBlockView, ProfileUserUnblockView
    # ProfileGetPrivacySettingsView, ProfileSetPrivacySettingsView
)


urlpatterns = [
    path(
        'profiles/<int:pk>/privacy/',
        ProfilePrivacySettingsView.as_view({'get': 'retrieve'}),
        name='get_profile_privacy_settings'
    ),
    path(
        'profiles/<int:pk>/privacy/update',
        UpdateProfilePrivacySettingsView.as_view({'patch': 'update'}),
        name='update_profile_privacy_settings'
    ),
    path(
        'profiles/<int:pk>/blacklist/user/block/',
        ProfileUserBlockView.as_view({'patch': 'update'}),
        name='profile_add_user_in_blacklist'
    ),
    path(
        'profiles/<int:pk>/blacklist/user/unblock/',
        ProfileUserUnblockView.as_view({'patch': 'update'}),
        name='profile_remove_user_from_blacklist'
    ),
]
