"""The viewsets extentions for app my_knowledge"""

from typing import Any
from django.db import transaction
from django.db.models import Q
from django.db.models.query import QuerySet
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.serializers import BaseSerializer
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.my_knowledge.models import MyKnowledge, Topic
from apps.my_knowledge.serializers import MyKnowledgeSerializer, TopicSerializer


class TopicViewSet(viewsets.ModelViewSet):
    """
    Представление для отображения всего списка топиков
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class MyKnowledgeViewSet(viewsets.ModelViewSet):
    """
    Представление для отображения списка заметок
    конкретного пользователя (можно видеть как свои заметки,
    так и заметки тех, кто открыл к ним доступ)
    """
    queryset = MyKnowledge.objects.all()
    serializer_class = MyKnowledgeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Any:
        note = MyKnowledge.objects.filter(
            user=self.request.user, id=self.kwargs['note_id']
        ).first()
        if note is None:
            raise NotFound()
        return note

    def get_queryset(self) -> QuerySet:
        # Получаем whitelist и blacklist текущего пользователя
        current_user = self.request.user

        try:
            my_whitelist = current_user.profile.profile_privacies.whitelist.all()
            my_blacklist = current_user.profile.profile_privacies.blacklist.all()
        except (Profile.DoesNotExist, ProfilePrivacySettings.DoesNotExist):
            my_whitelist = User.objects.none()
            my_blacklist = User.objects.none()

        # при создании filter_conditions отвечается на вопрос:
        # Какие записи я (current_user) буду видеть
        filter_conditions = Q()

        # при создании exclude_conditions отвечаем на вопрос: 
        # Какие записи я (current_user) НЕ буду видеть
        exclude_conditions = Q()

        # 1. Я вижу все свои записи + неопубликованные + удалённые
        filter_conditions |= Q(user=current_user)

        # 2. Я не вижу все записи пользователей из моего blacklist
        if my_blacklist.exists():
            exclude_conditions |= Q(user__in=my_blacklist)

        # 3. Я вижу все публичные записи
        filter_conditions |= Q(privacy__in=['all', 'not_all'])

        # # 4. Я не вижу публичные записи, если я в blacklist автора записи
        exclude_conditions |= Q(
            privacy='not_all',
            user__profile__profile_privacies__blacklist=current_user
        )

        # 5. Я вижу приватные записи, если я в whitelist автора записи
        filter_conditions |= Q(
            privacy='no_one_except',
            user__profile__profile_privacies__whitelist=current_user
        )

        # 6. Я не вижу все приватные записи nobody
        # exclude_conditions |= Q(Q(privacy='nobody') & Q(user!=current_user))

        # 6.5. Я не вижу все неопубликованные и удалённые записи
        exclude_conditions |= (
            ~Q(user=current_user) &
            (Q(is_published=False) | Q(is_deleted=True))
        )

        # Запрос знаний
        queryset = (
            MyKnowledge.objects
            .filter(filter_conditions)
            .exclude(exclude_conditions)
            .select_related('user').select_related('parent')
            .distinct()
        )

        return queryset

    # def check_permissions(self, request: Request) -> None:
    #     if request.method == 'GET':

    #     return super().check_permissions(request)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Кастомизация метода нужна, чтобы автоматически создавать
        топик в своей модели, если было передано поле topic.
        В противном случае создавать запись без топика.
        """
        # request_data = request.data.copy()

        # if 'topic' not in request_data:
        #     # request.data.update(**request_data)
        #     return super().create(request, *args, **kwargs)

        # if not request_data.get('topic'):
        #     request_data.pop('topic')
        #     request.data.update(**request_data)
        #     return super().create(request, *args, **kwargs)

        # topic_value = request_data.get('topic').strip()
        # topic = None

        # if isinstance(topic_value, str):
        #     topic, _ = Topic.objects.get_or_create(title__iexact=topic_value)
        # elif isinstance(topic_value, int):
        #     try:
        #         topic = Topic.objects.get(pk=topic_value)
        #     except Topic.DoesNotExist:
        #         raise NotFound()

        # # if not topic:
        # #     topic = Topic.objects.create(title=topic_value)

        # request_data['topic'] = topic.pk
        # request.data.update(**request_data)
        return super().create(request, *args, **kwargs)
