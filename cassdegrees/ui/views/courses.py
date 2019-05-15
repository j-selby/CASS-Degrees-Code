from api.models import CourseModel, SubplanModel, ProgramModel
from api.views import search

from django.http import HttpResponseNotFound, HttpRequest
from django.shortcuts import render, redirect

from ui.forms import EditCourseFormSnippet
import json


def create_course(request):
    duplicate = request.GET.get('duplicate', 'false')
    if duplicate == 'true':
        duplicate = True
    elif duplicate == 'false':
        duplicate = False

    # Initialise instance with an empty string so that we don't get a "may be referenced before assignment" error below
    instance = ""

    # If we are creating a course from a duplicate, we retrieve the instance with the given id
    # (should always come along with 'duplicate' variable) and return that data to the user.
    if duplicate:
        id = request.GET.get('id')
        if not id:
            return HttpResponseNotFound("Specified ID not found")
        # Find the course to specifically create from:
        instance = CourseModel.objects.get(id=int(id))

    if request.method == 'POST':
        form = EditCourseFormSnippet(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/list/?view=Course&msg=Successfully Added Course!')

    else:
        if duplicate:
            form = EditCourseFormSnippet(instance=instance)
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

    # Grab all the courses in the database
    gen_request.GET = {'select': 'id,code,year', 'from': 'course'}
    courses = json.loads(search(gen_request).content.decode())

    # ids of all the courses that were selected to be deleted
    ids_to_delete = [int(course_id) for course_id in data.getlist('id')]
    courses_to_delete = [c for c in courses if c['id'] in ids_to_delete]

    error_msg = ""
    instances = []

    for course in courses_to_delete:
        gen_request.GET = {'select': 'code', 'from': 'course', 'code': course['code']}
        duplicate_courses = json.loads(search(gen_request).content.decode())
        if len(duplicate_courses) < 2:
            gen_request.GET = {'select': 'code,year,rules', 'from': 'subplan', 'rules': course['code']}
            # subplans which depend on course where its code is equal to course['code']
            subplans = json.loads(search(gen_request).content.decode())
            gen_request.GET = {'select': 'code,year,rules', 'from': 'program', 'rules': course['code']}
            # programs which depend on course where its code is equal to course['code']
            programs = json.loads(search(gen_request).content.decode())

            # if there are any subplans/programs that could be affected by the deletion of the selected courses
            if len(subplans) > 0 or len(programs) > 0:
                # compose error message
                if len(subplans) > 0:
                    for subplan in subplans:
                        error_msg += "Course Code: '" + course['code'] + "'(" + str(course['year']) + \
                                     ") is used by Subplan Code: '" + subplan['code'] + "'(" + \
                                     str(subplan['year']) + ").\n"
                if len(programs) > 0:
                    for program in programs:
                        error_msg += "Course Code: '" + course['code'] + "'(" + str(course['year']) + \
                                         ") is used by Program Code: '" + program['code'] + "'(" + \
                                         str(program['year']) + ").\n"
                continue  # dont append course to the list instances
        instances.append(CourseModel.objects.get(id=course['id']))

    if len(error_msg) > 0:
        return redirect('/list/?view=Course&error=Failed to Delete Course(s)!\n' + error_msg +
                        '\nPlease check dependencies!')

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
