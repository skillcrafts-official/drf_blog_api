import jwt
from django.conf import settings

from rest_framework.authentication import BaseAuthentication

from apps.accounts.models import GuestUser


class GuestAuthentication(BaseAuthentication):
    """Кастомная аутентификация для гостевых токенов"""

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            # Декодируем JWT
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256']
            )

            # Проверяем что это гость
            if payload.get('type') != 'guest':
                return None

            # Находим гостя в БД
            guest_id = payload.get('guest_id')
            if not guest_id:
                return None

            try:
                guest = GuestUser.objects.get(guest_id=guest_id)
                return (guest, token)  # (user, auth)
            except GuestUser.DoesNotExist:
                return None

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
