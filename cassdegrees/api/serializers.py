from .models import SampleModel
from rest_framework import serializers


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SampleModel
        fields = ('id', 'text')
