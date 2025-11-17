from rest_framework import serializers
from apps.profiles.models import Profile
from apps.accounts.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileImageSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField(source="avatar", read_only=True)
    wallpaper_url = serializers.ImageField(source="wallpaper", read_only=True)

    class Meta:
        model = Profile
        fields = ['avatar_url', 'wallpaper_url']
