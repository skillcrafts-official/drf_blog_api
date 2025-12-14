from os import name
from django.db import transaction

from apps.profiles.models import Profile, WorkFormat, RussianEduLevel
from apps.privacy_settings.models import ProfilePrivacySettings
from apps.resume.models import Summary, WorkExperience, Language


def create_user_profile_handler(user_instance):
    """
    Обработчик: Создает Profile для нового User
    """
    try:
        with transaction.atomic():
            profile, _ = Profile.objects.get_or_create(user=user_instance)
            work_formats, _ = WorkFormat.objects.get_or_create(profile=profile)
            # edu_levels, _ = RussianEduLevel.objects.get_or_create(
            #     profile=profile,
            #     nothing=True
            # )
            privacy, _ = ProfilePrivacySettings.objects.get_or_create(profile=profile)
            summary, _ = Summary.objects.get_or_create(profile=profile)
            work_experience, _ = WorkExperience.objects.get_or_create(profile=profile)
            language, _ = Language.objects.get_or_create(
                profile=profile,
                name='russian',
                level='N'
            )
            return profile

    except Exception as e:
        # try:
        #     return Profile.objects.create(user=user_instance)
        # except:
        raise e
