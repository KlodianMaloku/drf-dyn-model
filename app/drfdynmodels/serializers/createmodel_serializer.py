from rest_framework import serializers
from drfdynmodels.models import ModelSchema, FieldSchema


class FieldSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldSchema
        exclude = ('model_schema',)


class ModelSchemaSerializer(serializers.ModelSerializer):
    fields = FieldSchemaSerializer(many=True)

    class Meta:
        model = ModelSchema
        fields = '__all__'

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        model_schema = ModelSchema.objects.create(**validated_data)
        for field_data in fields_data:
            FieldSchema.objects.create(model_schema=model_schema, **field_data)
        return model_schema

    def update(self, instance, validated_data):
        posted_fields = validated_data.pop('fields')
        instance.name = validated_data.get('name', instance.name)
        instance.db_name = validated_data.get('db_name', instance.db_name)
        instance.managed = validated_data.get('managed', instance.managed)
        instance.db_table_name = validated_data.get('db_table_name', instance.db_table_name)
        instance.save()

        existing_fields = instance.fields.all()
        existing_fields = list(existing_fields)

        for posted_field in posted_fields:

            try:
                field = [f for f in existing_fields if f.name == posted_field['name']][0]
                field.name = posted_field.get('name', field.name)
                field.class_name = posted_field.get('class_name', field.class_name)
                field.kwargs = posted_field.get('kwargs', field.kwargs)
                existing_fields.remove(field)
            except IndexError:
                field = FieldSchema.objects.create(
                    model_schema=instance,
                    name=posted_field.get('name'),
                    class_name=posted_field.get('class_name'),
                    kwargs=posted_field.get('kwargs')
                )
            field.save()

        for field in existing_fields:
            field.delete()

        return instance

    def validate(self, attrs):
        fields = attrs.get('fields', [])
        if not fields:
            raise serializers.ValidationError("At least one field must be provided.")
        return attrs
