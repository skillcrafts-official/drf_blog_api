from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.posts'
    verbose_name = 'Статьи пользователей'

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel,unused-import
            from apps.posts import spectaculars  # noqa: F401
        except ImportError:
            pass
