from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from django.utils import timezone

from rest_framework.exceptions import NotFound

from apps.accounts.models import User


class AbstractBaseModel(models.Model):
    """
    Абстрактная базовая модель.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    # created_by = models.ForeignKey(
    #     User, on_delete=models.SET_NULL, related_name='+'
    # )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    # updated_by = models.ForeignKey(
    #     User, on_delete=models.SET_NULL, related_name='+'
    # )

    class Meta:
        abstract = True


class PrivacyBaseModel(AbstractBaseModel):
    PRIVACIES = [
        ('all', 'видно всем'),
        ('not_all', 'видно всем, кроме...'),
        ('no_one_except', 'не видно никому, кроме...'),
        ('nobody', 'не видно никому')
    ]

    privacy = models.CharField(
        choices=PRIVACIES, default='nobody', blank=True
    )

    class Meta:
        abstract = True


class Topic(AbstractBaseModel):
    title = models.CharField(
        verbose_name='Название темы/раздела знаний',
        max_length=300,
        unique=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class MyKnowledge(MPTTModel, PrivacyBaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_knowledge'
    )

    topic = models.CharField(
        verbose_name='Название темы/раздела знаний',
        max_length=300,
        null=True, blank=True
    )

    published_at = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    is_published = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['created_at']

    class Meta:
        verbose_name = 'Мои знания'
        verbose_name_plural = 'Мои знания'
        # unique_together = ['user', 'topic']
        indexes = [
            models.Index(fields=['privacy']),
            models.Index(fields=['user', 'privacy']),
        ]

    # def delete(self, *args, **kwargs):
    #     if self.is_deleted:
    #         raise NotFound()
    #     self.is_deleted = True
    #     self.deleted_at = timezone.now()
    #     self.save()

    def __str__(self):
        return f"{self.user.username} - {self.topic if self.topic else 'Без темы'}"


class Note(AbstractBaseModel):
    topic = models.OneToOneField(
        MyKnowledge,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='topic_note',
    )

    note = models.TextField(null=True, blank=True)
