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
    gen_request.GET = {'select': 'id,code,name,year,rules', 'from': 'subplan'}
    # Grab all the subplans in the database
    subplans = json.loads(search(gen_request).content.decode())

    # Grab all the courses in the database
    gen_request.GET = {'select': 'id,code,year', 'from': 'course'}
    courses = json.loads(search(gen_request).content.decode())

    ids_to_delete = data.getlist('id')  # ids of all the courses that were selected to be deleted
    safe_to_delete = True
    used_programs_subplans = dict()  # {program/subplan (str): [course] (list(str))}
    for id_to_delete in ids_to_delete:
        # checks subplans' rules if they are using the selected courses for deletion
        for subplan in subplans:
            course_ids_in_rules = [rule['id'] for rule in subplan['rules']]
            # if course to delete is being used in a subplan
            if int(id_to_delete) in course_ids_in_rules:
                safe_to_delete = False
                # gets course in courses with the id id_to_delete
                course = [c for c in filter(lambda c: c['id'] == int(id_to_delete), courses)].pop()
                # if the subplan has already been seen using another course
                if subplan['id'] in used_programs_subplans:
                    used_programs_subplans[subplan['id']] = used_programs_subplans[subplan['id']] + [course]
                else:
                    used_programs_subplans[subplan['id']] = [course]
        # TODO: Grab all the programs in the database

        if safe_to_delete:
            instances.append(CourseModel.objects.get(id=int(id_to_delete)))

    if used_programs_subplans:  # if there exists programs/subplans that use selected courses
        error_msg = ''
        # composes the error message
        for list_id, courses in used_programs_subplans.items():
            error_msg += 'The course(s): '
            num_of_courses = len(courses)
            for i in range(num_of_courses):
                error_msg += courses[i]['code'] + ' in ' + str(courses[i]['year'])\
                             + (', ' if i < num_of_courses-1 else '')
            # TODO: search through programs
            program_subplan = [s for s in filter(lambda s: s['id'] == list_id, subplans)].pop()
            error_msg += ' ' + ('are' if num_of_courses > 1 else 'is') + ' being used by ' + program_subplan['name']\
                         + '(' + program_subplan['code'] + ')' + ' in  ' + str(program_subplan['year']) + '.'
        return redirect('/list/?view=Course&error=Failed to Delete Course(s)! ' + error_msg
                        + ' Please act on these dependencies before the deletion can occur.')

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
