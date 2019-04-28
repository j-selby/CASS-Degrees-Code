from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from api.models import DegreeModel, SubplanModel, CourseModel, CoursesInSubplanModel
import requests
import csv
import operator
from io import TextIOWrapper


def create_program(request):
    render_properties = {
        'msg': None,
        'is_error': False
    }

    if request.method == 'POST':
        post_data = request.POST

        # Grab the specific attributes that we are looking for
        degree_dict = \
            {
                'code': post_data.get('code'),
                'name': post_data.get('name'),
                # Do some early validation of these fields
                'year': int(post_data.get('year')),
                'units': int(post_data.get('units')),
                'degreeType': post_data.get('degreeType'),
                'globalRequirements': post_data.get('globalRequirements')
            }

        # Re-inject them into the page for later
        for k, v in degree_dict.items():
            render_properties[k] = v

        # Verify that the data is sane
        if DegreeModel.objects.filter(name__iexact=degree_dict['name'], year=degree_dict['year']).count() > 0:
            # Duplicate name, year pair
            render_properties['is_error'] = True
            render_properties['msg'] = "A program with the same year and name already exists!"
        else:
            # Convert to native types now (i.e parse JSON)
            model = DegreeModel(
                code = degree_dict['code'],
                name = degree_dict['name'],
                year = degree_dict['year'],
                units = degree_dict['units'],
                degreeType = degree_dict['degreeType'],
                globalRequirements = json.loads(degree_dict['globalRequirements'])
            )

            try:
                model.save()
            except (IntegrityError, ValueError) as e:
                message = str(e)

                render_properties['is_error'] = True

                if "duplicate key value" in message and "(code, year)" in message:
                    render_properties['msg'] = "A program with the same year and code already exists!"
                elif "duplicate key value" in message and "(name, year)" in message:
                    render_properties['msg'] = "A program with the same year and name already exists!"
                else:
                    render_properties['msg'] = "An error occurred while saving: " + message
            else:
                render_properties['msg'] = 'Program template successfully added!'

    return render(request, 'createprogram.html', context=render_properties)


def manage_programs(request):
    # Reads the 'action' attribute from the url (i.e. manage/?action=Add) and determines the submission method
    action = request.GET.get('action', 'Add')

    program = requests.get(request.build_absolute_uri('/api/model/degree/?format=json')).json()
    # If POST request, redirect the received information to the backend:
    render_properties = {
        'msg': None,
        'is_error': False
    }

    if request.method == 'POST':
        model_api_url = request.build_absolute_uri('/api/model/degree/')
        post_data = request.POST
        perform_function = post_data.get('perform_function')

        # If the request came from list.html (from the add, edit and delete button from the courses list page)
        # Edit is pending the relevant story issue.
        if perform_function == 'retrieve view from selected':
            if action == 'Edit':
                # TODO: edit programs
                render_properties['msg'] = 'Not yet Implemented!'

            elif action == 'Delete':
                ids_to_delete = post_data.getlist('id')
                rest_api = None
                for id_to_delete in ids_to_delete:
                    rest_api = requests.delete(model_api_url + id_to_delete + '/')

                if rest_api is None:
                    render_properties['is_error'] = True
                    render_properties['msg'] = 'Please select a program to delete!'
                else:
                    if rest_api.status_code == 204:
                        render_properties['msg'] = 'program successfully deleted!'
                    else:
                        render_properties['is_error'] = True
                        render_properties['msg'] = "Failed to delete program. " \
                                                   "An unknown error has occurred. Please try again."

    return render(request, 'manageprograms.html', context={'action': action, 'program': program,
                                                          'render': render_properties})

