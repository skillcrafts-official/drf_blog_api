from django.urls import path

from apps.profiles.views import UserProfileView
from apps.profiles.viewsets import (
    WorkFormatView, ProfilesView,
    ProfileSkillViewSet, SkillViewSet, PrivacyProfileSkillViewSet
)


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
    path(
        '<int:profile>/skills/',
        ProfileSkillViewSet.as_view({'get': 'retrieve', 'post': 'create'}),
        name='get_profile_skills'
    ),
    path(
        '<int:profile>/skills/<int:skill>/',
        ProfileSkillViewSet.as_view({'delete': 'destroy'}),
        name='destroy_profile_skill'
    ),
    path(
        '<int:profile>/skills/<int:skill>/privacies/',
        PrivacyProfileSkillViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
        name='update_skill_privacy_setting'
    ),
    path(
        'displays/education-levels/',
        ProfilesView.as_view({'get': 'education_levels'}),
        name='update_user_profile'
    ),
    path(
        'displays/skills/',
        SkillViewSet.as_view({'get': 'list'}),
        name='get_skill_list'
    )
]
