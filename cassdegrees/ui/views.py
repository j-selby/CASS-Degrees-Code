from django.shortcuts import render
import os


# Create your views here.
# I added a very simple sample request handler, this is very simple and all it does is load index.html from templates.
def index(request):
    return render(request, 'index.html', context={})

def planList(request):
    # Generates a table based on whatever JSON object is stored in 'data'
    # NOTE: data must be an array of dictionaries, with matching labels for each item
    data = [{"id":"1","text":"Test"}, {"id":"2","text":"Test2"}]
    # response = requests.get('/api/sample/?format=json').json()
    return render(request, 'list.html', context={'data': data})