from django.db.models.query import QuerySet

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.privacy_settings.serializers import (
    ProfilePrivacySettingsSerializer, UpdateProfilePrivacySettingsSerializer,
    ProfileUserBlockSerializer, ProfileUserUnblockSerializer,
    ProfileUserAddSerializer, ProfileUserExcludeSerializer
)
from apps.privacy_settings.models import ProfilePrivacySettings


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class ProfilePrivacySettingsView(BaseModelViewSet):
    queryset = ProfilePrivacySettings.objects.all()
    serializer_class = ProfilePrivacySettingsSerializer
    lookup_field = 'pk'


class UpdateProfilePrivacySettingsView(BaseModelViewSet):
    queryset = ProfilePrivacySettings.objects.all()
    serializer_class = UpdateProfilePrivacySettingsSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs) -> Response:
        user = request.user
        if user.pk != kwargs['pk']:
            raise PermissionDenied()
        return super().update(request, *args, **kwargs)


class ProfileUserBlockView(BaseModelViewSet):
    queryset = ProfilePrivacySettings.objects.all()
    serializer_class = ProfileUserBlockSerializer
    lookup_field = 'pk'


class ProfileUserUnblockView(BaseModelViewSet):
    queryset = ProfilePrivacySettings.objects.all()
    serializer_class = ProfileUserUnblockSerializer
    lookup_field = 'pk'


class ProfileUserAddView(BaseModelViewSet):
    queryset = ProfilePrivacySettings.objects.all()
    serializer_class = ProfileUserAddSerializer
    lookup_field = 'pk'


class ProfileUserExcludeView(BaseModelViewSet):
    queryset = ProfilePrivacySettings.objects.all()
    serializer_class = ProfileUserExcludeSerializer
    lookup_field = 'pk'