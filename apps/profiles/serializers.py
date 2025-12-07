"""Сериализаторы для профилей пользователей"""
# pylint: disable=too-few-public-methods,no-member
from rest_framework import serializers
from apps.profiles.models import Profile

from apps.privacy_settings.models import ProfilePrivacySettings


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выдачи профиля пользователя
    по запросу авторизованного пользователя
    """
    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        """
        Маскуются поля в зависимости от настроек приватности
        при отображении (GET запросы)
        """
        representation = super().to_representation(instance)

        request = self.context.get('request')

        if request and not request.user.is_authenticated:
            try:
                privacy_settings = (
                    ProfilePrivacySettings.objects
                    .get(profile=instance)
                )
            except ProfilePrivacySettings.DoesNotExist:
                return representation

            for field_name in representation.keys():
                if field_name in ('id', 'user'):
                    continue

                access_level = getattr(privacy_settings, field_name, 'all')

                if access_level != 'all':
                    representation[field_name] = '*****'

            return representation

        return representation


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления профиля пользователя
    (модели Profile) в контексте авторизованного пользователя
    """
    class Meta:
        model = Profile
        exclude = ['user']


class ProfileImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления всего медиа-контента
    в контексте авторизованного пользователя (НА БУДУЩЕЕ)
    """
    avatar_url = serializers.ImageField(source="avatar", read_only=True)
    wallpaper_url = serializers.ImageField(source="wallpaper", read_only=True)

    class Meta:
        model = Profile
        fields = ['avatar_url', 'wallpaper_url']
