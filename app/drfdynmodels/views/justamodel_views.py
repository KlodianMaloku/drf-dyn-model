from rest_framework import viewsets

from drfdynmodels.models import JustAModel
from drfdynmodels.serializers import JustAModelSerializer


class JustAModelViewset(viewsets.ModelViewSet):
    queryset = JustAModel.objects.all()
    serializer_class = JustAModelSerializer