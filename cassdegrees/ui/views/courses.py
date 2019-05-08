from api.models import CourseModel
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from ui.forms import EditCourseFormSnippet


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

    # TODO: Check if breaking subplans
    # for course in courses_in_subplans:
    #     # if course being deleted is in current subplan
    #     if int(id_to_delete) == int(course['courseId_id']):
    #         # TODO: improve this using django queries
    #         used_subplans.extend(
    #             [subplan['name'] + '(' + subplan['code'] + ')' for subplan in subplans if
    #              course['subplanId_id'] == subplan['id']])

    ids_to_delete = data.getlist('id')
    for id_to_delete in ids_to_delete:
        instances.append(CourseModel.objects.get(id=int(id_to_delete)))

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
