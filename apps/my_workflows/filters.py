"""The filter extentions for app $PATH_TO_APP"""
import django_filters

from apps.my_workflows.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Task
        fields = ['status']
