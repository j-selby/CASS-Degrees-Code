from django.shortcuts import render
from .models import SampleModel
from .serializers import SampleSerializer
from rest_framework import generics


class SampleList(generics.ListCreateAPIView):
    queryset = SampleModel.objects.all()
    serializer_class = SampleSerializer
