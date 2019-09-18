from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpRequest


def report_section(request):
    return render(request, 'staff/report/coursereport.html', context={'data': {}})
