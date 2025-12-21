"""
Утилиты для отправки email с красивыми шаблонами
"""
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging


logger = logging.getLogger(__name__)  # 'apps.core.email_utils'


def generate_confirmation_code() -> str:
    """
    Генерирует 4-значный код подтверждения
    """
    return str(random.randint(1000, 9999))


def send_confirmation_email(email: str, username: str = None) -> dict:
    """
    Отправляет письмо с кодом подтверждения

    Args:
        email: Email адрес получателя
        username: Имя пользователя (опционально)

    Returns:
        dict: {'success': bool, 'code': str, 'message': str}
    """
    logger.info(f"Начало отправки письма для {email}")
    try:
        # Генерируем код
        confirmation_code = generate_confirmation_code()

        # Подготавливаем контекст для шаблона
        context = {
            'confirmation_code': confirmation_code,
            'username': username,
            'site_name': 'SkillCrafts',
            'site_url': 'https://skillcrafts.ru',
            'support_email': 'support@skillcrafts.ru',
        }

        # Рендерим HTML и текстовую версии
        html_content = render_to_string(
            'emails/confirmation_email.html', context
        )
        text_content = render_to_string(
            'emails/confirmation_email.txt', context
        )

        # Создаем email сообщение
        subject = f'Код подтверждения SkillCrafts: {confirmation_code}'

        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
            reply_to=[settings.SERVER_EMAIL],
        )

        # Добавляем HTML версию
        email_msg.attach_alternative(html_content, "text/html")

        # Отправляем
        email_msg.send(fail_silently=False)

        logger.info(f"Письмо успешно отправлено на {email}, код: {confirmation_code}")
        return {
            'success': True,
            'code': confirmation_code,
            'message': f'Код подтверждения отправлен на {email}'
        }

    except Exception as e:
        logger.error(f"Ошибка отправки письма на {email}: {str(e)}", exc_info=True)
        return {
            'success': False,
            'code': None,
            'message': f'Ошибка при отправке письма: {str(e)}'
        }


def send_welcome_email(email: str, username: str) -> dict:
    """
    Отправляет приветственное письмо после подтверждения
    """
    try:
        subject = 'Добро пожаловать в SkillCrafts! 🎉'

        context = {
            'username': username,
            'site_name': 'SkillCrafts',
            'site_url': 'https://skillcrafts.ru',
        }

        html_content = render_to_string(
            'templates/emails/welcome_email.html', context
        )
        text_content = render_to_string(
            'templates/emails/welcome_email.txt', context
        )

        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send(fail_silently=False)

        return {'success': True, 'message': 'Приветственное письмо отправлено'}

    except Exception as e:
        return {'success': False, 'message': str(e)}
