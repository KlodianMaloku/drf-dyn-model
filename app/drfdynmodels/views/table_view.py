from rest_framework.response import Response
from rest_framework.views import APIView


class TableAPIView(APIView):

    def post(self, request):
        return Response({"message": f"Table  created successfully"}, status=200)
