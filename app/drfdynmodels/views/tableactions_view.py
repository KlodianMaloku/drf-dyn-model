from django.db import models
from django.apps import apps
from django.db import connection

from rest_framework.response import Response
from rest_framework.views import APIView

from drfdynmodels.serializers.dynamic_serializer import create_dynamic_serializer


class UpdateTableAPIView(APIView):
    def put(self, request, id):
        # TODO: Impelement this
        return Response({"message": f"Table {id} updated successfully"}, status=200)


class TableRowAPIView(APIView):
    def post(self, request, id):
        # TODO: Check if table exists
        # TODO: Get appname from apps.py
        DynamicModel = apps.get_model('drfdynmodels', 'table_name')

        # Create the serializer
        DynamicModelSerializer = create_dynamic_serializer(DynamicModel)
        serializer = DynamicModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": f"Row added to table {id} successfully"}, status=200)


class TableRowsAPIView(APIView):
    def post(self, request, id):
        # TODO: Impelement this
        pass


