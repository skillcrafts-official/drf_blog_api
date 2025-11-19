"""Local conftest.py"""
import pytest
from faker import Faker

# from apps.accounts.models import User
# from apps.profiles.models import Profile

# Нужна фикстура, которая будет создавать тестового пользователя и авторизовываться
# Также нужны фабрики фикстур данных

fake = Faker()  # Создаем экземпляр Faker
Faker.seed(42)  # Для воспроизводимости результатов


@pytest.fixture
def profile_data():
    """
    Фабрика профилей пользователя для apps.profiles.models.Profile
    """
    def get_profile(user_id: int, **kwargs):
        defaults = {
            "user_id": user_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "profession": fake.job(),
            "short_desc": fake.paragraph(3),
            "full_desc": fake.paragraph(20),
            "wallpaper": fake.uri_path(),
            "avatar": fake.uri_path(),
            "link_to_instagram": f"https://instagram.com/{fake.user_name()}",
            "link_to_telegram": f"https://t.me/{fake.user_name()}",
            "link_to_github": f"https://github.com/{fake.user_name()}",
            "link_to_vk": f"https://vk.com/{fake.user_name()}"
        }
        defaults.update(kwargs)
        return defaults
        # if user is None:
        #     return defaults
        # return Profile.objects.update(**defaults, user=user)
    return get_profile


# print(profile()(1))
# print(profile()())
