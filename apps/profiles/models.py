from django.db import models

from apps.accounts.models import User


def user_avatar_path(instance, filename):
    # uploads/avatars/user_123/avatar_1641234567890.jpg
    # timestamp = int(time.time())
    extension = filename.split('.')[-1]
    # filename = f"avatar_{timestamp}.{extension}"
    return f"avatars/user_{instance.user.id}/{filename}"


class Profile(models.Model):
    """
    Модель для профиля пользователя
    """
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)
    short_desc = models.CharField(max_length=300, null=True, blank=True)
    full_desc = models.TextField(null=True, blank=True)

    wallpaper = models.ImageField(upload_to='wallpapers/', null=True, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)

    link_to_instagram = models.URLField(null=True, blank=True)
    link_to_vk = models.URLField(null=True, blank=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profiles'
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
