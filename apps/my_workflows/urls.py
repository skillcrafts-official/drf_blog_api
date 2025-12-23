"""The urls routing for app $PATH_TO_APP"""
from django.urls import path

from apps.my_workflows.views import TaskAPIView
from apps.my_workflows.viewsets import TaskViewSet, CycleTimeViewSet


urlpatterns = [
    path(
        'tasks/',
        TaskAPIView.as_view(),
        name='get_all_tasks_or_create_once'
    ),
    path(
        'tasks/<int:pk>/',
        TaskViewSet.as_view({
            'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
        name='rud_user_task'
    ),
    path(
        'tasks/<int:task_id>/statistics/', CycleTimeViewSet.as_view({'get': 'list'}),
        name='all_user_statistics'
    ),
]
