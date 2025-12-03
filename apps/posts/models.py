from ast import mod
from django.db import models
from django.utils import timezone

from apps.accounts.models import User


POST_STATUS = [
    ('draft', 'Черновик'),
    ('published', 'Опубликовано'),
    ('archived', 'В архиве'),
]

COMMENT_STATUS = [
    ('pending', 'На модерации'),
    ('approved', 'Одобрено'),
    ('rejected', 'Отклонено'),
    ('deleted', 'Удалено'),
]


def post_images_path(instance, filename):
    """Путь для изображений поста"""
    if instance.post_id:
        return f"post_images/post_{instance.post.id}/{filename}"
    return f"post_images/temp/{filename}"


class BaseModel(models.Model):
    """Абстрактный метод для наследования итерации по полям моделей"""
    class Meta:
        abstract = True

    def __iter__(self):
        for field in self._meta.fields:  # pylint: disable=no-member
            if not field.auto_created:
                yield field.name, getattr(self, field.name)


class PostTag(BaseModel):
    """Модель для хранения уникальных тегов для статей"""
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return str(self.name)


class Post(BaseModel):
    """Основная модель для хранения статей пользователя"""
    title = models.CharField(max_length=200)
    post = models.TextField()
    status = models.CharField(
        max_length=20, choices=POST_STATUS, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        default=None, null=True, blank=True, db_index=True
    )
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    is_blocked = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    tags = models.ManyToManyField(
        PostTag, related_name='posts', blank=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )

    @property
    def is_published(self):
        return self.status == 'published'

    @property
    def short_title(self):
        if len(self.title) > 50:
            return self.title[:47] + '...'
        return self.title

    def save(self, *args, **kwargs):
        # Если статус меняется на published и published_at не установлен
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        # Если статус не published, сбрасываем published_at
        elif self.status != 'published' and self.published_at:
            self.published_at = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    def delete(self, using=None, keep_parents=False):
        """Мягкое удаление"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class PostComment(BaseModel):
    """Модель для хранения комментариев к статьям"""
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='replies'
    )
    status = models.CharField(max_length=20, choices=COMMENT_STATUS)
    comment = models.TextField(
        default="Комментарий по умолчанию для тестирования"
    )
    author = models.ForeignKey(  # добавить автора комментария
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    is_blocked = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий к статье'
        verbose_name_plural = 'Комментарии к статье'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.comment)

    def delete(self, using=None, keep_parents=False):
        """Мягкое удаление"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class PostImage(BaseModel):
    """Модель для хранения изображений встроенных в статьи"""
    image = models.ImageField(
        upload_to=post_images_path, null=True, blank=True
    )
    is_wallpaper = models.BooleanField(default=False, blank=True)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images'
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return str(self.image)
