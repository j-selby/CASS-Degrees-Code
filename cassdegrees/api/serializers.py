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
        fields = ('id', 'code', 'year', 'name', 'units', 'offeredSem1', 'offeredSem2')#([f.name for f in CourseModel._meta.get_fields()])
        lookup_field = 'id'


class SubplanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubplanModel
        fields = ('id', 'code', 'year', 'name', 'units', 'planType')#([f.name for f in SubplanModel._meta.get_fields()])
        lookup_field = 'id'


class CourseIDSerializer(serializers.PrimaryKeyRelatedField):
    class Meta:
        model = CourseModel
        fields = ['id', 'code']
        many = True
        read_only = False
        queryset = CourseModel.objects.all()


class SubplanIDSerializer(serializers.PrimaryKeyRelatedField):
    class Meta:
        model = SubplanModel
        fields = ['id', 'code']
        many = True
        read_only = False
        queryset = SubplanModel.objects.all()


class CoursesInSubplanSerializer(serializers.HyperlinkedModelSerializer):
    courseId = CourseIDSerializer(queryset = CourseModel.objects.all())
    subplanId = SubplanIDSerializer(queryset = SubplanModel.objects.all())

    class Meta:
        model = CoursesInSubplanModel
        fields = ('id', 'courseId', 'subplanId')
