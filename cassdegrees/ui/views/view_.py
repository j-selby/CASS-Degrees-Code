from django.shortcuts import render
import requests

def view_(request):
    id_to_edit = request.GET.get('id', None)
    url = request.build_absolute_uri()

    if "view_course" in url:
        course = requests.get(request.build_absolute_uri('/api/model/course/' + id_to_edit + '/?format=json')).json()
        return render(request, 'viewcourse.html', context={'data': course})

    elif "view_subplan" in url:
        subplan = requests.get(request.build_absolute_uri('/api/model/subplan/' + id_to_edit + '/?format=json')).json()
        return render(request, 'viewsubplan.html', context={'data': subplan})

    elif "view_program" in url:
        program = requests.get(request.build_absolute_uri('/api/model/degree/' + id_to_edit + '/?format=json')).json()
        return render(request, 'viewprogram.html', context={'data': program})
