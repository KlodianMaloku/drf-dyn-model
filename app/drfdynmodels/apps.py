from django.apps import AppConfig


class DrfdynmodelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drfdynmodels'

    def ready(self):
        from drfdynmodels.utils import ModelRegistry
        ModelRegistry.load_models_from_db(self.name)