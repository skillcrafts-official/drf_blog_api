from apps.CONSTANTS import NOT_AUTHENTICATED, PERMISSION_DENIED

from rest_framework.exceptions import (
    status,
    AuthenticationFailed, NotAuthenticated, PermissionDenied
)
from rest_framework import serializers
from drf_spectacular.utils import (
    inline_serializer, extend_schema, extend_schema_view,
    OpenApiExample
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.extensions import OpenApiViewExtension


class FixUpdateUserEmailView(OpenApiViewExtension):
    """
    Фиксируется документация для UpdateUserEmailView
    """
    target_class = 'apps.accounts.views.UpdateUserEmailView'

    def view_replacement(self):
        @extend_schema_view(
            post=extend_schema(
                summary="Добавить новый email",
                description=(
                    "Добавление нового email адреса для авторизованного "
                    "пользователя.  \n  \n"
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Только для владельца аккаунта"
                ),
                # request=UserEmailSerializer,
                # auth=True,
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
                # examples=[
                #     OpenApiExample(
                #         'Пример ошибки 401',
                #         value={'detail': NotAuthenticated.default_detail},  # ✅ Реальное сообщение
                #         response_only=True,
                #         status_codes=['201']
                #     ),
                #     OpenApiExample(
                #         'Пример ошибки 403',
                #         value={'detail': PermissionDenied.default_detail},  # ✅ Реальное сообщение
                #         response_only=True, 
                #         status_codes=['201']
                #     ),
                # ]
            )
        )
        # pylint: disable=no-member,inherit-non-class,unnecessary-pass
        class Fixed(self.target_class):
            pass

        return Fixed


class FixUpdateUserPasswordView(OpenApiViewExtension):
    """
    Фиксируется документация для UpdateUserEmailView
    """
    target_class = 'apps.accounts.views.UpdateUserPasswordView'

    def view_replacement(self):
        @extend_schema_view(
            put=extend_schema(
                summary="Изменить текущий пароль",
                description=(
                    "Изменение пароля для авторизованного "
                    "пользователя.  \n  \n"
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Только для владельца аккаунта"
                ),
                # request=UserEmailSerializer,
                # auth=True,
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
        # pylint: disable=no-member,inherit-non-class,unnecessary-pass
        class Fixed(self.target_class):
            pass

        return Fixed
