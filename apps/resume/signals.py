from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.resume.models import WorkExperience


@receiver(post_save, sender=WorkExperience)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Автоматически создает Profile при создании нового User
    """
    if created:
        from apps.resume.handlers import create_work_result_handler
        create_work_result_handler(work_experience=instance)
