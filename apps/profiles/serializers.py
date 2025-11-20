from rest_framework import serializers
from apps.profiles.models import Profile
from apps.accounts.serializers import UserSerializer


class SelfProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выдачи полной информации о пользователе
    (модели User, Email и Profile) в контексте авторизованного пользователя
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        """Устанавливает user из контекста (request.user)"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выдачи профиля пользователя
    по запросу авторизованного пользователя
    """
    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = self.context.get('user_id')

    @property
    def data(self):
        """
        Выдает данные сериализатора по параметру пути user_id
        Если профиля нет, то выбрасывает исключение NotFound
        """
        if self.user_id is not None:
            self.instance = Profile.objects.filter(
                user_id=self.user_id).first()
            if self.instance is None:
                raise serializers.ValidationError("Profile not found")
        return super().data


class ProfileImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления всего медиа-контента
    в контексте авторизованного пользователя
    """
    avatar_url = serializers.ImageField(source="avatar", read_only=True)
    wallpaper_url = serializers.ImageField(source="wallpaper", read_only=True)

    class Meta:
        model = Profile
        fields = ['avatar_url', 'wallpaper_url']
