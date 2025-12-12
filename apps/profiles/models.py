from datetime import date
from django.db import models

from rest_framework.exceptions import NotFound, PermissionDenied

from apps.accounts.models import User


WORK_FORMATS = [
    ('office', 'офис'),
    ('hybrid', 'гибрид'),
    ('remote', 'удаленно'),
    ('any', 'любой')
]

EDU_LEVELS = [
    ('not', 'не указано'),
    ('first_middle', '11 классов'),
    ('primary_voc_edu', 'Начальное профессиональное образование'),
    ('secondary_voc_edu', 'Среднее профессиональное образование'),
    ('higher_voc_edu', 'Высшее профессиональное образование')
]


def user_avatar_path(instance, filename):
    """Персонализируется путь к аватару пользователя"""
    return f"avatars/user_{instance.user.id}/{filename}"


def user_wallpaper_path(instance, filename):
    """Персонализируется путь к обоям пользователя"""
    return f"wallpapers/user_{instance.user.id}/{filename}"


class Profile(models.Model):
    """
    Модель для профиля пользователя
    """
    # Персональные данные
    first_name = models.CharField(max_length=20, default='', blank=True)
    middle_name = models.CharField(max_length=50, default='', blank=True)
    last_name = models.CharField(max_length=20, default='', blank=True)
    profession = models.CharField(
        verbose_name='Senior Product Manager | Growth & Monetization',
        max_length=100, default='', blank=True
    )

    # Локация
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    relocation = models.CharField(max_length=200, default='', blank=True)
    # work_formats = models.OneToOneField(
    #     WorkFormat,
    #     on_delete=models.CASCADE,
    #     related_name='profile'
    # )

    # # Образование
    # edu_levels = models.OneToOneField(
    #     RussianEduLevels,
    #     on_delete=models.CASCADE,
    #     related_name='profile'
    # )
    institution_name = models.CharField(max_length=200, default='', blank=True)
    graduation_year = models.SmallIntegerField(null=True, blank=True)

    short_desc = models.CharField(max_length=1000, default='', blank=True)
    full_desc = models.TextField(default='', blank=True)

    wallpaper = models.ImageField(
        upload_to=user_wallpaper_path, null=True, blank=True
    )
    avatar = models.ImageField(
        upload_to=user_avatar_path, null=True, blank=True
    )

    link_to_instagram = models.URLField(default='', blank=True)
    link_to_telegram = models.URLField(default='', blank=True)
    link_to_github = models.URLField(default='', blank=True)
    link_to_vk = models.URLField(default='', blank=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __iter__(self):
        for field in self._meta.fields:  # pylint: disable=no-member
            if not field.auto_created:
                yield field.name, getattr(self, field.name)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def get_profile(cls, user_id):
        """Получаем профиль по user_id"""
        try:
            profile = cls.objects.get(user_id=user_id)
        except cls.DoesNotExist:
            profile = None

        if profile is None:
            raise NotFound(
                detail="Profile not found"
            )

        return profile

    def delete(self, using=None, keep_parents=False):
        # user = User.objects.get(pk=self.user)
        self.user.is_active = False
        self.user.save()

    @property
    def full_name(self):
        return str(self)

    @property
    def email(self):
        return self.user.primary_email

    @property
    def total_experience_years(self):
        # Расчет общего опыта работы
        experiences = self.experiences.all()
        if not experiences:
            return 0

        total_days = 0
        for exp in experiences:
            if exp.end_date:
                total_days += (exp.end_date - exp.start_date).days
            else:
                total_days += (date.today() - exp.start_date).days

        return round(total_days / 365.25, 1)


class WorkFormat(models.Model):
    """
    Модель для хранения форматов работы
    """
    office = models.BooleanField(default=False, blank=True)
    hybrid = models.BooleanField(default=False, blank=True)
    remote = models.BooleanField(default=False, blank=True)

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='work_formats'
    )

    class Meta:
        verbose_name = 'Форматы работы'
        verbose_name_plural = 'Форматы работы'


class RussianEduLevel(models.Model):
    """
    Модель для хранения уровней образования в России
    """
    nothing = models.BooleanField(default=False, blank=True)
    first_middle = models.BooleanField(default=False, blank=True)
    primary_voc_edu = models.BooleanField(default=False, blank=True)
    secondary_voc_edu = models.BooleanField(default=False, blank=True)
    higher_voc_edu = models.BooleanField(default=False, blank=True)

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='edu_level'
    )

    class Meta:
        verbose_name = 'Уровни государственного образования'
        verbose_name_plural = 'Уровни государственного образования'
