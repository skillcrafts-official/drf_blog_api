"""The DRF documentation extends for app ${PATH_TO_APP}"""
# pylint: disable=no-member,inherit-non-class,unnecessary-pass

from rest_framework.viewsets import ModelViewSet

from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, extend_schema_view


class FixPostTagsView(OpenApiViewExtension):
    """
    Расширяется документация для PostTagsView
    """
    target_class = 'apps.posts.views.PostTagsView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить список тегов",
                description=(
                    "Получение списка всех тегов  \n  \n"
                    "В системе это происходит автоматически, например, "
                    "для проведения лингвистической экспертизы"
                )
            ),
            create=extend_schema(
                summary="Создать уникальный тег",
                description=(
                    "Создание тегов при сохранении или публикации статьи"
                    "  \n  \n"
                    "В системе это происходит автоматически, но администратор "
                    "или автоматическая служба может исправлять ошибки или "
                    "контролировать корректность содержания, например, "
                    "удалять матершиные или любые иные неприличные "
                    "слова и высказывания на лету"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPostsView(OpenApiViewExtension):
    """
    Расширяется документация для PostsView
    """
    target_class = 'apps.posts.views.PostsView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить список статей",
                description=(
                    "Получение списка всех статей в порядке "
                    "убывания даты публикации  \n  \n"
                    "Статьи доступны всем пользователям, включая анонимных "
                    "если статья публичная, и "
                    "только подписчикам, если статья приватная"
                )
            ),
            create=extend_schema(
                summary="Создать статью",
                description=(
                    "Создание статьи с форматированным текстом и вставленными "
                    "изображениями"
                    "  \n  \n"
                    "По умолчанию система сохраняет черновик статьи. "
                    "Но по желанию пользователя статья может быть сразу "
                    "опубликована"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPostView(OpenApiViewExtension):
    """
    Расширяется документация для PostView
    """
    target_class = 'apps.posts.views.PostView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить статью",
                description=(
                    "Получение статьи и всей мета информации о ней "
                    "по уникльному id  \n  \n"
                    "Этот ендпоинт реализует возможность детально "
                    "просматривать выбранную статью "
                    "Просмотр статьи доступны всем пользователям, "
                    "включая анонимных если статья публичная, и "
                    "только подписчикам, если статья приватная"
                )
            ),
            update=extend_schema(
                summary="Изменить статью",
                description=(
                    "Изменение статьи с форматированным текстом "
                    "и вставленными изображениями"
                    "  \n  \n"
                    "По умолчанию изменить статью можно всегда. "
                    "Но по желанию любого авторизованного пользователя "
                    "редактирование "
                    "статьи может быть заблокировано (если этот пользователь "
                    "написал комментарий)"
                )
            ),
            destroy=extend_schema(
                summary="Удалить статью",
                description=(
                    "Удаление статьи происходит мягко, то есть фактически "
                    "статья хранится на сервере "
                    "  \n  \n"
                    "Статью может удалить только её автор или администратор "
                    "или автоматизированная система контроля. "
                    "По умолчанию статью нельзя удалить, если на неё "
                    "написан, хотя бы один комментарий. В этом случае, "
                    "удаление доступно только администраторам"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPostCommentView(OpenApiViewExtension):
    """
    Расширяется документация для PostCommentView
    """
    target_class = 'apps.posts.views.PostCommentView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить комментарий к статье",
                description=(
                    "Получение комментария к статье по "
                    "уникльным id статьи и комментария  \n  \n"
                    "Этот ендпоинт реализует возможность отображения "
                    "комментария в списке комментариев к выбранной статье"
                )
            ),
            update=extend_schema(
                summary="Изменить комментарий",
                description=(
                    "Изменение комментария к статье"
                    "  \n  \n"
                    "По умолчанию изменить комментарий можно всегда. "
                    "Но по желанию любого авторизованного пользователя "
                    "редактирование комментария может быть заблокировано "
                    "(если этот пользователь написал ответный комментарий)"
                )
            ),
            destroy=extend_schema(
                summary="Удалить комментарий",
                description=(
                    "Удаление комментария происходит мягко, то есть фактически "
                    "комментарий хранится на сервере "
                    "  \n  \n"
                    "Комментарий может удалить только её автор или администратор "
                    "или автоматизированная система контроля. "
                    "По умолчанию комментарий нельзя удалить, если на него "
                    "написан, хотя бы один комментарий. В этом случае, "
                    "удаление доступно только администраторам"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPostCommentsView(OpenApiViewExtension):
    """
    Расширяется документация для PostCommentsView
    """
    target_class = 'apps.posts.views.PostCommentsView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить список комментариев",
                description=(
                    "Получение списка всех комментариев в порядке "
                    "убывания даты публикации для выбранной статьи  \n  \n"
                    "Комментарии доступны всем пользователям, включая "
                    "анонимных если статья публичная, и "
                    "только подписчикам, если статья приватная"
                )
            ),
            create=extend_schema(
                summary="Создать комментарий",
                description=(
                    "Создание простого комментария в ответ на статью или "
                    "на другой комментарий этой же статьи"
                    "  \n  \n"
                    "По умолчанию система сохраняет черновик комментария. "
                    "Но по желанию пользователя комментарий может быть сразу "
                    "опубликован"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPostImagesView(OpenApiViewExtension):
    """
    Расширяется документация для PostImagesView
    """
    target_class = 'apps.posts.views.PostImagesView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить список изображений",
                description=(
                    "Получение списка всех изображений, использованных "
                    "в статье  \n  \n"
                    "Это служебный ендпоинт и фактически использутеся "
                    "вместе с ендпоинтами создания и чтения статьей. "
                    "Доступ разрешён только автору статьи"
                )
            ),
            create=extend_schema(
                summary="Добавить изображение",
                description=(
                    "Добавление изображения к списку изображений "
                    "для статьи  \n  \n"
                    "Это служебный ендпоинт и фактически использутеся "
                    "вместе с ендпоинтами создания и чтения статьей. "
                    "Доступ разрешён только автору статьи"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed
