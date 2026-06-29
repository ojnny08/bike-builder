from django.apps import AppConfig


class ComponentsConfig(AppConfig):
    name = 'apps.components'

    def ready(self):
        from . import signal  # noqa: F401  connects cache-refresh receivers
