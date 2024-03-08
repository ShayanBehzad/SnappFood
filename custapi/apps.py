from django.apps import AppConfig

import custapi


class CustapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "custapi"

    def ready(self):
        import custapi.signals
