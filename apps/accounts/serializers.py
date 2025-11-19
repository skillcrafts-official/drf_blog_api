from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.accounts.models import User, Email
from apps.profiles.models import Profile


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
        Profile.objects.create(
            user=user
        )
        return user
    
    def create_new_email(self, validated_data):
        email = Email.objects.create(
            email=validated_data['email']
        )
        return email


class UserConfirmSerializer(serializers.Serializer):
    primary_email = serializers.CharField(read_only=True)
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # if user.is_staff:
        #     token['group'] = 'admin'
        # else:
        #     token['group'] = 'user'
        #     token['role'] = user.account_type

        return token

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
