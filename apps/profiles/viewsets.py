from django.core.cache import cache
from django.db.models import F

from rest_framework import viewsets
from rest_framework.serializers import BaseSerializer, ModelSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from apps.profiles.models import Profile, ProfileSkill, Skill, WorkFormat
from apps.profiles.serializers import (
    ProfileSkillSerializer, UpdateProfileSkillSerializer, SkillSerializer,
    WorkFormatSerializer,
    ProfileSerializer, PrivacyProfileSkillSerializer
)
from apps.accounts.permissions import AllowGuests


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowGuests]

    def create(self, request, *args, **kwargs) -> Response:
        user = request.user
        user_id = kwargs.get('user_id', None)
        profile_id = kwargs.get('profile', None)
        if profile_id is None:
            profile_id = request.data.get('profile', None)
        if user.pk != (user_id if user_id else profile_id):
            raise PermissionDenied()
        return super().create(request, *args, **kwargs)

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
            raise PermissionDenied()
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


class ProfilesView(viewsets.ModelViewSet):
    """Для выдачи списка профилей"""
    queryset = Profile.objects.filter(user__is_active=True)
    serializer_class = ProfileSerializer

    @action(detail=False, methods=['get'])
    def education_levels(self, request):
        """
        Кастомный ендпоинт выдаёт список языков
        для компонентов выбора на клиенте
        """
        cache_key = 'education_choices'
        choices = cache.get(cache_key)

        if not choices:
            choices = dict(Profile.EDUCATION_CHOICES)
            cache.set(cache_key, choices, timeout=3600)  # Кэш на 1 час

        return Response(choices)


class WorkFormatView(BaseModelViewSet):
    """Для выдачи предпочитаемых форматов работы"""
    queryset = WorkFormat.objects.all()
    serializer_class = WorkFormatSerializer
    lookup_field = 'profile'


class ProfileSkillViewSet(BaseModelViewSet):
    """Для выдачи навыков пользователя"""
    queryset = ProfileSkill.objects.all()
    serializer_class = ProfileSkillSerializer
    lookup_field = 'profile'

    def get_queryset(self):
        if self.action in ['partial_update', 'destroy']:
            return ProfileSkill.objects.filter(
                profile=self.kwargs.get('profile'),
                id=self.kwargs.get('skill')
            ).annotate(
                skill_name=F('skill__name')
            ).select_related('skill')

        return ProfileSkill.objects.annotate(
            skill_name=F('skill__name')
        ).select_related('skill')

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UpdateProfileSkillSerializer
        return super().get_serializer_class()


class PrivacyProfileSkillViewSet(BaseModelViewSet):
    queryset = ProfileSkill.objects.all()
    serializer_class = PrivacyProfileSkillSerializer
    lookup_field = 'profile'


class SkillViewSet(BaseModelViewSet):
    """Для выдачи предпочитаемых форматов работы"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = 'pk'
