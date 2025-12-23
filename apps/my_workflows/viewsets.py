from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound

from apps.profiles.models import Profile
from apps.privacy_settings.models import ProfilePrivacySettings

from apps.my_workflows.models import Task, CycleTime
from apps.my_workflows.serializers import TaskSerializer, CycleTimeSerializer
from apps.my_workflows.filters import TaskFilter


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    # def retrieve(self, request, *args, **kwargs) -> Response:
    #     user = request.user
    #     user_id = kwargs.get('user_id', None)
    #     profile_id = kwargs.get('profile', None)
    #     if profile_id is None:
    #         profile_id = request.data.get('profile', None)
    #     if user.pk != (user_id if user_id else profile_id):
    #         raise PermissionDenied()
    #     return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs) -> Response:
        user = request.user
        user_id = kwargs.get('user_id', None)
        profile_id = kwargs.get('profile', None)
        if profile_id is None:
            profile_id = request.data.get('profile', None)
        if user.pk != (user_id if user_id else profile_id):
            raise PermissionDenied()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        user = request.user
        user_id = kwargs.get('user_id', None)
        profile_id = kwargs.get('profile', None)
        if profile_id is None:
            profile_id = request.data.get('profile', None)
        if user.pk != (user_id if user_id else profile_id):
            raise PermissionDenied()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs) -> Response:
        user = request.user
        user_id = kwargs.get('user_id', None)
        profile_id = kwargs.get('profile', None)
        if profile_id is None:
            profile_id = request.data.get('profile', None)
        if user.pk != (user_id if user_id else profile_id):
            raise PermissionDenied()
        return super().partial_update(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs) -> Response:
    #     user = request.user
    #     user_id = kwargs.get('user_id', None)
    #     profile_id = kwargs.get('profile', None)
    #     if profile_id is None:
    #         profile_id = request.data.get('profile', None)
    #     if user.pk != (user_id if user_id else profile_id):
    #         raise PermissionDenied()
    #     return super().destroy(request, *args, **kwargs)


class TaskViewSet(BaseModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # filterset_class = TaskFilter

    def get_object(self):
        task = Task.objects.filter(
            profile=self.request.user.pk, **self.kwargs
        ).first()
        if task is None:
            raise NotFound(detail='Task not found!')
        return task

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
