"""
Сигналы для автоматической отправки email при регистрации
"""
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.email_utils import send_confirmation_email
from apps.accounts.models import User


@receiver(post_save, sender=User)
def send_email_on_user_creation(sender, instance, created, **kwargs):
    """
    Отправляет письмо с кодом подтверждения при создании пользователя
    """
    print('=== Send Code EMAIL ===')
    if created and instance.primary_email:
        # Проверяем, что email подтверждён (если у вас есть такое поле)
        print(f'{getattr(instance, 'email_verified', False) = }')
        if not getattr(instance, 'email_verified', False):
            # Отправляем код подтверждения
            result = send_confirmation_email(
                email=instance.primary_email,
                username=instance.primary_email
            )

            # Сохраняем код в базе (если нужно)
            if result['success']:
                # Здесь можно сохранить код в модель пользователя
                instance.confirmation_code = result['code']
                instance.generated_code_at = timezone.now()
                instance.save(update_fields=['confirmation_code'])
                pass
        print(f'{result = }')


# @receiver(post_save, sender=User)
# def send_welcome_on_email_verification(sender, instance, **kwargs):
#     """
#     Отправляет приветственное письмо при подтверждении email
#     """
#     # Проверяем, изменился ли статус подтверждения email
#     if hasattr(instance, 'email_verified'):
#         # Нужно отслеживать изменения через django-model-utils или вручную
#         pass