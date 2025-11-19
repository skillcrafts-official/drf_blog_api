from apps.CONSTANTS import NOT_AUTHENTICATED, PERMISSION_DENIED

from rest_framework.exceptions import status
from rest_framework import serializers
from drf_spectacular.utils import (
    inline_serializer, extend_schema, extend_schema_view,
    OpenApiExample, OpenApiResponse
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.extensions import OpenApiViewExtension

from apps.profiles.serializers import SelfProfileSerializer, ProfileSerializer


class FixSelfUserProfileView(OpenApiViewExtension):
    """
    Фиксируется документация для SelfUserProfileView
    """
    target_class = 'apps.profiles.views.SelfUserProfileView'

    def view_replacement(self):

        @extend_schema_view(
            get=extend_schema(
                summary="Получить свой профиль",
                description=(
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Только для владельца аккаунта"
                ),
                responses={
                    status.HTTP_200_OK: SelfProfileSerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED
                },
            ),
            post=extend_schema(
                summary="Обновить свой профиль",
                description=(
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Только для владельца аккаунта"
                ),
                responses={
                    status.HTTP_200_OK: inline_serializer(
                        name='ProfileUpdated',
                        fields={
                            'message': serializers.CharField(),
                        }
                    ),
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
                    "**Права:** Только для владельца аккаунта"
                ),
                responses={
                    status.HTTP_204_NO_CONTENT: OpenApiResponse(),
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED
                }
            ),
        )
        # pylint: disable=no-member,inherit-non-class,unnecessary-pass
        class Fixed(self.target_class):
            pass

        return Fixed


class FixUserProfileView(OpenApiViewExtension):
    """
    Фиксируется документация для UserProfileView
    """
    target_class = 'apps.profiles.views.UserProfileView'

    def view_replacement(self):

        @extend_schema_view(
            get=extend_schema(
                summary="Получить чужой профиль",
                description=(
                    "**Требуется аутентификация:** Да  \n"
                    "**Права:** Для авторизованных пользователей"
                ),
                responses={
                    status.HTTP_200_OK: ProfileSerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                },
            )
        )
        # pylint: disable=no-member,inherit-non-class,unnecessary-pass
        class Fixed(self.target_class):
            pass

        return Fixed
