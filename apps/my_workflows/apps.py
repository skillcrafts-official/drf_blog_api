from django.apps import AppConfig


class MyWorkflowsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.my_workflows'

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel,unused-import
            from apps.my_workflows import spectaculars  # noqa: F401
            from apps.my_workflows import signals       # noqa: F401
            from apps.my_workflows import handlers      # noqa: F401
        except ImportError:
            pass
