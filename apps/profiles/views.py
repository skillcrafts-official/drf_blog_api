# pylint: disable=no-member,unused-argument
from django.db.models.query import QuerySet

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, BasePermission

from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer
from apps.privacy_settings.models import ProfilePrivacySettings


class ProfilesView(viewsets.ModelViewSet):
    """Для выдачи списка профилей"""
    queryset = Profile.objects.filter(user__is_active=True)
    serializer_class = ProfileSerializer
    lookup_field = 'pk'


class UserProfileView(APIView):
    """Выдача профиля"""
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        """Получение профиля"""
        user = request.user
        profile = Profile.get_profile(kwargs['pk'])
        privacy = ProfilePrivacySettings.objects.get(profile=profile)
        if user and user.is_authenticated and user in privacy.blacklist.all():
            raise PermissionDenied()
        serializer = self.serializer_class(
            profile, context={'request': request}
        )
        return Response(data=serializer.data, status=200)


class UpdateUserProfileView(APIView):
    """Ендпоинты для обновления профиля"""
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, BasePermission]

    def post(self, request, *args, **kwargs):
        """Обновление своего профиля"""
        data = request.data
        user_id = kwargs['pk']
        user = request.user

        if user_id != user.id:
            raise PermissionDenied()

        profile = Profile.get_profile(kwargs['pk'])

        serializer = self.serializer_class(
            instance=profile, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        """Мягкое удаление своего профиля"""
        user = request.user
        user_id = kwargs['pk']

        if user_id != user.id:
            raise PermissionDenied()

        profile = Profile.get_profile(kwargs['pk'])
        profile.delete()

        response = Response(status=status.HTTP_204_NO_CONTENT)
        response['X-Message'] = 'User has been deleted!'
        return response
