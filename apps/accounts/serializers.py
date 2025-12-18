import hashlib
from typing import Any
import uuid
import jwt
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.conf import settings

from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from apps.accounts.models import GuestConsent, User, GuestUser, Email
from apps.profiles.models import Profile
from apps.privacy_settings.models import ProfilePrivacySettings


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        # fields = '__all__'
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    emails = EmailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'pk', 'primary_email', 'password', 'emails'
        ]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)

        # при регистрации автоматически выбарется как primary_email
        Email.objects.create(
            email=user.primary_email,
            user=user,
            is_confirmed=True,  # временно!!!
            is_active=True
        )
        # автоматически добавляется пустой профиль
        # permissions = ProfilePrivacySettings.objects.create(profile=profile)
        return user

    def create_new_email(self, validated_data):
        email = Email.objects.create(
            email=validated_data['email']
        )
        return email


class EmailConfirmSerializer(serializers.Serializer):
    new_email = serializers.EmailField(write_only=True)
    confirm_code = serializers.CharField(write_only=True)

    def validate_confirm_code(self, confirm_code):
        if confirm_code != 'TESTCODE':
            raise serializers.ValidationError(
                "Неверный код подтверждения"
            )
        return confirm_code

    def update(self, instance, validated_data):
        instance.is_confirmed = True
        instance.save()
        return instance

    def create(self, validated_data):
        pass


class UserPasswordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'user', 'password'
        ]


class UserEmailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Email
        fields = [
            'user', 'email'
        ]


class GuestTokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения гостевого токена"""

    def validate(self, attrs):
        """
        Главный метод валидации, который вызывается при serializer.is_valid()
        """
        return self.create_guest_token()

    def get_current_consent_text(self):
        """Возвращает актуальный текст соглашения"""
        # Можно хранить в БД, файле или settings
        texts = {
            'registration': """
            Я даю согласие на обработку моих персональных данных, 
            предоставляемых в качестве гостя сайта, включая сбор, 
            запись, систематизацию, накопление, хранение, уточнение, 
            извлечение, использование, передачу (распространение, 
            предоставление, доступ), обезличивание, блокирование, 
            удаление, уничтожение персональных данных.
            
            Согласие действует до момента его отзыва.
            Полный текст политики: /privacy-policy
            """
        }
        return texts.get('registration', '')

    def generate_text_hash(self, text):
        """Генерирует хэш текста соглашения"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    # def generate_guest_token(self, guest):
    #     """Генерация access token для гостя"""
    #     from rest_framework_simplejwt.tokens import AccessToken

    #     token = AccessToken()
    #     token['group'] = 'guest'
    #     token['guest_id'] = str(guest.guest_id)
    #     token['type'] = 'guest'
    #     token['permissions'] = ['guest_access']  # Ограниченные права

    #     return token

    # def generate_guest_refresh_token(self, guest):
    #     """Генерация refresh token для гостя"""
    #     from rest_framework_simplejwt.tokens import RefreshToken

    #     refresh = RefreshToken()
    #     refresh['type'] = 'guest'
    #     refresh['guest_id'] = str(guest.guest_id)

    #     return refresh

    def create_guest_token(self):
        """Генерация гостевого токена"""
        request = self.context.get('request')

        if not request:
            raise serializers.ValidationError({
                'detail': 'Request context is required for guest token',
                'code': 'no_request_context'
            })

        # Генерируем уникальный guest_id
        guest_id = str(uuid.uuid4())

        # Создаём или находим гостя
        guest, created = GuestUser.objects.get_or_create(
            guest_uuid=guest_id,
            defaults={
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'ip_address': request.META.get('REMOTE_ADDR', ''),
            }
        )

        # Обновляем активность
        guest.save()

        active_consent = GuestConsent.objects.filter(
            guest=guest,
            is_active=True,
            consent_type='registration'
        ).first()

        if not active_consent:
            # Если согласия нет - создаём новое
            consent_text = self.get_current_consent_text()
            consent_hash = self.generate_text_hash(consent_text)

            guest_consent = GuestConsent.objects.create(
                guest=guest,
                consent_type='registration',
                ip_address=guest.ip_address,
                user_agent=guest.user_agent,
                consent_text_hash=consent_hash,
                # is_active=True по умолчанию
                # withdrawn_at=None по умолчанию
            )

        # Проверяем, не было ли согласие отозвано
        if GuestConsent.objects.filter(
            guest=guest, is_active=False, consent_type='registration'
        ).exists():
            raise serializers.ValidationError({
                'detail': 'Согласие на обработку данных было отозвано',
                'code': 'consent_withdrawn'
            })

        # Генерируем JWT токен для гостя
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken()
        refresh['type'] = 'guest'
        refresh['guest_id'] = str(guest.guest_uuid)
        refresh['group'] = 'guest'
        refresh['permissions'] = ['guest_access']
        refresh['user_id'] = str(guest.guest_uuid)

        # В access токен (ОБЯЗАТЕЛЬНО!)
        refresh.access_token['type'] = 'guest'  # ← И ЭТО ТОЖЕ ВАЖНО!
        refresh.access_token['guest_id'] = str(guest.guest_uuid)
        refresh.access_token['user_id'] = str(guest.guest_uuid)

        # Устанавливаем время жизни
        from datetime import timedelta
        from django.conf import settings

        guest_lifetime = settings.SIMPLE_JWT.get('GUEST_TOKEN_LIFETIME', timedelta(days=30))
        refresh.access_token.set_exp(lifetime=guest_lifetime)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': 'guest',
            'guest_id': str(guest.guest_uuid),
            'user_id': str(guest.guest_uuid),  # Для совместимости
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Добавляем кастомные claims
        token['user_id'] = user.pk
        token['email'] = user.primary_email if hasattr(user, 'primary_email') else user.email
        token['type'] = 'user'  # Тип токена

        if user.is_staff:
            token['group'] = 'admin'
            token['permissions'] = ['full_access']
        else:
            token['group'] = 'user'
            token['permissions'] = ['user_access']
            
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        refresh = self.get_token(self.user)
        
        # Обновляем данные с правильными токенами
        data.update({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': self.user.pk,
            'email': self.user.primary_email if hasattr(self.user, 'primary_email') else self.user.email,
            'group': 'admin' if self.user.is_staff else 'user',
            'user_type': 'user'
        })
        
        return data
