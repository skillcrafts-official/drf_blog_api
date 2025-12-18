from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from .models import GuestUser, User
from datetime import datetime
import uuid


class UnifiedJWTAuthentication(JWTAuthentication):
    """
    Универсальная JWT аутентификация с поддержкой UUID
    """
    
    def get_user(self, validated_token):
        """
        Получение пользователя на основе токена
        Теперь работает с UUID для обоих типов пользователей
        """
        print(f"=== GET_USER CALLED ===")
        
        # Определяем тип пользователя из токена
        user_type = validated_token.get('type', 'user')
        print(f"User type from token: {user_type}")
        
        if user_type == 'guest':
            # Гостевой пользователь
            guest_id = validated_token.get('guest_id')
            print(f"Guest ID: {guest_id}")
            
            if not guest_id:
                return None
            
            try:
                # Преобразуем строку в UUID
                guest_uuid = uuid.UUID(str(guest_id))
            except (ValueError, AttributeError):
                print(f"Invalid UUID format: {guest_id}")
                return None
            
            try:
                guest = GuestUser.objects.get(guest_id=guest_uuid)
                guest.last_activity = datetime.now()
                guest.save(update_fields=['last_activity'])
                print(f"Guest found: {guest}")
                return guest
            except GuestUser.DoesNotExist:
                print(f"Guest not found, creating new: {guest_id}")
                # Создаем нового гостя
                return GuestUser.objects.create(
                    guest_id=guest_uuid,
                    last_activity=datetime.now()
                )
        
        else:
            # Обычный пользователь
            user_id = validated_token.get('user_id')
            print(f"User ID: {user_id}")
            
            if not user_id:
                return None
            
            try:
                # Пробуем как UUID
                user_uuid = uuid.UUID(str(user_id))
                user = User.objects.get(id=user_uuid)
                print(f"User found by UUID: {user}")
                return user
            except (ValueError, AttributeError):
                # Если не UUID, пробуем как число (для обратной совместимости)
                try:
                    user = User.objects.get(pk=user_id)
                    print(f"User found by numeric ID: {user}")
                    return user
                except (ValueError, User.DoesNotExist):
                    print(f"User not found: {user_id}")
                    return None
            except User.DoesNotExist:
                print(f"User not found: {user_id}")
                return None

# class UnifiedJWTAuthentication(JWTAuthentication):
#     """
#     Универсальная JWT аутентификация без сессий
#     """
    
#     def authenticate(self, request):
#         """
#         Аутентификация только по JWT токену
#         """
#         header = self.get_header(request)
#         if header is None:
#             return None
        
#         raw_token = self.get_raw_token(header)
#         if raw_token is None:
#             return None
        
#         try:
#             # Валидируем токен
#             validated_token = self.get_validated_token(raw_token)
            
#             # Получаем пользователя
#             user = self.get_user_from_token(validated_token)
#             if user is None:
#                 return None
                
#             return (user, validated_token)
            
#         except (TokenError, jwt.InvalidTokenError) as e:
#             raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')
    
#     def get_user_from_token(self, validated_token):
#         """Получение пользователя из токена"""
#         token_type = validated_token.get('type', 'user')
        
#         if token_type == 'guest':
#             # Гостевой токен
#             guest_id = validated_token.get('guest_id')
#             if not guest_id:
#                 return None
            
#             try:
#                 guest = GuestUser.objects.get(guest_id=guest_id)
#                 # Обновляем активность
#                 guest.last_activity = datetime.now()
#                 guest.save(update_fields=['last_activity'])
#                 return guest
#             except GuestUser.DoesNotExist:
#                 # Если гостя нет в БД, создаем его на основе данных из токена
#                 # (если хотите воссоздать гостя)
#                 ip_address = validated_token.get('ip_address', '')
#                 user_agent = validated_token.get('user_agent', '')
                
#                 # Создаем нового гостя с тем же ID
#                 guest = GuestUser.objects.create(
#                     guest_id=guest_id,
#                     ip_address=ip_address,
#                     user_agent=user_agent,
#                     last_activity=datetime.now()
#                 )
#                 return guest
#         else:
#             # Обычный пользовательский токен
#             try:
#                 user_id = validated_token.get('user_id')
#                 return User.objects.get(pk=user_id)
#             except (KeyError, User.DoesNotExist):
#                 return None
