from api.models import CourseModel, SubplanModel, ProgramModel
from api.views import search

from django.http import HttpResponseNotFound, HttpRequest
from django.shortcuts import render, redirect

from ui.forms import EditCourseFormSnippet
import json


def create_course(request):
    if request.method == 'POST':
        form = EditCourseFormSnippet(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/list/?view=Course&msg=Successfully Added Course!')

    else:
        form = EditCourseFormSnippet()

    return render(request, 'createcourse.html', context={
        "edit": False,
        "form": form,
        "courses": CourseModel.objects.values()
    })


def delete_course(request):
    data = request.POST
    instances = []

    # Generate an internal request to search api made by Jack
    gen_request = HttpRequest()

    # Grab all the programs in the database
    gen_request.GET = {'select': 'id,code,year,name,rules', 'from': 'program'}
    programs = json.loads(search(gen_request).content.decode())

    # Grab all the subplans in the database
    gen_request.GET = {'select': 'id,code,name,year,rules', 'from': 'subplan'}
    subplans = json.loads(search(gen_request).content.decode())

    # Grab all the courses in the database
    gen_request.GET = {'select': 'id,code,year', 'from': 'course'}
    courses = json.loads(search(gen_request).content.decode())

    ids_to_delete = data.getlist('id')  # ids of all the courses that were selected to be deleted

    # inner join ids_to_delete with courses
    courses_to_delete = [c for c in filter(lambda c: c['id'] in map(int, ids_to_delete), courses)]  # [dict]
    used_subplans = dict()  # {subplan id (int): [course] (list(dict))}
    used_programs = dict()  # {program id (int): [subplan/course] (list(dict))}
    # grabs all subplans that depend on courses selected to be deleted
    for c in courses_to_delete:
        for s in subplans:
            # if course c is in subplan s
            if any(c['id'] == r['id'] for r in s['rules']):
                # keep track of it
                if s['id'] not in used_subplans:
                    used_subplans[s['id']] = [c]
                else:
                    used_subplans[s['id']] += [c]
        # TODO: parse program rules field
        # attempt to find standalone courses in program rules
        gen_request.GET = {'select': 'id,name,year,rules', 'from': 'program',
                           'rules': c['code']}
        for p in json.loads(search(gen_request).content.decode()):
            if p['id'] not in used_programs:
                used_programs[p['id']] = [c]
            else:
                used_programs[p['id']] += [c]

    print('used programs: ', used_programs)

    if used_subplans:  # if there are any subplans being used with one or more of the courses selected
        subplan_info = dict()  # {subplan_id (int): subplan information (str)}
        # composes error message
        for s in subplans:
            # if subplan s is being used
            if s['id'] in used_subplans:
                subplan_info[s['id']] = s['name'] + ' (' + s['code'] + ') ' + 'in ' + str(s['year'])
        error_msg = 'The course(s):\n'
        for subplan_id, cs in used_subplans.items():
            is_plural = len(cs) > 1
            error_msg += '{} {} being used by: {} {}'.format(
                (', ' if is_plural else ' ').join([c['code'] + ' in ' + str(c['year']) for c in cs]),
                'are' if is_plural else 'is', subplan_info[subplan_id], '\n')
            print(error_msg)
        return redirect('/list/?view=Course&error=Failed to Delete Course(s)!\n' + error_msg)
    else:
        for c in courses_to_delete:
            instances.append(CourseModel.objects.get(id=c['id']))

    if "confirm" in data:
        for instance in instances:
            instance.delete()

        return redirect('/list/?view=Course&msg=Successfully Deleted Course(s)!')
    else:
        return render(request, 'deletecourses.html', context={
            "instances": instances
        })


def edit_course(request):
    id = request.GET.get('id')
    if not id:
        return HttpResponseNotFound("Specified ID not found")

    # Find the program to specifically edit
    instance = CourseModel.objects.get(id=int(id))

    if request.method == 'POST':
        form = EditCourseFormSnippet(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('/list/?view=Course&msg=Successfully Edited Course!')

    else:
        form = EditCourseFormSnippet(instance=instance)

    return render(request, 'createcourse.html', context={
        "edit": True,
        "form": form,
        "courses": CourseModel.objects.values()
    })
