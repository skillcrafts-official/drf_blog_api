"""
Тесты моделей приложения profiles
"""
# pylint: disable=too-few-public-methods,no-member

import pytest

from rest_framework.exceptions import ValidationError

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer


@pytest.mark.django_db
class TestProfileSerializer:
    """
    Проверяет сериализатор ProfileSerializer, который
    возвращает данные по user_id для авторизованных пользователей
    """
    serializer_class = ProfileSerializer

    def test_execute_profile_data_from_db(
            self, users_pool, profile_data, temp_media):
        """
        Проверяется извлечение данных из БД сериализатором
        """
        users = users_pool()
        profile1 = profile_data(for_user=users.user1)

        db_profile = Profile.objects.create(**profile1)
        serializer = self.serializer_class(instance=db_profile)

        # проверка структуры данных, загруженных из БД
        for field, value in profile1.items():
            if field == 'user_id':
                assert isinstance(serializer.data['user'], type(value))
            elif isinstance(value, SimpleUploadedFile):
                assert isinstance(serializer.data[field], type(value.name))
            else:
                assert isinstance(serializer.data[field], type(value))

    def test_update_profile_data_in_db(
            self, users_pool, profile_data, temp_media):
        """
        Проверяется обновление данных в БД сериализатором
        """
        users = users_pool()
        profile1 = profile_data(for_user=users.user1)
        profile2 = profile_data(for_user=users.user1)
        profile3 = profile_data(for_user=users.user1)

        db_profile = Profile.objects.create(**profile1)

        # попытка полного обновления данных (user_id is UNIQUE)
        serializer = self.serializer_class(
            instance=db_profile, data=profile2
        )

        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        assert 'user' in str(exc_info.value), exc_info.value

        # попытка частичного обновления данных (без user_id)
        serializer = self.serializer_class(
            instance=db_profile, data=profile3, partial=True
        )

        assert serializer.is_valid(raise_exception=True)

        serializer.save()

        # проверка структуры очищенных данных (кроме user_id)
        profile3.pop('user_id')
        for field, value in profile3.items():
            assert serializer.validated_data[field] == value
