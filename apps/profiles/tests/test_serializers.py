"""
Тесты моделей приложения profiles
"""
# pylint: disable=too-few-public-methods,no-member

import pytest
from apps.utils import create_test_image
from django.db import transaction, IntegrityError
from apps.profiles.serializers import (
    ProfileSerializer, SelfProfileSerializer,
    ProfileImageSerializer
)


@pytest.mark.django_db
class TestSelfProfileSerializer:
    """
    Проверяет сериализатор SelfProfileSerializer
    Проверяет валидацию данных на всех установленных уровнях
    """
    serializer_class = SelfProfileSerializer

    def test_valid_request_for_update_user_profile(self, users_pool, profile_data):
        """
        Проверяется реквест для обновления профиля пользователя
        """
        users = users_pool()
        profile = profile_data(for_user=users.user1)

        profile.pop('user_id')
        # profile['user'] = users.user1

        profile['wallpaper'] = create_test_image('wallpaper.jpg')
        profile['avatar'] = create_test_image('avatar.jpg')

        serializer = self.serializer_class(
            data=profile,
            context={'request': type('Request', (), {'user': users.user1})()}
        )

        assert serializer.is_valid(), serializer.is_valid()

        instance = serializer.save()
        assert instance.user == users.user1

    def test_serialize_nullable_data_from_request(
            self, users_pool, profile_data
    ):
        """
        Проверяется реквест для обновления профиля пользователя
        """
        users = users_pool()
        profile = profile_data(for_user=users.user1, is_null=True)

        profile.pop('user_id')
        profile['user'] = users.user1

        serializer = self.serializer_class(data=profile)

        assert serializer.is_valid(), serializer.is_valid()

    @pytest.mark.parametrize(
        "field, value",
        [
            ('user', None),
            ('user', '1'),
            ('user', 1),
        ]
    )
    def test_foreign_key_fields_from_request_user_profile(
            self, users_pool, profile_data, field, value
    ):
        """
        Проверяется реквест для обновления профиля пользователя
        """
        users = users_pool()
        profile = profile_data(for_user=users.user1, is_null=True)

        profile.pop('user_id')
        profile[field] = value

        serializer = self.serializer_class(data=profile)
        assert serializer.is_valid()

        data = serializer.validated_data
        assert not data.get(field, None), f"{data[field] =} {field =} "

    @pytest.mark.parametrize(
        "field, value",
        [
            ('first_name', 'a' * 21),
            ('last_name', 'a' * 21),
            ('profession', 'a' * 51),
            ('short_desc', 'a' * 301),
        ]
    )
    def test_char_fields_from_user_profile_request(
            self, users_pool, profile_data, field, value
    ):
        """
        Проверяется валидация полей типа CharField
        """
        users = users_pool()
        profile = profile_data(for_user=users.user1)

        profile.pop('user_id')
        profile['user'] = users.user1

        profile['wallpaper'] = None
        profile['avatar'] = None

        profile[field] = value

        serializer = self.serializer_class(data=profile)

        assert not serializer.is_valid(), serializer.is_valid()

    @pytest.mark.parametrize(
        "field, value",
        [
            ('link_to_instagram', 'htt://example.com'),
            ('link_to_telegram', 'https//example.com'),
            ('link_to_github', 'http:/example.com'),
            ('link_to_vk', '//example.com'),
        ]
    )
    def test_url_fields_from_user_profile_request(
            self, users_pool, profile_data, field, value
    ):
        """
        Проверяется валидация полей типа URLField
        """
        users = users_pool()
        profile = profile_data(for_user=users.user1)

        profile.pop('user_id')
        profile['user'] = users.user1

        profile['wallpaper'] = None
        profile['avatar'] = None

        profile[field] = value

        serializer = self.serializer_class(data=profile)

        assert not serializer.is_valid(), serializer.is_valid()

    @pytest.mark.parametrize(
        "field, value",
        [
            ('wallpaper', 'media/wallpapers/wallpaper.jpg'),
            ('avatar', 'media/wallpapers/avatar.jpg'),
        ]
    )
    def test_image_fields_from_user_profile_request(
            self, users_pool, profile_data, field, value
    ):
        """
        Проверяется валидация полей типа ImageField
        """
        users = users_pool()
        profile = profile_data(for_user=users.user1)

        profile.pop('user_id')
        profile['user'] = users.user1

        profile['wallpaper'] = None
        profile['avatar'] = None

        profile[field] = value

        serializer = self.serializer_class(data=profile)

        assert not serializer.is_valid(), serializer.is_valid()
