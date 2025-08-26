from django.apps import AppConfig
from django.conf import settings
import geoip2.database


class ClickifyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clickify'

    def ready(self):
        if not hasattr(settings, 'GEOIP_PATH'):
            return
        try:
            self.geoip_reader = geoip2.database.Reader(settings.GEOIP_PATH)
        except (FileNotFoundError, ValueError):
            self.geoip_reader = None
