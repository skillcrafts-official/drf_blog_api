from django.apps import AppConfig


class EmailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.emails'

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel,unused-import
            # from apps.accounts import spectaculars  # noqa: F401
            from apps.emails import signals       # noqa: F401
            # from apps.accounts import handlers      # noqa: F401
        except ImportError:
            pass
