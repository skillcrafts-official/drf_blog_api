"""The urls routing for app $PATH_TO_APP"""
from django.urls import path

from apps.resume.viewsets import (
    SkillViewSet, PrivacySkillViewSet, SummaryViewSet, PrivacySummaryViewSet,
    LanguageViewSet, UpdateLanguageViewSet, PrivacyLanguageViewSet,
    WorkExperienceViewSet,
    PrivacyWorkExperienceViewSet,
    WorkResultViewSet, PrivacyWorkResultViewSet,
    SkillClusterViewSet, UpdateSkillClusterViewSet,
    SertificateViewSet, UpdateSertificateViewSet, PrivacySertificateViewSet
)


urlpatterns = [
    path(
        '', SummaryViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='get_resume_list'
    ),
    path(
        '<int:pk>/<int:user_id>/privacies/',
        PrivacySummaryViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
        name='update_resume_privacy_setting'
    ),
    path(
        'work-experiences/',
        WorkExperienceViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='add_user_experiences'
    ),
    path(
        'work-experiences/<int:pk>/',
        WorkExperienceViewSet.as_view({'patch': 'partial_update'}),
        name='udpate_user_experiences'
    ),
    path(
        'work-experiences/<int:pk>/<int:user_id>/privacies/',
        PrivacyWorkExperienceViewSet.as_view({
            'get': 'retrieve', 'put': 'update'
        }),
        name='update_work_experience_privacy_setting'
    ),
    path(
        'work-experiences/results/',
        WorkResultViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='get_user_experience_results'
    ),
    path(
        'work-experiences/results/<int:pk>/<int:user_id>/',
        WorkResultViewSet.as_view({'patch': 'partial_update'}),
        name='udpate_experience_results'
    ),
    path(
        'work-experiences/results/<int:pk>/<int:user_id>/privacies/',
        PrivacyWorkResultViewSet.as_view({
            'get': 'retrieve', 'put': 'update'
        }),
        name='update_work_result_privacy_setting'
    ),
    path(
        'skill-clusters/',
        SkillClusterViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='get_skill_clusters'
    ),
    # path(
    #     'skill-clusters/update/',
    #     UpdateSkillClusterViewSet.as_view({'post': 'create'}),
    #     name='update_skill_clusters'
    # ),
    path(
        'skills/',
        SkillViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='get_skills'
    ),
    path(
        'skills/<int:pk>/<int:user_id>/privacies/',
        PrivacySkillViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
        name='update_skill_privacy_setting'
    ),
    path(
        'sertificates/',
        SertificateViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='get_sertificates'
    ),
    path(
        'sertificates/<int:pk>/',
        UpdateSertificateViewSet.as_view({
            'patch': 'partial_update', 'delete': 'destroy'
        }),
        name='update_sertificates'
    ),
    path(
        'sertificates/<int:pk>/<int:user_id>/privacies/',
        PrivacySertificateViewSet.as_view({
            'get': 'retrieve', 'put': 'update'
        }),
        name='update_sertificate_privacy_setting'
    ),
    path(
        'languages/',
        LanguageViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='get_languages'
    ),
    path(
        'languages/<int:pk>/',
        UpdateLanguageViewSet.as_view({
            'patch': 'partial_update', 'delete': 'destroy'
        }),
        name='update_languages'
    ),
    path(
        'languages/<int:pk>/<int:user_id>/privacies/',
        PrivacyLanguageViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
        name='update_language_privacy_setting'
    ),
]
