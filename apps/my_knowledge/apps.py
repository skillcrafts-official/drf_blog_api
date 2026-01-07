from django.apps import AppConfig


class MyKnowledgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.my_knowledge'

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel,unused-import
            from apps.my_knowledge import spectaculars  # noqa: F401
            # from apps.my_knowledge import signals       # noqa: F401
            # from apps.my_knowledge import handlers      # noqa: F401
        except ImportError:
            pass
