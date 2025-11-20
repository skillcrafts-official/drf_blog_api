"""
Тесты моделей приложения profiles
"""
# pylint: disable=too-few-public-methods,no-member

import pytest
from apps.utils import is_django_field_empty
from django.db import transaction, IntegrityError
from apps.profiles.models import Profile


@pytest.mark.django_db
class TestProfileModel:
    """
    Тесты для модели профиля пользователя в базе данных
    """
    def test_create_unique_user_profile(self, users_pool, profile_data):
        """
        Проверяется создание профиля для пользователя
        Один профиль для одного пользователя
        """
        # Создание пользователя на уровне моделей не должно создавать профиль
        users = users_pool()
        assert not Profile.objects.filter(user=users.user1).exists()

        # Для одного пользователя создать можно только один профиль
        r_profile = profile_data(for_user=users.user1)
        profile1 = Profile.objects.create(**r_profile)
        assert isinstance(profile1, Profile), f"{type(profile1) =} "
        assert profile1.user == users.user1
        for attr in r_profile:
            assert getattr(profile1, attr)

        # Повторное создание профиля должно приводить к IntegrityError
        try:
            with transaction.atomic():
                Profile.objects.create(**r_profile)
        except IntegrityError as e:
            assert 'UNIQUE' in str(e), f"{str(e) =} "

    def test_create_user_empty_profile(self, users_pool, profile_data):
        """
        Проверяется возможность создания пустого профиля пользователя
        """
        users = users_pool()

        r_profile = profile_data(for_user=users.user1, is_null=True)
        profile1 = Profile.objects.create(**r_profile)

        for attr in (attr for attr in r_profile if attr != 'user_id'):
            assert is_django_field_empty(getattr(profile1, attr))
