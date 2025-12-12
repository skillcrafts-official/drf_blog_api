from rest_framework import serializers
from rest_framework.exceptions import status  # type: ignore
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import (
    inline_serializer, extend_schema, extend_schema_view,
    OpenApiResponse
)
from drf_spectacular.extensions import OpenApiViewExtension

from apps.profiles.serializers import (
    ProfileSerializer, UpdateProfileSerializer
)

from apps.CONSTANTS import NOT_AUTHENTICATED, PERMISSION_DENIED


class FixUserProfileViewView(OpenApiViewExtension):
    """
    Фиксируется документация для UserProfileView
    """
    target_class = 'apps.profiles.views.UserProfileView'

    def view_replacement(self) -> type[APIView]:

        @extend_schema_view(
            get=extend_schema(
                summary="Получить профиль пользователя",
                description=(
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Для всех авторизованных пользователей"
                ),
                responses={
                    status.HTTP_200_OK: ProfileSerializer,
                    # status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED
                },
            ),
            post=extend_schema(
                summary="Обновить свой профиль",
                description=(
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Только для владельца аккаунта"
                ),
                request=UpdateProfileSerializer,
                responses={
                    status.HTTP_200_OK: UpdateProfileSerializer,
                    status.HTTP_400_BAD_REQUEST: inline_serializer(
                        name='ProfileValidationError',
                        fields={
                            'errors': serializers.ListField(),
                        }
                    ),
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED
                },
            ),
            delete=extend_schema(
                summary="Удалить свой профиль",
                description=(
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Только для владельца аккаунта или "
                    "администратора"
                ),
                responses={
                    status.HTTP_204_NO_CONTENT: OpenApiResponse(),
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED
                }
            ),
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixRussianEduLevelView(OpenApiViewExtension):
    """
    Расширяется документация для RussianEduLevelView
    """
    target_class = 'apps.profiles.viewsets.RussianEduLevelView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить уровень образования",
                description=(
                    "Получение уровня образования пользователя.  \n  \n"
                    "Этот ендпоинт возращает информацию только об "
                    "уровне образования для компонентов фронтенда "
                    "типа MultiCheckBox.  \n"
                    "По умолчанию информация доступна **всем авторизованным** "
                    "пользователям и гостям. Видимость этого компонента "
                    "профиля и резюме можно настраивать отдельно."
                )
            ),
            partial_update=extend_schema(
                summary="Изменить уровень образования",
                description=(
                    "Изменение уровня образования  \n  \n"
                    "Изменение доступно только владельцу аккаунта и "
                    "только из специального компонента фронтенда "
                    "типа MultiCheckBox"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixWorkFormatView(OpenApiViewExtension):
    """
    Расширяется документация для WorkFormatView
    """
    target_class = 'apps.profiles.viewsets.WorkFormatView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить список форматов работы",
                description=(
                    "Получение списка препочитаемых форматов работы.  \n  \n"
                    "Этот ендпоинт возращает информацию только о "
                    "предпочтениях для компонентов фронтенда "
                    "типа SimpleCheckBox.  \n"
                    "По умолчанию информация доступна **всем авторизованным** "
                    "пользователям и гостям. Видимость этого компонента "
                    "профиля и резюме можно настраивать отдельно."
                )
            ),
            partial_update=extend_schema(
                summary="Изменить список форматов работы",
                description=(
                    "Изменение списка форматов работы  \n  \n"
                    "Изменение доступно только владельцу аккаунта и "
                    "только из специального компонента фронтенда "
                    "типа SimpleCheckBox"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed
