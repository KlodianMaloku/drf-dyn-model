from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db import models
from django.utils.text import slugify

from drfdynmodels.models.dynamic_models import compat
from drfdynmodels.models.dynamic_models.exceptions import InvalidFieldNameError, NullFieldChangedError
from drfdynmodels.models.dynamic_models.schema import FieldSchemaEditor
from drfdynmodels.models.modelschema import ModelSchema


class FieldKwargsJSON(compat.JSONField):
    description = "A field that handles storing models.Field kwargs as JSON"

    def to_python(self, value):
        raw_value = super().to_python(value)
        try:
            return self._convert_on_delete_to_function(raw_value)
        except AttributeError as err:
            raise ValidationError("Invalid value for 'on_delete'") from err

    def from_db_value(self, value, expression, connection):
        # django.contrib.postgres.fields.JSONField does not implement from_db_value
        # for some reason. In that version, value is already a dict
        try:
            db_value = super().from_db_value(value, expression, connection)
        except AttributeError:
            db_value = value
        return self._convert_on_delete_to_function(db_value)

    def get_prep_value(self, value):
        prep_value = self._convert_on_delete_to_string(value)
        return super().get_prep_value(prep_value)

    def _convert_on_delete_to_function(self, raw_value):
        if raw_value is None or "on_delete" not in raw_value:
            return raw_value

        raw_on_delete = raw_value["on_delete"]
        if isinstance(raw_on_delete, str):
            raw_value["on_delete"] = getattr(models, raw_on_delete)

        return raw_value

    def _convert_on_delete_to_string(self, raw_value):
        if raw_value is None or "on_delete" not in raw_value:
            return raw_value

        raw_on_delete = raw_value["on_delete"]
        if callable(raw_on_delete):
            raw_value["on_delete"] = raw_on_delete.__name__

        return raw_value


class FieldSchema(models.Model):
    _PROHIBITED_NAMES = ("__module__", "_declared")

    name = models.CharField(max_length=63, null=False, blank=False)
    model_schema = models.ForeignKey(ModelSchema, on_delete=models.CASCADE, related_name="fields")
    class_name = models.TextField(null=False, blank=False)
    kwargs = FieldKwargsJSON(default=dict)

    class Meta:
        unique_together = (("name", "model_schema"),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_name = self.name
        self._initial_field = self.get_registered_model_field()
        self._schema_editor = (
            FieldSchemaEditor(initial_field=self._initial_field, db_name=self.model_schema.db_name)
            if self.model_schema.managed
            else None
        )
        self._initial_null = self.null

    def save(self, **kwargs):
        self.validate()
        super().save(**kwargs)
        model, field = self._get_model_with_field()
        if self._schema_editor:
            self._schema_editor.update_column(model, field)

    def delete(self, **kwargs):
        model, field = self._get_model_with_field()
        if self._schema_editor:
            self._schema_editor.drop_column(model, field)
        super().delete(**kwargs)

    def validate(self):
        if self._initial_null and not self.null:
            raise NullFieldChangedError(f"Cannot change NULL field '{self.name}' to NOT NULL")

        if self.name in self.get_prohibited_names():
            raise InvalidFieldNameError(f"{self.name} is not a valid field name")

    def get_registered_model_field(self):
        latest_model = self.model_schema.get_registered_model()
        if latest_model and self.name:
            try:
                return latest_model._meta.get_field(self.name.lower().replace(" ", "_"))
            except FieldDoesNotExist:
                pass

    @classmethod
    def get_prohibited_names(cls):
        # TODO: return prohbited names based on backend
        return cls._PROHIBITED_NAMES

    @property
    def db_column(self):
        return slugify(self.name).replace("-", "_")

    @property
    def null(self):
        return self.kwargs.get("null", False)

    @null.setter
    def null(self, value):
        self.kwargs["null"] = value

    def get_options(self):
        return self.kwargs.copy()

    def _get_model_with_field(self):
        model = self.model_schema.as_model()
        try:
            field = model._meta.get_field(self.db_column)
        except FieldDoesNotExist:
            field = None
        return model, field
