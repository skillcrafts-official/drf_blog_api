from rest_framework import serializers
from apps.profiles.models import Profile
from apps.accounts.serializers import UserSerializer


class SelfProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        """Устанавливает user из контекста (request.user)"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileImageSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField(source="avatar", read_only=True)
    wallpaper_url = serializers.ImageField(source="wallpaper", read_only=True)

    class Meta:
        model = Profile
        fields = ['avatar_url', 'wallpaper_url']
