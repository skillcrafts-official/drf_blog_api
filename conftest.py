"""Global conftest.py"""
import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


@pytest.fixture(scope='class')
def users_pool():
    """Пул пользователей"""
    # pylint: disable=too-few-public-methods
    class UsersPool:
        """
        Создаёт именные атрибуты пользователей
        """
        def __init__(self, quantity: int = 1):
            for i in range(quantity):
                user_data = {
                    'email': f'testuser{i + 1}@example.com',
                    'password': 'testpass123'
                }
                setattr(
                    self, f'user{i + 1}',
                    User.objects.create(**user_data)
                )

    return UsersPool


@pytest.fixture
def auth_client():
    """Фабрика API клиентов с JWT токеном в заголовках"""
    def create_auth_clint(**kwargs):
        user = kwargs.get('user')
        refresh = RefreshToken.for_user(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
    return create_auth_clint
