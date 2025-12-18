# import jwt
# from django.conf import settings

# from rest_framework.authentication import BaseAuthentication

# from apps.accounts.models import GuestUser


# class GuestAuthentication(BaseAuthentication):
#     """Кастомная аутентификация для гостевых токенов"""

#     def authenticate(self, request):
#         auth_header = request.headers.get('Authorization')

#         if not auth_header or not auth_header.startswith('Bearer '):
#             return None

#         token = auth_header.split(' ')[1]

#         try:
#             # Декодируем JWT
#             payload = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=['HS256']
#             )

#             # Проверяем что это гость
#             if payload.get('type') != 'guest':
#                 return None

#             # Находим гостя в БД
#             guest_id = payload.get('guest_id')
#             if not guest_id:
#                 return None

#             try:
#                 guest = GuestUser.objects.get(guest_id=guest_id)
#                 return (guest, token)  # (user, auth)
#             except GuestUser.DoesNotExist:
#                 return None

#         except jwt.ExpiredSignatureError:
#             return None
#         except jwt.InvalidTokenError:
#             return None


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings
from .models import GuestUser, User


class UnifiedJWTAuthentication(JWTAuthentication):
    """
    Универсальная аутентификация для:
    - Обычных пользователей (type: 'user')
    - Гостевых пользователей (type: 'guest')
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            # Валидируем токен
            validated_token = self.get_validated_token(raw_token)

            # Получаем пользователя на основе типа токена
            user = self.get_user(validated_token)

            return (user, validated_token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

    def get_validated_token(self, raw_token):
        """Декодирование и валидация токена"""
        try:
            # Декодируем без проверки подписи сначала
            unverified = jwt.decode(
                raw_token,
                options={"verify_signature": False}
            )
            
            # Определяем алгоритм
            algorithm = unverified.get('alg', 'HS256')
            
            # Декодируем с проверкой подписи
            return jwt.decode(
                raw_token,
                settings.SECRET_KEY,
                algorithms=[algorithm]
            )
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')
    
    def get_user(self, validated_token):
        """Получение пользователя на основе токена"""
        token_type = validated_token.get('type', 'user')
        
        if token_type == 'guest':
            # Гостевой токен
            guest_id = validated_token.get('guest_id')
            if not guest_id:
                return None
            
            try:
                return GuestUser.objects.get(guest_id=guest_id)
            except GuestUser.DoesNotExist:
                return None
        else:
            # Обычный пользовательский токен
            try:
                user_id = validated_token.get(settings.SIMPLE_JWT['USER_ID_CLAIM'])
                return User.objects.get(pk=user_id)
            except (KeyError, User.DoesNotExist):
                return None