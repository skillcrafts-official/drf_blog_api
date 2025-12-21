import hashlib
from typing import Any
import uuid

import jwt
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.db import models
from django.utils import timezone

from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from apps.accounts.models import GuestConsent, User, GuestUser, Email, UserConsent
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


class EmailConfirmSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['primary_email', 'confirmation_code']

    def validate(self, attrs: Any) -> Any:
        confirmed_email = attrs.pop('primary_email', None)
        confirm_code = attrs.pop('confirmation_code', None)
        print(self.instance.generated_code_at)
        try:
            if not all((
                self.instance.primary_email == confirmed_email,
                self.instance.confirmation_code == confirm_code,
                (timezone.now() - self.instance.generated_code_at) <= timedelta(minutes=60)
            )):
                raise ValidationError(detail='message')
        except Exception as e:
            print(str(e))

        self.instance.email_verified = True

        if self.instance.email_verified:
            raise ValidationError(detail='message')

        self.instance.save()

        return super().validate(attrs)

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


class BaseConsent:
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

    def check_consent(self, ConsentInstance: models.Model, **kwargs):
        active_consent = ConsentInstance.objects.filter(
            is_active=True,
            consent_type='registration',
            **kwargs
        ).first()

        if not active_consent:
            # Если согласия нет - создаём новое
            consent_text = self.get_current_consent_text()
            consent_hash = self.generate_text_hash(consent_text)

            user_params = {
                **kwargs
            }

            if kwargs.get('guest', None):
                user_params.update({
                    'ip_address': kwargs['guest'].ip_address,
                    'user_agent': kwargs['guest'].user_agent
                })

            consent = ConsentInstance.objects.create(
                consent_type='registration',
                consent_text_hash=consent_hash,
                **user_params
                # is_active=True по умолчанию
                # withdrawn_at=None по умолчанию
            )

        # Проверяем, не было ли согласие отозвано
        if ConsentInstance.objects.filter(
            is_active=False, consent_type='registration', **kwargs
        ).exists():
            raise serializers.ValidationError({
                'detail': 'Согласие на обработку данных было отозвано',
                'code': 'consent_withdrawn'
            })


class GuestTokenObtainSerializer(BaseConsent, serializers.Serializer):
    """Сериализатор для получения гостевого токена"""

    def validate(self, attrs):
        """
        Главный метод валидации, который вызывается при serializer.is_valid()
        """
        return self.create_guest_token()

    # def get_current_consent_text(self):
    #     """Возвращает актуальный текст соглашения"""
    #     # Можно хранить в БД, файле или settings
    #     texts = {
    #         'registration': """
    #         Я даю согласие на обработку моих персональных данных, 
    #         предоставляемых в качестве гостя сайта, включая сбор, 
    #         запись, систематизацию, накопление, хранение, уточнение, 
    #         извлечение, использование, передачу (распространение, 
    #         предоставление, доступ), обезличивание, блокирование, 
    #         удаление, уничтожение персональных данных.
            
    #         Согласие действует до момента его отзыва.
    #         Полный текст политики: /privacy-policy
    #         """
    #     }
    #     return texts.get('registration', '')

    # def generate_text_hash(self, text):
    #     """Генерирует хэш текста соглашения"""
    #     return hashlib.sha256(text.encode('utf-8')).hexdigest()

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

        self.check_consent(GuestConsent, guest=guest)
        # active_consent = GuestConsent.objects.filter(
        #     guest=guest,
        #     is_active=True,
        #     consent_type='registration'
        # ).first()

        # if not active_consent:
        #     # Если согласия нет - создаём новое
        #     consent_text = self.get_current_consent_text()
        #     consent_hash = self.generate_text_hash(consent_text)

        #     guest_consent = GuestConsent.objects.create(
        #         guest=guest,
        #         consent_type='registration',
        #         ip_address=guest.ip_address,
        #         user_agent=guest.user_agent,
        #         consent_text_hash=consent_hash,
        #         # is_active=True по умолчанию
        #         # withdrawn_at=None по умолчанию
        #     )

        # # Проверяем, не было ли согласие отозвано
        # if GuestConsent.objects.filter(
        #     guest=guest, is_active=False, consent_type='registration'
        # ).exists():
        #     raise serializers.ValidationError({
        #         'detail': 'Согласие на обработку данных было отозвано',
        #         'code': 'consent_withdrawn'
        #     })

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


class MyTokenObtainPairSerializer(BaseConsent, TokenObtainPairSerializer):

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

        self.check_consent(UserConsent, user=self.user)

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
