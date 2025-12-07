"""The DRF documentation extends for app ${PATH_TO_APP}"""
# pylint: disable=no-member,inherit-non-class,unnecessary-pass
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.privacy_settings.serializers import (
    ProfilePrivacySettingsSerializer, UpdateProfilePrivacySettingsSerializer,
    ProfileUserBlockSerializer, ProfileUserUnblockSerializer
)
from apps.CONSTANTS import NOT_AUTHENTICATED, PERMISSION_DENIED, BAD_REQUEST


class FixProfilePrivacySettingsView(OpenApiViewExtension):
    """
    Расширяется документация для ProfilePrivacySettingsView
    """
    target_class = 'apps.privacy_settings.views.ProfilePrivacySettingsView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить настройки приватности профиля",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно отобразить чужой профиль  \n  \n"
                    "Данный endpoint возвращает настройки приватности для "
                    "профиля выбранного пользователя  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям  \n"
                    "- **nobody** - не видно никому  \n  \n"
                    "Доступ к настройкам приватности профиля пользователя "
                    "есть у всех авторизованных пользователей"
                ),
                responses={
                    status.HTTP_200_OK: ProfilePrivacySettingsSerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixUpdateProfilePrivacySettingsView(OpenApiViewExtension):
    """
    Расширяется документация для UpdateProfilePrivacySettingsView
    """
    target_class = 'apps.privacy_settings.views.UpdateProfilePrivacySettingsView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            update=extend_schema(
                summary="Изменить настройки приватности профиля",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно изменить настройки приватности "
                    "для отображения своего профиля другим пользователям  \n  \n"
                    "Данный endpoint может устанавливать настройки "
                    "приватности **только для собственного профиля**  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям  \n"
                    "- **nobody** - не видно никому  \n  \n"
                ),
                responses={
                    status.HTTP_200_OK: UpdateProfilePrivacySettingsSerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixProfileUserBlockView(OpenApiViewExtension):
    """
    Расширяется документация для ProfileUserBlockView
    """
    target_class = 'apps.privacy_settings.views.ProfileUserBlockView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            update=extend_schema(
                summary="Заблокировать пользователя",
                description=(
                    "Endpoint добавляет указанного пользователя "
                    "в чёрный список текущего профиля  \n  \n"
                    "Если пользователь заблокирован, то он не может "
                    "просмотривать текущий профиль, "
                    "но может заблокировать в ответ  \n"
                    "Операция блокировки доступна всем авторизованным "
                    "пользователям, но нельзя заблокировать самого себя"
                ),
                responses={
                    status.HTTP_200_OK: ProfileUserBlockSerializer,
                    status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixProfileUserUnblockView(OpenApiViewExtension):
    """
    Расширяется документация для ProfileUserUnblockView
    """
    target_class = 'apps.privacy_settings.views.ProfileUserUnblockView'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            update=extend_schema(
                summary="Разблокировать пользователя",
                description=(
                    "Endpoint удаляет указанного пользователя "
                    "из чёрного списка текущего профиля  \n  \n"
                    "Если пользователь разблокирован, то ему возвращаются "
                    "все прежние права доступа к профилю "
                    "Операция разблокировки доступна всем авторизованным "
                    "пользователям"
                ),
                responses={
                    status.HTTP_200_OK: ProfileUserUnblockSerializer,
                    status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed
