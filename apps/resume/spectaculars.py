"""The DRF documentation extends for app ${PATH_TO_APP}"""
# pylint: disable=no-member,inherit-non-class,unnecessary-pass
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.CONSTANTS import NOT_AUTHENTICATED, PERMISSION_DENIED, BAD_REQUEST
from apps.resume.serializers import (
    PrivacySummarySerializer, PrivacyWorkExperienceSerializer,
    PrivacyWorkResultSerializer, PrivacyLanguageSerializer,
    PrivacySertificateSerializer, PrivacySkillSerializer
)


class FixSummaryViewSet(OpenApiViewExtension):
    """
    Расширяется документация для SummaryViewSet
    """
    target_class = 'apps.resume.viewsets.SummaryViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить список резюме",
                description=(
                    "Получение списка резюме с возможностью "
                    "фильтровать по идентификатору профиля.  \n  \n"
                    "Этот ендпоинт возращает всю информацию, "
                    "предоставленную пользователем о своём опыте.  \n"
                    "По умолчанию информация доступна **всем авторизованным** "
                    "пользователям и гостям. Видимость резюме можно "
                    "настраивать также, как профиль пользователя.  \n  \n"
                    "Поиск резюме является служебным действием и в целом, "
                    "пользователю не нужен"
                )
            ),
            create=extend_schema(
                summary="Создать резюме",
                description=(
                    "Создание резюме доступно только зарегистрированным "
                    "пользователям  \n  \n"
                    "Создать можно только одно резюме, точнее открыть его"
                    "сборку. Резюме собирается автоматически на основе "
                    "информации предоставленный в других разделах приложения."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixLanguageViewSet(OpenApiViewExtension):
    """
    Расширяется документация для LanguageViewSet
    """
    target_class = 'apps.resume.viewsets.LanguageViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить список языков",
                description=(
                    "Получение списка языков с возможностью "
                    "фильтровать по идентификатору профиля.  \n  \n"
                    "Этот ендпоинт возращает информацию только о "
                    "языковых возможностях пользователя, которую он "
                    "предоставил.  \n"
                    "По умолчанию информация доступна **всем авторизованным** "
                    "пользователям и гостям. Видимость этого компонента "
                    "резюме можно настраивать отдельно.  \n  \n"
                    "Поиск также является служебным действием"
                )
            ),
            create=extend_schema(
                summary="Добавить язык в резюме",
                description=(
                    "Добавление владения языком в резюме доступно"
                    "только зарегистрированным пользователям  \n  \n"
                    "Добавлять можно множество языков, но каждый язык "
                    "добавить можно только один раз, далее "
                    "можно управлять уровнем его владения."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixUpdateLanguageViewSet(OpenApiViewExtension):
    """
    Расширяется документация для UpdateLanguageViewSet
    """
    target_class = 'apps.resume.viewsets.UpdateLanguageViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            partial_update=extend_schema(
                summary="Изменить уровень",
                description=(
                    "Изменение уровня владения языком  \n  \n"
                    "Этот ендпоинт возращает только изменённую " 
                    "информацию  \n"
                    "Изменение доступно только владельцу аккаунта"
                )
            ),
            destroy=extend_schema(
                summary="Удалить язык",
                description=(
                    "Удаление владение языком из резюме  \n  \n"
                    "Удаление доступно только владельцу аккаунта.  \n  \n"
                    "**ВНИМАНИЕ!!!**  \n Удаление происходит физически, восстановлению "
                    "не подлежит!"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixSertificateViewSet(OpenApiViewExtension):
    """
    Расширяется документация для SertificateViewSet
    """
    target_class = 'apps.resume.viewsets.SertificateViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить список сертификатов",
                description=(
                    "Получение списка сертификатов с возможностью "
                    "фильтровать по идентификатору профиля.  \n  \n"
                    "Этот ендпоинт возращает информацию только о "
                    "сертификатах пользователя, которую он "
                    "предоставил.  \n"
                    "По умолчанию информация доступна **всем авторизованным** "
                    "пользователям и гостям. Видимость этого компонента "
                    "резюме можно настраивать отдельно.  \n  \n"
                    "Поиск является служебным действием"
                )
            ),
            create=extend_schema(
                summary="Добавить сертификат в резюме",
                description=(
                    "Добавление сертификата в резюме доступно"
                    "только зарегистрированным пользователям  \n  \n"
                    "Добавлять можно множество сертификатов, "
                    "далее можно редактировать или удалять сертификаты."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixUpdateSertificateViewSet(OpenApiViewExtension):
    """
    Расширяется документация для UpdateSertificateViewSet
    """
    target_class = 'apps.resume.viewsets.UpdateSertificateViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            partial_update=extend_schema(
                summary="Изменить сертификат",
                description=(
                    "Изменение информации о сертификате  \n  \n"
                    "Изменение доступно только владельцу аккаунта"
                )
            ),
            destroy=extend_schema(
                summary="Удалить сертификат",
                description=(
                    "Удаление сертификата из резюме  \n  \n"
                    "Удаление доступно только владельцу аккаунта.  \n  \n"
                    "**ВНИМАНИЕ!!!**  \n Удаление происходит физически, "
                    "восстановлению не подлежит!"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixSkillClusterViewSet(OpenApiViewExtension):
    """
    Расширяется документация для SkillClusterViewSet
    """
    target_class = 'apps.resume.viewsets.SkillClusterViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить кластеры навыков",
                description=(
                    "Получение списка кластеров  \n  \n"
                    "Этот ендпоинт возращает информацию о всех навыках, "
                    "входящих в кластер и пользователях ими облащающих  \n"
                    "По умолчанию информация доступна **всем авторизованным** "
                    "пользователям и гостям. Видимость этого компонента "
                    "резюме можно настраивать отдельно.  \n  \n"
                    "Поиск является служебным действием"
                )
            ),
            create=extend_schema(
                summary="Добавить новый кластер",
                description=(
                    "Добавление кластера в резюме доступно"
                    "только зарегистрированным пользователям  \n  \n"
                    "Добавлять можно множество кластеров, "
                    "далее их нельзя редактировать и удалять. "
                    "Более того, нельзя создать уже дубликат."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixSkillViewSet(OpenApiViewExtension):
    """
    Расширяется документация для SkillViewSet
    """
    target_class = 'apps.resume.viewsets.SkillViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить список навыков",
                description=(
                    "Получение списка навыков с возможностью "
                    "фильтровать различными спобами.  \n  \n"
                    "Этот ендпоинт возращает информацию о всех навыках, "
                    "всех пользователей или отфильтрованные "
                    "по трёми полям:  \n"
                    "Фильтр по идентификатору пользователя "
                    "`profile_id`  \n"
                    "  - для служебных запросов к API; \n"
                    "  - бесполезно для пользователя. \n  \n"
                    "Фильтр по идентификатору кластера навыков "
                    "`cluster_id`  \n"
                    "  - для служебных запросов к API; \n"
                    "  - бесполезно для пользователя. \n  \n"
                    "Фильтр по названию навыка `skill`  \n"
                    "  - для служебных запросов к API; \n"
                    "  - может быть полезным для пользователя. \n"
                    " \n "
                    "По умолчанию информация доступна **всем авторизованным** "
                    "пользователям и гостям. Видимость этого компонента "
                    "резюме можно настраивать отдельно.  \n"
                )
            ),
            create=extend_schema(
                summary="Добавить новый навык",
                description=(
                    "Добавление навыка в резюме доступно"
                    "только зарегистрированным пользователям  \n  \n"
                    "Добавлять можно множество навыков, "
                    "далее их нельзя редактировать и удалять. "
                    "Более того, нельзя создать дубликат и нельзя "
                    "навык оставить без привязки к кластеру и профилю."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixWorkExperienceViewSet(OpenApiViewExtension):
    """
    Расширяется документация для WorkExperienceViewSet
    """
    target_class = 'apps.resume.viewsets.WorkExperienceViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить места работы",
                description=(
                    "Получение списка работодателей с возможностью "
                    "фильтровать по идентификатору пользователя.  \n  \n"
                    "Этот ендпоинт возращает информацию обо всех "
                    "работодателях с привязкой к работнику.  \n"
                    "**ВНИМАНИЕ!** Не гарантируется "
                    "уникальность работодателей!"
                    "  \n  \n"
                    "По умолчанию информация доступна **всем авторизованным** "
                    "пользователям и гостям. Видимость этого компонента "
                    "резюме можно настраивать отдельно.  \n  \n"
                    "Поиск является служебным действием искать можно "
                    "по нескольким полям:  \n"
                    "- profile_id - по идентификатору пользователя;  \n"
                    "- company - по названию компании;  \n"
                    "- indastry_desc - по описанию индустрии."
                )
            ),
            create=extend_schema(
                summary="Добавить место работы",
                description=(
                    "Добавление места работы в резюме доступно"
                    "только зарегистрированным пользователям  \n  \n"
                    "Добавлять можно множество мест работы, "
                    "далее можно редактировать или удалять их."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixUpdateWorkExperienceViewSet(OpenApiViewExtension):
    """
    Расширяется документация для UpdateWorkExperienceViewSet
    """
    target_class = 'apps.resume.viewsets.UpdateWorkExperienceViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            partial_update=extend_schema(
                summary="Изменить место работы",
                description=(
                    "Изменение информации о месте работы  \n  \n"
                    "Изменение доступно только владельцу аккаунта"
                )
            ),
            destroy=extend_schema(
                summary="Удалить место работы",
                description=(
                    "Удаление места работы из резюме  \n  \n"
                    "Удаление доступно только владельцу аккаунта.  \n  \n"
                    "**ВНИМАНИЕ!!!**  \n Удаление происходит физически, "
                    "восстановлению не подлежит!"
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixWorkResultViewSet(OpenApiViewExtension):
    """
    Расширяется документация для WorkResultViewSet
    """
    target_class = 'apps.resume.viewsets.WorkResultViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            list=extend_schema(
                summary="Получить список рабочих результатов",
                description=(
                    "Получение списка рабочих результатов с возможностью "
                    "фильтровать по идентификатору профиля.  \n  \n"
                    "Этот ендпоинт возращает информацию только о "
                    "рабочих результатов пользователя, которую он "
                    "предоставил и сделал публичным или приватным.  \n"
                    "По умолчанию информация доступна **всем авторизованным** "
                    "пользователям и гостям. Видимость этого компонента "
                    "резюме можно настраивать отдельно.  \n  \n"
                    "Поиск является служебным действием"
                )
            ),
            create=extend_schema(
                summary="Добавить рабочий результат в резюме",
                description=(
                    "Добавление рабочего результата в резюме доступно"
                    "только зарегистрированным пользователям  \n  \n"
                    "Добавлять можно множество рабочих результатов, "
                    "далее можно редактировать или удалять их.  \n  \n"
                    "Пользователь должен быть предупреждён о "
                    "разумном количестве результатов для одного "
                    "места работы и ему должны быть предложены "
                    "лучшие практики формулировки результатов."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixUpdateWorkResultViewSet(OpenApiViewExtension):
    """
    Расширяется документация для UpdateWorkResultViewSet
    """
    target_class = 'apps.resume.viewsets.UpdateWorkResultViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            partial_update=extend_schema(
                summary="Редактировать рабочий результат",
                description=(
                    "Редактирование рабочего результата в резюме  \n  \n"
                    "Редактирование доступно только владельцу аккаунта"
                )
            ),
            destroy=extend_schema(
                summary="Удалить рабочий результат",
                description=(
                    "Удаление рабочего результата из резюме  \n  \n"
                    "Удаление доступно только владельцу аккаунта.  \n  \n"
                    "**ВНИМАНИЕ!!!**  \n Удаление происходит физически, "
                    "восстановлению не подлежит!  \n  \n "
                    "Также надо напоминать пользователю о том, что "
                    "можно настраивать видимость любого блока резюме, "
                    "оставляя возможность для себя не удалять, а скрывать "
                    "информацию."
                )
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPrivacySummaryViewSet(OpenApiViewExtension):
    """
    Расширяется документация для PrivacySummaryViewSet
    """
    target_class = 'apps.resume.viewsets.PrivacySummaryViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить настройки приватности резюме",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно отобразить чужое резюме  \n  \n"
                    "Данный endpoint возвращает настройки приватности для "
                    "выбранного резюме  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                    "Доступ к настройкам приватности резюме пользователя "
                    "есть у всех авторизованных пользователей"
                ),
                responses={
                    status.HTTP_200_OK: PrivacySummarySerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                }
            ),
            update=extend_schema(
                summary="Изменить настройки приватности резюме",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно изменить настройки приватности "
                    "для отображения своего резюме другим пользователям"
                    "  \n  \n"
                    "Данный endpoint может устанавливать настройки "
                    "приватности **только для собственного резюме**  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                ),
                responses={
                    status.HTTP_200_OK: PrivacySummarySerializer,
                    status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPrivacyLanguageViewSet(OpenApiViewExtension):
    """
    Расширяется документация для PrivacyLanguageViewSet
    """
    target_class = 'apps.resume.viewsets.PrivacyLanguageViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить настройки приватности владения языком",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно отобразить чужое резюме  \n  \n"
                    "Данный endpoint возвращает настройки приватности для "
                    "выбранного языка  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                    "Доступ к настройкам приватности владения языками "
                    "есть у всех авторизованных пользователей"
                ),
                responses={
                    status.HTTP_200_OK: PrivacyLanguageSerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                }
            ),
            update=extend_schema(
                summary="Изменить настройки приватности владения языком",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно изменить настройки приватности "
                    "для отображения своего резюме другим пользователям"
                    "  \n  \n"
                    "Данный endpoint может устанавливать настройки "
                    "приватности **только для собственного резюме**  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                ),
                responses={
                    status.HTTP_200_OK: PrivacyLanguageSerializer,
                    status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPrivacySertificateViewSet(OpenApiViewExtension):
    """
    Расширяется документация для PrivacySertificateViewSet
    """
    target_class = 'apps.resume.viewsets.PrivacySertificateViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить настройки приватности сертификатов",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно отобразить чужое резюме  \n  \n"
                    "Данный endpoint возвращает настройки приватности для "
                    "выбранного сертификата  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                    "Доступ к настройкам приватности сертификатов "
                    "есть у всех авторизованных пользователей"
                ),
                responses={
                    status.HTTP_200_OK: PrivacySertificateSerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                }
            ),
            update=extend_schema(
                summary="Изменить настройки приватности сертификатов",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно изменить настройки приватности "
                    "для отображения своих сертификатов другим пользователям"
                    "  \n  \n"
                    "Данный endpoint может устанавливать настройки "
                    "приватности **только для собственного резюме**  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                ),
                responses={
                    status.HTTP_200_OK: PrivacySertificateSerializer,
                    status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPrivacySkillViewSet(OpenApiViewExtension):
    """
    Расширяется документация для PrivacySkillViewSet
    """
    target_class = 'apps.resume.viewsets.PrivacySkillViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить настройки приватности навыков",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно отобразить чужое резюме  \n  \n"
                    "Данный endpoint возвращает настройки приватности для "
                    "выбранного навыка  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                    "Доступ к настройкам приватности навыков "
                    "есть у всех авторизованных пользователей"
                ),
                responses={
                    status.HTTP_200_OK: PrivacySkillSerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                }
            ),
            update=extend_schema(
                summary="Изменить настройки приватности навыков",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно изменить настройки приватности "
                    "для отображения своих навыков другим пользователям"
                    "  \n  \n"
                    "Данный endpoint может устанавливать настройки "
                    "приватности **только для собственного резюме**  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                ),
                responses={
                    status.HTTP_200_OK: PrivacySkillSerializer,
                    status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPrivacyWorkExperienceViewSet(OpenApiViewExtension):
    """
    Расширяется документация для PrivacyWorkExperienceViewSet
    """
    target_class = 'apps.resume.viewsets.PrivacyWorkExperienceViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить настройки приватности места работы",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно отобразить чужое резюме  \n  \n"
                    "Данный endpoint возвращает настройки приватности для "
                    "выбранного места работы  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                    "Доступ к настройкам приватности мест работы "
                    "есть у всех авторизованных пользователей"
                ),
                responses={
                    status.HTTP_200_OK: PrivacyWorkExperienceSerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                }
            ),
            update=extend_schema(
                summary="Изменить настройки приватности места работы",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно изменить настройки приватности "
                    "для отображения своих работодателей другим пользователям"
                    "  \n  \n"
                    "Данный endpoint может устанавливать настройки "
                    "приватности **только для собственного резюме**  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                ),
                responses={
                    status.HTTP_200_OK: PrivacyWorkExperienceSerializer,
                    status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed


class FixPrivacyWorkResultViewSet(OpenApiViewExtension):
    """
    Расширяется документация для PrivacyWorkResultViewSet
    """
    target_class = 'apps.resume.viewsets.PrivacyWorkResultViewSet'

    def view_replacement(self) -> type[ModelViewSet]:
        @extend_schema_view(
            retrieve=extend_schema(
                summary="Получить настройки приватности результатов работы",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно отобразить чужое резюме  \n  \n"
                    "Данный endpoint возвращает настройки приватности для "
                    "выбранного результата работы  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                    "Доступ к настройкам приватности результатов работы "
                    "есть у всех авторизованных пользователей"
                ),
                responses={
                    status.HTTP_200_OK: PrivacyWorkResultSerializer,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                }
            ),
            update=extend_schema(
                summary="Изменить настройки приватности результата работы",
                description=(
                    "Фактически, это служебный endpoint  \n В нём возникает "
                    "потребность, когда нужно изменить настройки приватности "
                    "для отображения своих результатов другим пользователям"
                    "  \n  \n"
                    "Данный endpoint может устанавливать настройки "
                    "приватности **только для собственного резюме**  \n"
                    "- **all** - видно всем пользователям в интернете  \n"
                    "- **not_all** - видно всем авторизованным пользователям"
                    "  \n"
                    "- **nobody** - не видно никому  \n  \n"
                ),
                responses={
                    status.HTTP_200_OK: PrivacyWorkResultSerializer,
                    status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
                    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED,
                    status.HTTP_403_FORBIDDEN: PERMISSION_DENIED,
                }
            )
        )
        class Fixed(self.target_class):  # type: ignore
            pass

        return Fixed
