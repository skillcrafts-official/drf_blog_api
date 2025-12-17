from typing import Any
import jwt
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from apps.accounts.models import User, GuestUser, Email
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

    def create_guest_token(self):
        # Создаём или находим гостя
        request = self.context.get('request')

        guest, created = GuestUser.objects.get_or_create(
            session_key=request.session.session_key,
            defaults={
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'ip_address': request.META.get('REMOTE_ADDR', ''),
            }
        )

        # Обновляем активность
        guest.save()

        # Генерируем JWT
        payload = {
            'guest_id': str(guest.guest_id),
            'type': 'guest',
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow(),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token, guest.guest_id, guest.user_agent, guest.ip_address


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        data['user_id'] = self.user.pk

        return data

    @classmethod
    def get_token(cls, user: User) -> Token:
        token = super().get_token(user)

        token['user_id'] = user.pk
        if user.is_staff:
            token['group'] = 'admin'
        else:
            token['group'] = 'user'
            # token['role'] = user.account_type

        return token

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
