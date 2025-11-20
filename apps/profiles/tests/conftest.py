"""Local conftest.py"""
import pytest
from faker import Faker

from apps.accounts.models import User
# from apps.profiles.models import Profile


fake = Faker()  # Создаем экземпляр Faker
Faker.seed(42)  # Для воспроизводимости результатов


@pytest.fixture
def profile_data():
    """
    Фабрика профилей пользователя для apps.profiles.models.Profile
    """
    def get_profile(*, for_user: User, is_null=False, **kwargs):
        defaults = {
            "user_id": for_user.pk,
            "first_name": None if is_null else fake.first_name(),
            "last_name": None if is_null else fake.last_name(),
            "profession": None if is_null else fake.job(),
            "short_desc": None if is_null else fake.paragraph(3),
            "full_desc": None if is_null else fake.paragraph(20),
            "wallpaper": None if is_null else fake.uri_path(),
            "avatar": None if is_null else fake.uri_path(),
            "link_to_instagram": None if is_null else f"https://instagram.com/{fake.user_name()}",  # noqa: E501 pylint: disable=line-too-long
            "link_to_telegram": None if is_null else f"https://t.me/{fake.user_name()}",            # noqa: E501 pylint: disable=line-too-long
            "link_to_github": None if is_null else f"https://github.com/{fake.user_name()}",        # noqa: E501 pylint: disable=line-too-long
            "link_to_vk": None if is_null else f"https://vk.com/{fake.user_name()}"                 # noqa: E501 pylint: disable=line-too-long
        }
        defaults.update(kwargs)
        return defaults
        # if user is None:
        #     return defaults
        # return Profile.objects.update(**defaults, user=user)
    return get_profile


# print(profile()(1))
# print(profile()())
