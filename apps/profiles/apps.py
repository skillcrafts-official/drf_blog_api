from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.profiles'
    verbose_name = 'Профили пользователей'

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel,unused-import
            from apps.profiles import spectaculars  # noqa: F401
        except ImportError:
            pass
