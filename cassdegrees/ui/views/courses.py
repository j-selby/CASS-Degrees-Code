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
    safe_to_delete = True
    used_subplans = dict()  # {subplan_id (str): [course] (list(str))}
    used_programs = dict()  # {program_id (str): [course] (list(str))}
    for id_to_delete in ids_to_delete:
        # checks subplans' rules if they are using the selected courses for deletion
        for subplan in subplans:
            course_ids_in_rules = [rule['id'] for rule in subplan['rules']]
            # TODO: try to rewrite using inner join
            # if course to delete is being used in a subplan
            if int(id_to_delete) in course_ids_in_rules:
                safe_to_delete = False
                # gets course in courses with the id id_to_delete
                course = [c for c in filter(lambda c: c['id'] == int(id_to_delete), courses)].pop()
                # if the subplan has already been seen using another course
                if subplan['id'] in used_subplans:
                    used_subplans[subplan['id']] += [course]
                else:
                    used_subplans[subplan['id']] = [course]

        for program in programs:
            # checks which subplans are being used by program
            subplan_ids_in_rules = [rule['ids'] for rule in program['rules'] if rule['type'] == 'subplan']
            for subplan_id in [subplan_id for subplan_ids in subplan_ids_in_rules for subplan_id in subplan_ids]:
                if program['id'] in used_programs:
                    used_programs[program['id']] += [subplan_id]
                else:
                    used_programs[program['id']] = [subplan_id]
            # checks which courses are being used by program


            # # inner join subplan_ids_in_rules with subplans
            # common_ids = set([s['id'] for s in subplans]) & set(subplan_ids_in_rules)
            # subplans_in_program = [s for s in filter(lambda s: s['id'] in common_ids, subplans)]

        if safe_to_delete:
            instances.append(CourseModel.objects.get(id=int(id_to_delete)))

    if used_subplans:  # if there exists programs/subplans that use selected courses
        error_msg = ''
        # composes the error message
        for subplan_id, courses in used_subplans.items():
            error_msg += 'The course(s): '
            num_of_courses = len(courses)
            for i in range(num_of_courses):
                error_msg += courses[i]['code'] + ' in ' + str(courses[i]['year'])\
                             + (', ' if i < num_of_courses-1 else '')
            # TODO: search through programs
            subplan = [s for s in filter(lambda s: s['id'] == subplan_id, subplans)].pop()
            error_msg += ' ' + ('are' if num_of_courses > 1 else 'is') + ' being used by ' + subplan['name']\
                         + '(' + subplan['code'] + ')' + ' in  ' + str(subplan['year']) + '.'
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
