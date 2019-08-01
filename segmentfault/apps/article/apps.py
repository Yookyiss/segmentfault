from django.apps import AppConfig


class ArticleConfig(AppConfig):
    name = 'segmentfault.apps.article'
    verbose = '文章'

    def ready(self):
        try:
            import apps.users.signals  # noqa F401
        except ImportError:
            pass

