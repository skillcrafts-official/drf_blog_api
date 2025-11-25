"""Сериализаторы для профилей пользователей"""
# pylint: disable=too-few-public-methods,no-member

from rest_framework import serializers
from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выдачи профиля пользователя
    по запросу авторизованного пользователя
    """
    class Meta:
        model = Profile
        fields = '__all__'


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
