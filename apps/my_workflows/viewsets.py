from math import radians
from typing import Sequence
from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound

from apps.profiles.models import Profile
from apps.privacy_settings.models import ProfilePrivacySettings

from apps.my_workflows.models import AcceptanceCriteria, Task, CycleTime
from apps.my_workflows.serializers import (
    TaskSerializer, CycleTimeSerializer, AcceptanceCriteriaSerializer
)
from apps.my_workflows.filters import TaskFilter


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class TaskViewSet(BaseModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    def get_object(self):
        task = Task.objects.filter(
            profile=self.request.user.pk, pk=self.kwargs['task_id']
        ).first()
        if task is None:
            raise NotFound(detail='Task not found!')
        return task

    def get_queryset(self):
        queryset = Task.objects.filter(profile__user=self.request.user)
        return queryset

    def destroy(self, request, *args, **kwargs) -> Response:
        user = request.user

        try:
            task = Task.objects.get(**kwargs)
        except Task.DoesNotExist:
            raise NotFound()

        if task is None or task.profile is None: 
            raise NotFound()

        if user and (user.pk != task.profile.user.pk):
            raise PermissionDenied()

        task.status = 'deleted'
        task.save()

        return Response(status=204)


class CycleTimeViewSet(BaseModelViewSet):
    queryset = CycleTime.objects.all()
    serializer_class = CycleTimeSerializer

    def get_queryset(self) -> QuerySet:
        statistic = CycleTime.objects.filter(
            task__profile=self.request.user.pk, task_id=self.kwargs['task_id']
        )
        # print(statistic.pk)
        if statistic is None:
            raise NotFound(detail='Statistic not found!')
        return statistic


class AcceptanceCriteriaViewSet(BaseModelViewSet):
    queryset = AcceptanceCriteria.objects.all()
    serializer_class = AcceptanceCriteriaSerializer

    def get_object(self):
        criteria = AcceptanceCriteria.objects.filter(
            pk=self.kwargs['criteria_id']
        ).first()
        if criteria is None:
            raise NotFound(detail='Task not found!')
        return criteria

    def check_permissions(self, request) -> None:
        user = request.user
        method = request.method

        print('im here!')

        if method not in ('GET', 'POST',):
            criteria_id = self.kwargs.get('criteria_id', None)
            if criteria_id is None:
                print('im there!')
                raise NotFound()

            try:
                criteria = AcceptanceCriteria.objects.get(pk=criteria_id)
            except AcceptanceCriteria.DoesNotExist:
                print('im there!')
                raise NotFound()

            if criteria.task.profile is None:
                print('im there!')
                raise NotFound()

            if user.pk != criteria.task.profile.user.pk:
                print('im there!')
                raise PermissionDenied()
        print('im there!')

        task_id = self.kwargs.get('task_id', None)
        if task_id is None:
            raise NotFound()

        request.data['task'] = task_id

        return super().check_permissions(request)

    def create(self, request, *args, **kwargs) -> Response:

        return super().create(request, *args, **kwargs)
