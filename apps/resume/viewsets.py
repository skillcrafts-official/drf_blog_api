from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.resume.serializers import (
    SummarySerializer, PrivacySummarySerializer,
    LanguageSerializer, UpdateLanguageSerializer, PrivacyLanguageSerializer,
    SkillSerializer, PrivacySkillSerializer,
    WorkExperienceSerializer, PrivacyWorkExperienceSerializer,
    WorkResultSerializer, PrivacyWorkResultSerializer,
    SkillClusterSerializer, UpdateSkillClusterSerializer,
    SertificateSerializer, UpdateSertificateSerializer,
    PrivacySertificateSerializer
)
from apps.resume.models import (
    Language, Skill, Summary, WorkExperience, WorkResult, SkillCluster,
    Sertificate
)
from apps.resume.filters import (
    SummaryFilters, WorkExperienceFilters, LanguageFilters,
    SertificateFilters, SkillClusterFilters, SkillFilters,
    WorkResultFilters
)


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    # def create(self, request, *args, **kwargs) -> Response:
    #     user = request.user
    #     if user.pk != kwargs['user_id']:
    #         raise PermissionDenied()
    #     return super().update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        user = request.user
        user_id = kwargs.get('user_id', None)
        profile_id = kwargs.get('profile', None)
        if profile_id is None:
            profile_id = request.data.get('profile', None)
        if user.pk != (user_id if user_id else profile_id):
            raise PermissionDenied()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs) -> Response:
        user = request.user
        user_id = kwargs.get('user_id', None)
        profile_id = kwargs.get('profile', None)
        if profile_id is None:
            profile_id = request.data.get('profile', None)
        if user.pk != (user_id if user_id else profile_id):
            raise PermissionDenied(f'{user.pk = } {user_id = } {profile_id = }')
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> Response:
        user = request.user
        user_id = kwargs.get('user_id', None)
        profile_id = kwargs.get('profile', None)
        if profile_id is None:
            profile_id = request.data.get('profile', None)
        if user.pk != (user_id if user_id else profile_id):
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)


class SummaryViewSet(BaseModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
    filterset_class = SummaryFilters

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            # Оптимизация запросов для детального просмотра
            queryset = (
                queryset.select_related('profile__user')
                .prefetch_related(
                    'profile__experiences',
                    'profile__experiences__results',
                    'profile__skills__cluster',
                    'profile__certificates',
                    'profile__languages'
                )
            )
        return queryset


class PrivacySummaryViewSet(BaseModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = PrivacySummarySerializer
    lookup_field = 'pk'


class WorkExperienceViewSet(BaseModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    filterset_class = WorkExperienceFilters
    lookup_field = 'pk'


class PrivacyWorkExperienceViewSet(BaseModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = PrivacyWorkExperienceSerializer
    lookup_field = 'pk'


class WorkResultViewSet(BaseModelViewSet):
    queryset = WorkResult.objects.all()
    serializer_class = WorkResultSerializer
    filterset_class = WorkResultFilters
    # lookup_field = 'pk'


# class UpdateWorkResultViewSet(BaseModelViewSet):
#     queryset = WorkResult.objects.all()
#     serializer_class = UpdateWorkResultSerializer
#     lookup_field = 'pk'


class PrivacyWorkResultViewSet(BaseModelViewSet):
    queryset = WorkResult.objects.all()
    serializer_class = PrivacyWorkResultSerializer
    lookup_field = 'pk'


class SkillClusterViewSet(BaseModelViewSet):
    queryset = SkillCluster.objects.all()
    serializer_class = SkillClusterSerializer
    filterset_class = SkillClusterFilters
    # lookup_field = 'skill-cluster-id'


class UpdateSkillClusterViewSet(BaseModelViewSet):
    queryset = SkillCluster.objects.all()
    serializer_class = UpdateSkillClusterSerializer
    lookup_field = 'pk'


class SkillViewSet(BaseModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filterset_class = SkillFilters
    # lookup_field = 'skill-id'


class PrivacySkillViewSet(BaseModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = PrivacySkillSerializer
    lookup_field = 'pk'


class SertificateViewSet(BaseModelViewSet):
    queryset = Sertificate.objects.all()
    serializer_class = SertificateSerializer
    filterset_class = SertificateFilters


class UpdateSertificateViewSet(BaseModelViewSet):
    queryset = Sertificate.objects.all()
    serializer_class = UpdateSertificateSerializer
    lookup_field = 'pk'


class PrivacySertificateViewSet(BaseModelViewSet):
    queryset = Sertificate.objects.all()
    serializer_class = PrivacySertificateSerializer
    lookup_field = 'pk'


class LanguageViewSet(BaseModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filterset_class = LanguageFilters
    # lookup_field = 'language-id'

    @action(detail=False, methods=['get'])
    def languages(self, request):
        """
        Кастомный ендпоинт выдаёт список языков
        для компонентов выбора на клиенте
        """
        cache_key = 'lang_choices'
        choices = cache.get(cache_key)

        if not choices:
            choices = dict(sorted(Language.LANGUAGES))
            cache.set(cache_key, choices, timeout=3600)  # Кэш на 1 час

        return Response(choices)

    @action(detail=False, methods=['get'])
    def levels(self, request):
        """
        Кастомный ендпоинт выдаёт список уровней владения
        языками для компонентов выбора на клиенте
        """
        cache_key = 'level_choices'
        choices = cache.get(cache_key)

        if not choices:
            choices = dict(sorted(Language.LANGUAGE_LEVELS))
            cache.set(cache_key, choices, timeout=3600)  # Кэш на 1 час

        return Response(choices)


class UpdateLanguageViewSet(BaseModelViewSet):
    queryset = Language.objects.all()
    serializer_class = UpdateLanguageSerializer
    # filterset_class = LanguageFilters
    lookup_field = 'pk'


class PrivacyLanguageViewSet(BaseModelViewSet):
    queryset = Language.objects.all()
    serializer_class = PrivacyLanguageSerializer
    lookup_field = 'pk'
