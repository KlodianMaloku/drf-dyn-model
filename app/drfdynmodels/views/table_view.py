from rest_framework.response import Response
from rest_framework.views import APIView

from drfdynmodels.serializers.createmodel_serializer import ModelSchemaSerializer


class TableAPIView(APIView):

    def post(self, request):
        serializer = ModelSchemaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({"message": f"Table  created successfully"}, status=200)
