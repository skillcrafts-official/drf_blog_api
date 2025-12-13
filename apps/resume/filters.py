"""The filter extentions for app $PATH_TO_APP"""
import django_filters

from apps.resume.models import (
    Summary, WorkExperience, Language, Sertificate, SkillCluster, Skill,
    WorkResult
)


class SummaryFilters(django_filters.FilterSet):
    profile_id = django_filters.NumberFilter(field_name='profile_id')

    class Meta:
        model = Summary
        fields = ['profile_id']


class LanguageFilters(django_filters.FilterSet):
    profile_id = django_filters.NumberFilter(field_name='profile_id')

    class Meta:
        model = Language
        fields = ['profile_id']


class SertificateFilters(django_filters.FilterSet):
    profile_id = django_filters.NumberFilter(field_name='profile_id')

    class Meta:
        model = Sertificate
        fields = ['profile_id']


class SkillClusterFilters(django_filters.FilterSet):
    skill_cluster = django_filters.CharFilter(field_name='cluster_name')

    class Meta:
        model = SkillCluster
        fields = ['skill_cluster']


class SkillFilters(django_filters.FilterSet):
    profile_id = django_filters.NumberFilter(field_name='profile_id')
    cluster_id = django_filters.NumberFilter(field_name='cluster_id')
    skill = django_filters.CharFilter(field_name='skill_name')

    class Meta:
        model = Skill
        fields = ['profile_id', 'cluster_id', 'skill']


class WorkExperienceFilters(django_filters.FilterSet):
    profile_id = django_filters.NumberFilter(field_name='profile_id')
    company = django_filters.CharFilter(field_name='company')
    industry_desc = django_filters.CharFilter(field_name='indastry_desc')

    class Meta:
        model = WorkExperience
        fields = ['profile_id', 'company', 'industry_desc']


class WorkResultFilters(django_filters.FilterSet):
    result_id = django_filters.NumberFilter(field_name='id')
    experience_id = django_filters.NumberFilter(field_name='work_experience_id')

    class Meta:
        model = WorkResult
        fields = ['result_id', 'experience_id']
