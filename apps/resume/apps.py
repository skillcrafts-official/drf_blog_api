from django.apps import AppConfig


class ResumeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.resume'

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel,unused-import
            from apps.resume import spectaculars  # noqa: F401
            # from apps.resume import signals       # noqa: F401
            # from apps.resume import handlers      # noqa: F401
        except ImportError:
            pass
