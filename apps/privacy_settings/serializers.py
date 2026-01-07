"""Serializers for $PATH_TO_APP"""
from django.db import transaction

from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.privacy_settings.models import ProfilePrivacySettings
from apps.accounts.models import User


class ProfilePrivacySettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfilePrivacySettings
        # fields = '__all__'
        exclude = ['profile']


class UpdateProfilePrivacySettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfilePrivacySettings
        # fields = '__all__'
        exclude = ['profile', 'blacklist']


class ProfileUserBlockSerializer(serializers.ModelSerializer):
    blocked_user_id = serializers.IntegerField(write_only=True)
    success = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProfilePrivacySettings
        fields = ['blocked_user_id', 'success']

    def update(self, instance, validated_data):
        blocked_user_id = validated_data.get('blocked_user_id', None)

        if blocked_user_id == self.context['request'].user.id:
            raise ValidationError()

        if blocked_user_id is None:
            return instance

        with transaction.atomic():
            user = User.objects.filter(id=blocked_user_id).first()
            if not user:
                return instance

            if not instance.blacklist.filter(id=blocked_user_id).exists():
                instance.blacklist.add(user)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['success'] = True
        return representation


class ProfileUserUnblockSerializer(serializers.ModelSerializer):
    unblocked_user_id = serializers.IntegerField(write_only=True)
    success = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProfilePrivacySettings
        fields = ['unblocked_user_id', 'success']

    def update(self, instance, validated_data):
        unblocked_user_id = validated_data.get('unblocked_user_id', None)

        if unblocked_user_id == self.context['request'].user.id:
            raise ValidationError()

        if unblocked_user_id is None:
            return instance

        with transaction.atomic():
            user = User.objects.filter(id=unblocked_user_id).first()

            if not user:
                return instance

            instance.blacklist.remove(user)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['success'] = True
        return representation


class ProfileUserAddSerializer(serializers.ModelSerializer):
    added_user_id = serializers.IntegerField(write_only=True)
    success = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProfilePrivacySettings
        fields = ['added_user_id', 'success']

    def update(self, instance, validated_data):
        added_user_id = validated_data.get('added_user_id', None)

        if added_user_id == self.context['request'].user.id:
            raise ValidationError()

        if added_user_id is None:
            return instance

        with transaction.atomic():
            user = User.objects.filter(id=added_user_id).first()
            if not user:
                return instance

            if not instance.whitelist.filter(id=added_user_id).exists():
                instance.whitelist.add(user)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['success'] = True
        return representation


class ProfileUserExcludeSerializer(serializers.ModelSerializer):
    excluded_user_id = serializers.IntegerField(write_only=True)
    success = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProfilePrivacySettings
        fields = ['excluded_user_id', 'success']

    def update(self, instance, validated_data):
        excluded_user_id = validated_data.get('excluded_user_id', None)

        if excluded_user_id == self.context['request'].user.id:
            raise ValidationError()

        if excluded_user_id is None:
            return instance

        with transaction.atomic():
            user = User.objects.filter(id=excluded_user_id).first()

            if not user:
                return instance

            instance.whitelist.remove(user)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['success'] = True
        return representation
