from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Аккаунты пользователей'

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel,unused-import
            from apps.accounts import spectaculars  # noqa: F401
        except ImportError:
            pass
