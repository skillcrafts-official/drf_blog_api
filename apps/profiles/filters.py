"""The filter extentions for app $PATH_TO_APP"""
import django_filters

from apps.profiles.models import (
    Profile
)


class ProfileFilters(django_filters.FilterSet):
    profile_id = django_filters.NumberFilter(field_name='user_id')

    class Meta:
        model = Profile
        fields = ['profile_id']
