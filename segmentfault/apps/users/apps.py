from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = "segmentfault.apps.users"
    verbose_name = "用户"

    def ready(self):
        try:
            import apps.users.signals  # noqa F401
        except ImportError:
            pass
