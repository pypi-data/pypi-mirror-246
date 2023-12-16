from pkg_resources import get_distribution
from django.conf import settings
from extras.plugins import PluginConfig


class StatusPageDemoPluginConfig(PluginConfig):
    name = __package__
    verbose_name = "Status-Page Demo"
    description = "Misc for Status-Page Demo"
    version = get_distribution(__package__).version
    author = "HerrTxbias"
    author_email = "admin@herrtxbias.net"
    base_url = "demo"
    required_settings = []
    default_settings = {}

    def ready(self):
        # https://docs.djangoproject.com/en/4.1/ref/applications/#django.apps.AppConfig.ready
        super().ready()

        # try to get config of plugin by plugin name
        plugin_config = settings.PLUGINS_CONFIG.get(__package__)  # noqa F841

        # do any required init here


config = StatusPageDemoPluginConfig
