from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpRequest
from django.shortcuts import render, redirect

from ui.forms import EditSubplanFormSnippet

from api.models import SubplanModel
from api.views import search
import json
from django.utils import timezone


# Using sampleform template and #59 - basic program creation workflow as it's inspirations
@login_required
def create_subplan(request):
    duplicate = request.GET.get('duplicate', 'false')
    if duplicate == 'true':
        duplicate = True
    elif duplicate == 'false':
        duplicate = False

    # Initialise instance with an empty string so that we don't get a "may be referenced before assignment" error below
    instance = ""

    # If we are creating a subplan from a duplicate, we retrieve the instance with the given id
    # (should always come along with 'duplicate' variable) and return that data to the user.
    if duplicate:
        id = request.GET.get('id')
        if not id:
            return HttpResponseNotFound("Specified ID not found")
        # Find the subplan to specifically create from:
        instance = SubplanModel.objects.get(id=int(id))

    if request.method == 'POST':
        form = EditSubplanFormSnippet(request.POST)

        if form.is_valid():
            form.save()

            # If there is cached 'program' data, redirect to that page instead
            if request.session.get('cached_program_form_data', ''):
                return redirect(request.session.get('cached_program_form_source', '/'))
            else:
                return redirect('/list/?view=Subplan&msg=Successfully Added Subplan!')

    else:
        if duplicate:
            form = EditSubplanFormSnippet(instance=instance)
        else:
            form = EditSubplanFormSnippet()

    return render(request, 'createsubplan.html', context={
        "form": form
    })


@login_required
def delete_subplan(request):
    data = request.POST
    instances = []

    # This is used to get the ids of subplans which are used by programs.
    # Generates an internal request to the search api made by Jack
    gen_request = HttpRequest()
    # Grab all the subplans in the database
    gen_request.GET = {'select': 'id,code,year', 'from': 'subplan'}
    # Sends the request to the search api
    subplans = json.loads(search(gen_request).content.decode())

    # ids of all the subplans that were selected to be deleted
    ids_to_delete = [int(subplan_id) for subplan_id in data.getlist('id')]
    if not ids_to_delete:
        return redirect('/list/?view=Subplan&error=Please select a Subplan to delete!')
    subplans_to_delete = [s for s in subplans if s['id'] in ids_to_delete]

    error_msg = ""
    instances = []

    for subplan in subplans_to_delete:
        gen_request.GET = {'select': 'code', 'from': 'subplan', 'code': subplan['code']}
        duplicate_subplans = json.loads(search(gen_request).content.decode())
        if len(duplicate_subplans) < 2:
            gen_request.GET = {'select': 'code,year,rules', 'from': 'program', 'rules': subplan['code']}
            # programs which depend on subplan where its code is equal to subplan['code']
            programs = json.loads(search(gen_request).content.decode())

            # if there are any programs that could be affected by the deletion of the selected subplan
            if len(programs) > 0:
                # compose error message
                for program in programs:
                    error_msg += "Subplans Code: '" + subplan['code'] + "'(" + str(subplan['year']) + \
                                 ") is used by Program Code: '" + program['code'] + "'(" + \
                                 str(program['year']) + ").\n"
                continue  # dont append course to the list instances
        instances.append(SubplanModel.objects.get(id=subplan['id']))

    if len(error_msg) > 0:
        return redirect('/list/?view=Course&error=Failed to Delete Subplan(s)!\n' + error_msg +
                        '\nPlease check dependencies!')

    if "confirm" in data:
        for instance in instances:
            instance.delete()

        return redirect('/list/?view=Subplan&msg=Successfully Deleted Subplan(s)!')
    else:
        return render(request, 'deletesubplans.html', context={
            "instances": instances
        })


@login_required
def edit_subplan(request):
    id = request.GET.get('id')
    if not id:
        return HttpResponseNotFound("Specified ID not found")

    # Find the program to specifically edit
    instance = SubplanModel.objects.get(id=int(id))

    if request.method == 'POST':
        form = EditSubplanFormSnippet(request.POST, instance=instance)

        if form.is_valid():
            instance.lastUpdated = timezone.now().strftime('%Y-%m-%d')
            instance.save(update_fields=['lastUpdated'])
            form.save()
            return redirect('/list/?view=Subplan&msg=Successfully Edited Subplan!')

    else:
        form = EditSubplanFormSnippet(instance=instance)

    return render(request, 'createsubplan.html', context={
        "edit": True,
        "form": form
    })
