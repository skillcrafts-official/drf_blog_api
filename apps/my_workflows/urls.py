"""The urls routing for app $PATH_TO_APP"""
from django.urls import path

from apps.my_workflows.views import TaskAPIView
from apps.my_workflows.viewsets import (
    ProjectViewSet, TagViewSet, TaskViewSet, TagsViewSet, CycleTimeViewSet,
    AcceptanceCriteriaViewSet, TimeEntryViewSet, TaskProjectViewSet
)


urlpatterns = [
    path(
        'projects/',
        ProjectViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='get_all_user_projects_or_creane_else'
    ),
    path(
        'tasks/',
        TaskViewSet.as_view({'get': 'list', 'post': 'create'}),
        # TaskAPIView.as_view(),
        name='get_all_tasks_or_create_once'
    ),
    path(
        'tasks/<int:task_id>/',
        TaskViewSet.as_view({
            'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
        name='rud_user_task'
    ),
    path(
        'tasks/<int:task_id>/projects/',
        TaskProjectViewSet.as_view({'patch': 'partial_update'}),
        name='rud_user_task'
    ),
    path(
        'tasks/<int:task_id>/statistics/', CycleTimeViewSet.as_view({'get': 'list'}),
        name='all_user_statistics'
    ),
    path(
        'tasks/<int:task_id>/acceptance-criterias/',
        AcceptanceCriteriaViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='criterias_update'
    ),
    path(
        'tasks/<int:task_id>/acceptance-criterias/<int:criteria_id>/',
        AcceptanceCriteriaViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'}),
        name='criterias_update'
    ),
    path(
        'tasks/<int:task_id>/hours-spents/',
        TimeEntryViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='time_entries_update'
    ),
    path(
        'tasks/tags/',
        TagsViewSet.as_view({'get': 'list'}),
        name='filtered_tag_list'
    ),
    path(
        'tasks/<int:task_id>/tags/',
        TagViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='task_tags'
    )
]
