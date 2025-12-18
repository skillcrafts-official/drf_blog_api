import uuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class GuestUser(models.Model):
    """Анонимный гость для хранения временных данных"""
    guest_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    user_agent = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    # Связь с будущим пользователем
    migrated_to = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        verbose_name = "Гостевой пользователь"
        verbose_name_plural = "Гостевые пользователи"
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Guest {self.guest_id}"

    @property
    def is_authenticated(self):
        """Всегда возвращает True для аутентификации в DRF"""
        return True

    @property
    def is_anonymous(self):
        """Всегда возвращает False"""
        return False

    # Добавьте метод для получения pk (иногда DRF требует)
    @property
    def pk(self):
        return self.guest_id

    def get_username(self):
        """Возвращает username-подобное значение"""
        return f"guest_{self.guest_id}"


class GuestConsent(models.Model):
    guest = models.ForeignKey(GuestUser, on_delete=models.CASCADE)
    consent_type = models.CharField(max_length=50)  # 'basic', 'cookies', 'marketing'
    given_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    consent_text_hash = models.CharField(max_length=64)  # Хэш текста политики на момент согласия

    # Для GDPR/РКН compliance
    is_active = models.BooleanField(default=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)


class User(AbstractUser):
    user_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = None
    # last_login = None
    # is_superuser = None
    # first_name = None
    # last_name = None
    # is_staff = None
    # is_active = None
    # date_joined = None
    username = None
    primary_email = models.EmailField(unique=True)

    guest_origin = models.ForeignKey(
        GuestUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='migrated_user'
    )

    USERNAME_FIELD = 'primary_email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def active_email(self):
        """Активный email пользователя"""
        try:
            return self.emails.get(is_active=True)
        except Email.DoesNotExist:
            return None

    @property
    def confirmed_emails(self):
        """Все подтвержденные email пользователя"""
        return self.emails.filter(is_confirmed=True)

    def set_active_email(self, email_instance):
        """Установить активный email"""
        if email_instance.user != self:
            raise ValueError("Email does not belong to this user")
        email_instance.is_active = True
        email_instance.save()

    def __iter__(self):
        # для итерации по полям модели User
        for field in self._meta.fields:
            if not field.auto_created:
                yield field.name, getattr(self, field.name)

    def __str__(self):
        return str(self.primary_email)


class Email(models.Model):
    """
    Модель для хранения всех Email,
    когда-либо засветившихся в системе при регистрации или смене
    """
    email = models.EmailField()
    is_confirmed = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="emails"
    )

    class Meta:
        """Мета данные модели"""
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'is_active', 'is_confirmed'],
                name='unique_active_email_per_user',
                condition=models.Q(is_active=True, is_confirmed=True)  # только для подтвержденных email
            ),
            models.UniqueConstraint(
                fields=['user', 'email'],
                name='unique_any_email_per_user'
            )
        ]

    def save(self, *args, **kwargs):
        # Устанавливаем confirmed_at при подтверждении
        if self.is_confirmed and not self.confirmed_at:
            self.confirmed_at = timezone.now()

        # При активации нового email деактивируем старые
        if self.is_active:
            Email.objects.filter(
                user=self.user, is_active=True
            ).update(is_active=False)

        # При получении тот же email от другого пользователя
        # В случае, если он не подтверждён другим пользователем
        # Отдавать этот email новому пользователю
        # Пока кто-нибудь этот email не подтвердит

        super().save(*args, **kwargs)

    def confirm(self):
        """Подтвердить email"""
        self.is_confirmed = True
        self.save()

    def activate(self):
        """Активировать email"""
        self.is_active = True
        self.save()

    @property
    def status(self):
        """Статус email в читаемом формате"""
        if self.is_active and self.is_confirmed:
            return "активный и подтвержденный"
        elif self.is_active:
            return "активный (не подтвержденный)"
        elif self.is_confirmed:
            return "подтвержденный (не активный)"
        else:
            return "не активный"

    def __iter__(self):
        # для итерации по полям модели User
        for field in self._meta.fields:
            if not field.auto_created:
                yield field.name, getattr(self, field.name)

    def __str__(self):
        return f"{self.email} ({self.user})"
