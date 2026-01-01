"""The filter extentions for app $PATH_TO_APP"""
import django_filters

from apps.my_workflows.models import Tag, Task


class TaskFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__name')
    status = django_filters.CharFilter(field_name='status')
    tags = django_filters.MultipleChoiceFilter(
        field_name='task_tags__name', conjoined=True
    )

    class Meta:
        model = Task
        fields = ['project', 'status', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Динамически заполняем choices для тегов
        request = kwargs.get('request', None)
        if request and request.user.is_authenticated:
            # Получаем все теги пользователя
            user_tags = Tag.objects.filter(
                profile=request.user.profile
            ).values_list('name', flat=True).distinct()

            # Создаем choices
            tag_choices = [(tag, tag) for tag in user_tags]
            self.filters['tags'].extra['choices'] = tag_choices


class TagFilter(django_filters.FilterSet):
    profile = django_filters.CharFilter(field_name='task__profile')
    project = django_filters.CharFilter(field_name='task__project__name')
    status = django_filters.CharFilter(field_name='task__status')

    class Meta:
        model = Tag
        fields = ['profile', 'project', 'status']
