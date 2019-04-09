from .models import *
from rest_framework import serializers


# Serialise the contents of the 'Sample' model with fields 'id' and 'text'
class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SampleModel
        fields = ('id', 'text')

class CoursesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = databaseModel_courses
        fields = ([f.name for f in databaseModel_courses._meta.get_fields()])
