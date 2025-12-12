from django.urls import path

from apps.profiles.views import (
    UserProfileView, UpdateUserProfileView
)
from apps.profiles.viewsets import (
    ProfilesView, RussianEduLevelView, WorkFormatView
)


urlpatterns = [
    path(
        '', ProfilesView.as_view({'get': 'list'}),
        name='get_profile_list'
    ),
    # path(
    #     '<int:pk>/get/', UserProfileView.as_view(),
    #     name='get_user_profile'
    # ),
    path(
        '<int:pk>/', UpdateUserProfileView.as_view(),
        name='update_user_profile'
    ),
    path(
        '<int:profile>/education_level/',
        RussianEduLevelView.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
        name='update_user_education_level'
    ),
    path(
        '<int:profile>/work_formats/',
        WorkFormatView.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
        name='update_user_work_formats'
    ),
]
