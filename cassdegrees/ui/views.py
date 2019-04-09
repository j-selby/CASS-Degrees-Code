from django.http import HttpResponse
from django.shortcuts import render
import requests


# Create your views here.
# I added a very simple sample request handler, this is very simple and all it does is load index.html from templates.
def index(request):
    return render(request, 'index.html', context={})


# I went through this tutorial to create the form html file and this view:
# https://docs.djangoproject.com/en/2.2/topics/forms/
# Hope this serves as an inspiration for when we make proper views and functions to submit course information
def sampleform(request):
    # If POST request, redirect the received information to the backend:
    if request.method == 'POST':
        # Create a python dictionary with exactly the same fields as the model (in this case, sampleModel)
        samplefields = \
            {
                'id': request.POST.get('id'),
                'text': request.POST.get('text')
            }
        # Submit a POST request to the sample API with samplefields as data (basically a new record)
        rest_api = requests.post('127.0.0.1:8000/api/sample/', data=samplefields)

        if rest_api.status_code == 201:
            return HttpResponse('Successfully submitted!')
        else:
            return HttpResponse('Failed to submit!')

    else:
        return render(request, 'sampleform.html')
