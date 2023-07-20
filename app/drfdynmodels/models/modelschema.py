from django.db import models
from django.db.utils import DEFAULT_DB_ALIAS
from django.utils.text import slugify

from drfdynmodels.models.dynamic_models import  config
from drfdynmodels.models.dynamic_models.factory import ModelFactory
from drfdynmodels.models.dynamic_models.schema import  ModelSchemaEditor
from drfdynmodels.utils import ModelRegistry


class ModelSchema(models.Model):
    name = models.CharField(max_length=250, unique=True)
    db_name = models.CharField(max_length=32, default=DEFAULT_DB_ALIAS)
    managed = models.BooleanField(default=True)
    db_table_name = models.CharField(max_length=250, blank=False, null=False,
                                     help_text="This field can not be blank or null")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry = ModelRegistry(self.app_label)
        self._initial_name = self.name
        initial_model = self.get_registered_model()
        self._schema_editor = (
            ModelSchemaEditor(initial_model=initial_model, db_name=self.db_name)
            if self.managed
            else None
        )

    def save(self, **kwargs):
        super().save(**kwargs)
        if self._schema_editor:
            created, model = self._schema_editor.update_table(self._factory.get_model())
            if created:
                self._registry.register_model(self._registry.get_model(self.model_name))
        self._initial_name = self.name

    def delete(self, **kwargs):
        if self._schema_editor:
            self._schema_editor.drop_table(self.as_model())
        self._factory.destroy_model()
        super().delete(**kwargs)

    def get_registered_model(self):
        return self._registry.get_model(self.model_name)

    @property
    def _factory(self):
        return ModelFactory(self)

    @property
    def app_label(self):
        return config.dynamic_models_app_label()

    @property
    def model_name(self):
        return self.get_model_name(self.name)

    @property
    def initial_model_name(self):
        return self.get_model_name(self._initial_name)

    @classmethod
    def get_model_name(cls, name):
        return name.title().replace(" ", "")

    @property
    def db_table(self):
        return self.db_table_name if self.db_table_name else self._default_db_table_name()

    def _default_db_table_name(self):
        safe_name = slugify(self.name).replace("-", "_")
        return f"{self.app_label}_{safe_name}"

    def as_model(self):
        return self._factory.get_model()

