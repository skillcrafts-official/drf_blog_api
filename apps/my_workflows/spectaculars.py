"""The DRF documentation extends for app $PATH_TO_APP"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.my_workflows.serializers import TaskSerializer, CycleTimeSerializer
from apps.CONSTANTS import NOT_AUTHENTICATED, PERMISSION_DENIED, BAD_REQUEST


class FixTaskAPIView(OpenApiViewExtension):
    """
    Расширяется документация для TaskAPIView
    """
    target_class = 'apps.my_workflows.views.TaskAPIView'

    def view_replacement(self) -> type[APIView]:
        @extend_schema_view(
            get=extend_schema(
                summary="Получить список задач",
                description=(
                    "Запрос отдаёт список задач их создателю "
                    "и всем связанным пользователям:  \n  \n "
                    "  - ответственному за её выполнение,  \n "
                    "  - заказчику, запросившему её выполнение,  \n "
                    "  - и всем, кто находится в белом списке её создателя."
                )
            ),
            post=extend_schema(
                summary="Создать задачу",
                description=(
                    "Создать задачу может любой пользователь. "
                    "Также пользователь может управлять её видимостью, "
                    "с помощью поля privacy. По умолчанию, задачу "
                    "не видит никто."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixTaskViewSet(OpenApiViewExtension):
    """
    Расширяется документация для TaskViewSet
    """
    target_class = 'apps.my_workflows.viewsets.TaskViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить задачу",
                description=(
                    "Запрос отдаёт задач по id её создателю "
                    "и всем связанным пользователям:  \n  \n "
                    "  - ответственному за её выполнение,  \n "
                    "  - заказчику, запросившему её выполнение,  \n "
                    "  - и всем, кто находится в белом списке её создателя."
                )
            ),
            partial_update=extend_schema(
                summary="Обновить задачу",
                description=(
                    "Обновление задачи доступно по следующим полям:  \n "
                    "  - status (backlog -> ready -> in progress "
                    "-> review -> done)  \n"
                    "  - privacy (nobody -> no one except -> "
                    "not all -> all  \n  \n"
                    "Список будет расширяться."
                )
            ),
            destroy=extend_schema(
                summary="Удалить задачу",
                description=(
                    "Фактически задача переводится в статус deleted"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixCycleTimeViewSet(OpenApiViewExtension):
    """
    Расширяется документация для CycleTimeViewSet
    """
    target_class = 'apps.my_workflows.viewsets.CycleTimeViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить статистику",
                description=(
                    "Запрос возвращает лог изменений статуса задачи "
                    "с перещётом времени нахождения задачи в каждом статусе."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixAcceptanceCriteriaViewSet(OpenApiViewExtension):
    """
    Расширяется документация для AcceptanceCriteriaViewSet
    """
    target_class = 'apps.my_workflows.viewsets.AcceptanceCriteriaViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить критерии по задаче",
                description=(
                    "Запрос возвращает упорядоченный по возрастанию даты "
                    "список критериев готовности задачи."
                )
            ),
            create=extend_schema(
                summary="Добавить критерий к задаче",
                description=(
                    "Запрос создаёт новый критерий."
                )
            ),
            partial_update=extend_schema(
                summary="Обновить критерий",
                description=(
                    "Запрос обновляет критерий, либо меняя "
                    "смысл, либо состояние."
                )
            ),
            destroy=extend_schema(
                summary="Удалить критерий",
                description=(
                    "Запрос безвозвратно удаляет критерий из БД."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed
