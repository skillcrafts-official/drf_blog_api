"""Кастомный класс для JWT аутентификации"""
import uuid
from datetime import datetime

from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import GuestUser, User


class UnifiedJWTAuthentication(JWTAuthentication):
    """
    Универсальная JWT аутентификация с поддержкой UUID
    """

    def get_user(self, validated_token):
        """
        Получение пользователя на основе токена
        Теперь работает с UUID для обоих типов пользователей
        """
        print("=== GET_USER CALLED ===")

        # Определяем тип пользователя из токена
        user_type = validated_token.get('group', 'user')
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
                guest = GuestUser.objects.get(guest_uuid=guest_uuid)
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
