"""The filter extentions for app $PATH_TO_APP"""
import django_filters

from apps.my_workflows.models import Tag, Task


class TaskFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__name')
    status = django_filters.CharFilter(field_name='status')
    tags = django_filters.BaseInFilter(field_name='task_tags__name')

    class Meta:
        model = Task
        fields = ['project', 'status', 'tags']


class TagFilter(django_filters.FilterSet):
    profile = django_filters.CharFilter(field_name='task__profile')
    project = django_filters.CharFilter(field_name='task__project__name')
    status = django_filters.CharFilter(field_name='task__status')

    class Meta:
        model = Tag
        fields = ['profile', 'project', 'status']
