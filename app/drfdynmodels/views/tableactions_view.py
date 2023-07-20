from django.apps import apps
from rest_framework.decorators import action

from rest_framework.response import Response

from rest_framework import viewsets

from drfdynmodels.models import ModelSchema
from drfdynmodels.serializers.dynamic_serializer import create_dynamic_serializer
from drfdynmodels.serializers.createmodel_serializer import ModelSchemaSerializer
from drfdynmodels.models.dynamic_models.config import dynamic_models_app_label


def get_dynamic_model_by_id(id):
    try:
        model_schema = ModelSchema.objects.get(id=id)
        return apps.get_model(dynamic_models_app_label(), model_schema.model_name)
    except ModelSchema.DoesNotExist:
        raise Exception(f"Table {id} does not exist")


def get_serializer_for_dynamic_model_by_id(id):
    try:
        dynamic_model = get_dynamic_model_by_id(id)
        return create_dynamic_serializer(dynamic_model)
    except ModelSchema.DoesNotExist:
        raise Exception(f"Error generating serializer for table {id}")


class TableActionsView(viewsets.ViewSet):

    def put(self, request, id):

        try:
            existing_model = ModelSchema.objects.get(id=id)
            serializer = ModelSchemaSerializer(existing_model, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(existing_model, serializer.validated_data)
            return Response({"message": f"Table {id} updated successfully"}, status=200)
        except ModelSchema.DoesNotExist:
            return Response({"message": f"Table {id} does not exist"}, status=404)

    @action(detail=False, methods=['post'])
    def row(self, request, id):
        try:
            dynamic_serializer = get_serializer_for_dynamic_model_by_id(id)
            serializer = dynamic_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": f"Row added to table {id} successfully"}, status=200)
        except Exception as e:
            return Response({"message": f"Error adding row to table {id}: {e}"}, status=500)

    @action(detail=False, methods=['get'])
    def rows(self, request, id):
        dynamic_serializer = get_serializer_for_dynamic_model_by_id(id)
        requested_model = get_dynamic_model_by_id(id)
        objects = requested_model.objects.all()
        serializer = dynamic_serializer(objects, many=True)
        return Response(serializer.data, status=200)





