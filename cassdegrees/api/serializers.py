from .models import *
from rest_framework import serializers


# Serialise the contents of the 'Sample' model with fields 'id' and 'text'
class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SampleModel
        fields = ('id', 'text')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseModel
        fields = ([f.name for f in CourseModel._meta.get_fields()])


class SubplanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubplanModel
        fields = ([f.name for f in SubplanModel._meta.get_fields()])
