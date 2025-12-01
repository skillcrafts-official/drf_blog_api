import django_filters

from apps.posts.models import Post


class PostFilters(django_filters.FilterSet):
    author_id = django_filters.NumberFilter(field_name='author_id')
    status = django_filters.CharFilter(field_name='status')
    tag = django_filters.CharFilter(field_name='tags__name')
    created_after = django_filters.DateFilter(
        field_name='created_at', lookup_expr='gte'
    )

    class Meta:
        model = Post
        fields = ['author_id', 'status', 'tag']
