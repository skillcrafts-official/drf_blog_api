from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Автоматически создает Profile при создании нового User
    """
    if created:
        from apps.profiles.handlers import create_user_profile_handler
        create_user_profile_handler(user_instance=instance)
