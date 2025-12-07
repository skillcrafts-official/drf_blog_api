from django.apps import AppConfig


class PermissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.privacy_settings'
    verbose_name = 'Права, доступы, ограничения'

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel,unused-import
            from apps.privacy_settings import spectaculars  # noqa: F401
        except ImportError:
            pass
