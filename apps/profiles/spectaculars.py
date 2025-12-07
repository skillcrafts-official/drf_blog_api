from rest_framework import serializers
from rest_framework.exceptions import status  # type: ignore
from rest_framework.views import APIView

from drf_spectacular.utils import (
    inline_serializer, extend_schema, extend_schema_view,
    OpenApiResponse
)
from drf_spectacular.extensions import OpenApiViewExtension

from apps.profiles.serializers import (
    ProfileSerializer, UpdateProfileSerializer
)

from apps.CONSTANTS import NOT_AUTHENTICATED, PERMISSION_DENIED


class FixUserProfileView(OpenApiViewExtension):
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
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixUpdateUserProfileView(OpenApiViewExtension):
    """
    Фиксируется документация для UpdateUserProfileView
    """
    target_class = 'apps.profiles.views.UpdateUserProfileView'

    def view_replacement(self) -> type[APIView]:

        @extend_schema_view(
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
