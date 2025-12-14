"""Serializers for $PATH_TO_APP"""

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.resume.models import (
    Language, Skill, Summary, WorkExperience, WorkResult, SkillCluster,
    Sertificate,
)


class BaseModelSerializer(serializers.ModelSerializer):
    """Базовый сериализатор"""

    class Meta:
        abstract = True

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop('profile', None)
    #     # Также удаляем другие связанные поля, если нужно
    #     representation.pop('work_experience', None)
    #     return representation
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if getattr(instance, 'work_experience', None):
                if request.user.pk == instance.work_experience.profile.user.pk:
                    return representation
            elif request.user.pk == instance.profile.user.pk:
                return representation
        if representation.get('privacy', None) == 'nobody':
            return {}
        return representation


class WorkResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkResult
        fields = '__all__'
        # exclude = ['work_experience_id']


class SummaryWorkResultSerializer(BaseModelSerializer):

    class Meta:
        model = WorkResult
        fields = '__all__'


# class UpdateWorkResultSerializer(BaseModelSerializer):

#     class Meta:
#         model = WorkResult
#         fields = ['result']


class PrivacyWorkResultSerializer(BaseModelSerializer):

    class Meta:
        model = WorkResult
        fields = ['privacy']


class SummaryWorkExperienceSerializer(BaseModelSerializer):
    results = SummaryWorkResultSerializer(many=True, read_only=True)

    class Meta:
        model = WorkExperience
        fields = '__all__'
        read_only_fields = ('profile', )


class WorkExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkExperience
        fields = '__all__'


class PrivacyWorkExperienceSerializer(BaseModelSerializer):

    class Meta:
        model = WorkExperience
        fields = ['privacy']


class SkillSerializer(BaseModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'


class PrivacySkillSerializer(BaseModelSerializer):

    class Meta:
        model = Skill
        fields = ['privacy']


class SkillClusterSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(
        # many=True, read_only=True, source='profile.skills'
        many=True, read_only=True
    )

    class Meta:
        model = SkillCluster
        fields = '__all__'


class UpdateSkillClusterSerializer(BaseModelSerializer):

    class Meta:
        model = SkillCluster
        fields = '__all__'


class SertificateSerializer(BaseModelSerializer):

    class Meta:
        model = Sertificate
        fields = '__all__'


class UpdateSertificateSerializer(BaseModelSerializer):

    class Meta:
        model = Sertificate
        # fields = '__all__'
        exclude = ['profile']


class PrivacySertificateSerializer(BaseModelSerializer):

    class Meta:
        model = Sertificate
        fields = ['privacy']


class LanguageSerializer(BaseModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class UpdateLanguageSerializer(BaseModelSerializer):

    class Meta:
        model = Language
        fields = ['level']


class PrivacyLanguageSerializer(BaseModelSerializer):

    class Meta:
        model = Language
        fields = ['privacy']


class SummarySerializer(BaseModelSerializer):
    experiences = SummaryWorkExperienceSerializer(
        many=True, read_only=True, source='profile.experiences'
    )
    skills = SkillSerializer(
        many=True, read_only=True, source='profile.skills'
    )
    sertificates = SertificateSerializer(
        many=True, read_only=True, source='profile.certificates'
    )
    languages = LanguageSerializer(
        many=True, read_only=True, source='profile.languages'
    )

    class Meta:
        model = Summary
        fields = '__all__'


class PrivacySummarySerializer(BaseModelSerializer):

    class Meta:
        model = Summary
        fields = ['privacy']
