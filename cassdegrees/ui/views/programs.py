from api.models import DegreeModel
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from ui.forms import EditProgramFormSnippet


def create_program(request):
    duplicate = request.GET.get('duplicate', False)
    if duplicate == "True":
        create_from = True

    # Initialise instance with an empty string so that we don't get a "may be referenced before assignment" error below
    instance = ""

    # If we are creating a program from a duplicate, we retrieve the instance with the given id
    # (should always come along with createFrom variable) and return that data to the user.
    if duplicate:
        id = request.GET.get('id')
        if not id:
            return HttpResponseNotFound("Specified ID not found")
        # Find the program to specifically create from:
        instance = DegreeModel.objects.get(id=int(id))

    if request.method == 'POST':
        form = EditProgramFormSnippet(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/list/?view=Degree&msg=Successfully Added Program!')

    else:
        if duplicate:
            form = EditProgramFormSnippet(instance=instance)
        else:
            form = EditProgramFormSnippet()

    return render(request, 'createprogram.html', context={
        "edit": False,
        "form": form
    })


def delete_program(request):
    data = request.POST
    instances = []

    ids_to_delete = data.getlist('id')
    for id_to_delete in ids_to_delete:
        instances.append(DegreeModel.objects.get(id=int(id_to_delete)))

    if "confirm" in data:
        for instance in instances:
            instance.delete()

        return redirect('/list/?view=Degree&msg=Successfully Deleted Program(s)!')
    else:
        return render(request, 'deleteprograms.html', context={
            "instances": instances
        })


def edit_program(request):
    id = request.GET.get('id')
    if not id:
        return HttpResponseNotFound("Specified ID not found")

    # Find the program to specifically edit
    instance = DegreeModel.objects.get(id=int(id))

    if request.method == 'POST':
        form = EditProgramFormSnippet(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('/list/?view=Degree&msg=Successfully Edited Program!')

    else:
        form = EditProgramFormSnippet(instance=instance)

    return render(request, 'createprogram.html', context={
        "edit": True,
        "form": form
    })
