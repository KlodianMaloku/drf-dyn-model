from rest_framework import serializers
from drfdynmodels.models import JustAModel


class JustAModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JustAModel
        fields = '__all__'