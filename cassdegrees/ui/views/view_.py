from django.shortcuts import render
import requests

def view_(request):
    id_to_edit = request.GET.get('id', None)
    url = request.build_absolute_uri()

    if "course" in url:
        course = requests.get(request.build_absolute_uri('/api/model/course/' + id_to_edit + '/?format=json')).json()
        return render(request, 'viewcourse.html', context={'data': course})

    elif "subplan" in url:
        subplan = requests.get(request.build_absolute_uri('/api/model/subplan/' + id_to_edit + '/?format=json')).json()
        return render(request, 'viewsubplan.html', context={'data': subplan})

    elif "program" in url:
        program = requests.get(request.build_absolute_uri('/api/model/degree/' + id_to_edit + '/?format=json')).json()
        #print(program)

        for req in program["globalRequirements"]:
            pretty = ""
            for field in req.keys():
                if field[:7] == "courses":
                    if req[field]:
                        pretty += field[7:11] + "-level, "
            pretty = pretty[:-2]

            if len(pretty) > 18:
                pretty = pretty[:-12] + " and" + pretty[-11:]
            elif len(pretty) > 10:
                pretty = pretty[:-11] + " and" + pretty[-11:]

            req["prettyList"] = pretty

        return render(request, 'viewprogram.html', context={'data': program})
