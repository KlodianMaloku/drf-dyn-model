from django.contrib import admin

# Register your models here.

from drfdynmodels.models import ModelSchema, FieldSchema

admin.site.register(ModelSchema)
admin.site.register(FieldSchema)
