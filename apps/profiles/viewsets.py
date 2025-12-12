from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, BasePermission

from apps.profiles.models import Profile, WorkFormat, RussianEduLevel
from apps.profiles.serializers import (
    WorkFormatSerializer, RussianEduLevelSerializer, ProfileSerializer
)
from apps.profiles.filters import ProfileFilters


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    # def create(self, request, *args, **kwargs) -> Response:
    #     user = request.user
    #     if user.pk != kwargs['user_id']:
    #         raise PermissionDenied()
    #     return super().update(request, *args, **kwargs)

    def get_user_id(self, **kwargs):
        return kwargs.get('user_id', None)

    def get_profile_id(self, **kwargs):
        return kwargs.get('profile', None)

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
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> Response:
        user = request.user
        user_id = kwargs.get('user_id', None)
        profile_id = kwargs.get('profile', None)
        if profile_id is None:
            profile_id = request.data.get('profile', None)
        if user.pk != (user_id if user_id else profile_id):
            raise PermissionDenied()
        return super().update(request, *args, **kwargs)


# class ProfilesView(viewsets.ModelViewSet):
#     """Для выдачи списка профилей"""
#     queryset = Profile.objects.filter(user__is_active=True)
#     serializer_class = ProfileSerializer
#     filterset_class = ProfileFilters
    # lookup_field = 'pk'


class WorkFormatView(BaseModelViewSet):
    """Для выдачи предпочитаемых форматов работы"""
    queryset = WorkFormat.objects.all()
    serializer_class = WorkFormatSerializer
    lookup_field = 'profile'


class RussianEduLevelView(BaseModelViewSet):
    """Для выдачи списка профилей"""
    queryset = RussianEduLevel.objects.all()
    serializer_class = RussianEduLevelSerializer
    # filterset_class = RussianEduLevelFilters
    lookup_field = 'profile'
