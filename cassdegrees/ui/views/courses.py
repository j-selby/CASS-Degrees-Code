from api.models import CourseModel, SubplanModel, ProgramModel
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from ui.forms import EditCourseFormSnippet


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
    used_programs_and_subplans = []

    subplans = list(SubplanModel.objects.values())
    programs = list(ProgramModel.objects.values())

    ids_to_delete = data.getlist('id')
    for id_to_delete in ids_to_delete:
        # checks which subplan is using the current course where course['id'] equals id_to_delete
        for subplan in subplans:
            if int(id_to_delete) in [rule['id'] for rule in subplan['rules']]:
                used_programs_and_subplans.append(subplan)
        # checks which program is using the current course where course['id'] equals id_to_delete
        # TODO: parse degree rules (check for used subplans as well as standalone courses)
        instances.append(CourseModel.objects.get(id=int(id_to_delete)))

    if "confirm" in data:
        for instance in instances:
            instance.delete()

        return redirect('/list/?view=Course&msg=Successfully Deleted Course(s)!')
    else:
        return render(request, 'deletecourses.html', context={
            "instances": instances,
            "used_programs_and_subplans": used_programs_and_subplans
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
