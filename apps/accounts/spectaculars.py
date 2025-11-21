"""Расширение автоматически сгенерированной документации"""
# pylint: disable=no-member,inherit-non-class,unnecessary-pass

from rest_framework.exceptions import status  # type: ignore
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import (
    inline_serializer, extend_schema, extend_schema_view,
    OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.extensions import OpenApiViewExtension

from apps.CONSTANTS import NOT_AUTHENTICATED, PERMISSION_DENIED


class FixUpdateUserEmailView(OpenApiViewExtension):
    """
    Фиксируется документация для UpdateUserEmailView
    """
    target_class = 'apps.accounts.views.UpdateUserEmailView'

    def view_replacement(self) -> type[APIView]:
        @extend_schema_view(
            post=extend_schema(
                summary="Добавить новый email",
                description=(
                    "Добавление нового email адреса для авторизованного "
                    "пользователя.  \n  \n"
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Только для владельца аккаунта"
                ),
                responses={
                    status.HTTP_201_CREATED: inline_serializer(
                        name='EmailCreated',
                        fields={
                            'message': serializers.CharField(),
                        }
                    ),
                    status.HTTP_400_BAD_REQUEST: inline_serializer(
                        name='EmailBadRequest',
                        fields={
                            'message': serializers.CharField(),
                        }
                    ),
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED,
                    status.HTTP_409_CONFLICT: inline_serializer(
                        name='EmailConflict',
                        fields={
                            'message': serializers.CharField()
                        }
                    ),
                },
            )
        )
        # pylint: disable=missing-class-docstring
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixUpdateUserPasswordView(OpenApiViewExtension):
    """
    Фиксируется документация для UpdateUserEmailView
    """
    target_class = 'apps.accounts.views.UpdateUserPasswordView'

    def view_replacement(self) -> type[APIView]:
        @extend_schema_view(
            put=extend_schema(
                summary="Изменить текущий пароль",
                description=(
                    "Изменение пароля для авторизованного "
                    "пользователя.  \n  \n"
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Только для владельца аккаунта"
                ),
                responses={
                    status.HTTP_200_OK: inline_serializer(
                        name='PasswordUpdated',
                        fields={
                            'message': serializers.CharField(),
                        }
                    ),
                    status.HTTP_400_BAD_REQUEST: inline_serializer(
                        name='PasswordValidationError',
                        fields={
                            'message': serializers.CharField(),
                        }
                    ),
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED,
                    status.HTTP_409_CONFLICT: inline_serializer(
                        name='PasswordConflict',
                        fields={
                            'message': serializers.CharField()
                        }
                    ),
                },
            )
        )
        # pylint: disable=missing-class-docstring
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixUserView(OpenApiViewExtension):
    """
    Фиксируется документация для UserView
    """
    target_class = 'apps.accounts.views.UserView'

    def view_replacement(self) -> type[ModelViewSet]:

        @extend_schema_view(
            list=extend_schema(
                summary="Получить всех пользователей",
                description=(
                    "Выдаётся списко всех активных "
                    "подтверждённых пользователей  \n  \n"
                    "**Пока доступно всем, но в будущем только Админам**"
                )
            ),
            retrieve=extend_schema(
                summary="Получить данные пользователя",
                description=(
                    "Получение аутентификационных данных о пользователе  \n  \n"
                    "**Пока доступно всем, но в будущем только Админам**"
                ),
                parameters=[
                    OpenApiParameter(
                       name="id",
                       description="ID пользователя",
                       required=True,
                       type=OpenApiTypes.INT,
                       location=OpenApiParameter.PATH,
                    ),
                ],
            ),
            create=extend_schema(
                summary="Зарегистрировать нового пользователя",
                description=(
                    "Регистрация новых пользователей  \n  \n"
                    "**Публичный метод, доступен всем**"
                )
            )
        )
        # pylint: disable=missing-class-docstring
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixUserConfirmView(OpenApiViewExtension):
    """
    Фиксируется документация для UserConfirmView
    """
    target_class = 'apps.accounts.views.UserConfirmView'

    def view_replacement(self) -> type[ModelViewSet]:

        @extend_schema_view(
            update=extend_schema(
                summary="Подтвердить пользователя",
                description=(
                    "Подтверждение регистрации пользователя "
                    "через код отправленный на указанный Email  \n  \n"
                    "**Публичный метод, доступен всем**"
                ),
                parameters=[
                    OpenApiParameter(
                       name="id",
                       description="ID пользователя",
                       required=True,
                       type=OpenApiTypes.INT,
                       location=OpenApiParameter.PATH,
                    ),
                    OpenApiParameter(
                       name="confirm_code",
                       description="Код подтверждения",
                       required=True,
                       type=OpenApiTypes.STR,
                    ),
                ],
            )
        )
        # pylint: disable=missing-class-docstring
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixMyTokenObtainPairView(OpenApiViewExtension):
    """
    Фиксирует расширение документации для MyTokenObtainPairView
    """
    target_class = 'apps.accounts.views.MyTokenObtainPairView'

    def view_replacement(self) -> type[GenericAPIView]:

        @extend_schema_view(
            post=extend_schema(
                summary="Получить токены",
                description="JWT авторизация пользователя",
                tags=["user_token"]
            )
        )
        # pylint: disable=missing-class-docstring
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixTokenRefreshView(OpenApiViewExtension):
    """
    Фиксирует расширение документации для TokenRefreshView
    """
    target_class = 'rest_framework_simplejwt.views.TokenRefreshView'

    def view_replacement(self) -> type[GenericAPIView]:

        @extend_schema_view(
            post=extend_schema(
                summary="Обновить токены",
                tags=["user_token"]
            )
        )
        # pylint: disable=missing-class-docstring
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixTokenVerifyView(OpenApiViewExtension):
    """
    Фиксирует расширение документации для TokenVerifyView
    """
    target_class = 'rest_framework_simplejwt.views.TokenVerifyView'

    def view_replacement(self) -> type[GenericAPIView]:

        @extend_schema_view(
            post=extend_schema(
                summary="Проверить токены",
                tags=["user_token"]
            )
        )
        # pylint: disable=missing-class-docstring
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed
