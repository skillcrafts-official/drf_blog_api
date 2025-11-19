"""Global conftest.py"""
import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


@pytest.fixture
def get_user():
    """Фабрика пользователей"""
    def create_user(**kwargs):
        defaults = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        defaults.update(kwargs)
        return User.objects.create(**defaults)
    return create_user


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
