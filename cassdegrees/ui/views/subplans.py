from django.shortcuts import render
import requests
import csv

from ui.forms import EditSubplanFormSnippet

# Using sampleform template and #59 - basic degree creation workflow as it's inspirations
def create_subplan(request):

    submitted = False

    if request.method == 'POST':
        form = EditSubplanFormSnippet(request.POST)

        if form.is_valid():
            form.save()
            submitted = True

    else:
        form = EditSubplanFormSnippet()

    return render(request, 'createsubplan.html', context={
        "form": form,
        "submitted": submitted
    })
    #
    # render_properties = {
    #     'msg': None,
    #     'is_error': False,
    #     'code': None,
    #     'year': None,
    #     'name': None,
    #     'planType': None
    # }
    #
    # if request.method == 'POST':
    #     model_api_url = 'http://127.0.0.1:8000/api/model/subplan/'
    #     post_data = request.POST
    #
    #     # Generate units from subtype plan selected
    #     subplanUnits = \
    #         {
    #             'MAJ': 48,
    #             'MIN': 24,
    #             'SPEC': 24
    #         }
    #
    #     subplanfields = \
    #         {
    #             'code': post_data.get('code'),
    #             'year': post_data.get('year'),
    #             'name': post_data.get('name'),
    #             'units': subplanUnits[post_data.get('planType')],
    #             'planType': post_data.get('planType')
    #         }
    #
    #     # Submit a POST request to the model with subplan data
    #     rest_api = requests.post(model_api_url, data=subplanfields)
    #
    #     # Store fields in render properties so they can be repopulated on error or success
    #     for field in subplanfields:
    #         render_properties[field] = subplanfields[field]
    #
    #     # Handle request return type and generate success or fail message
    #     if rest_api.status_code == 201:
    #         render_properties['msg'] = 'Subplan successfully added.'
    #     else:
    #         render_properties['is_error'] = True
    #
    #         rest_response = rest_api.json()
    #         if "The fields code, year must make a unique set." in rest_response['non_field_errors']:
    #             render_properties['msg'] = "A subplan already exists with this code and year."
    #
    #             ""
    #
    #         elif "The fields year, name, planType must make a unique set." in rest_response['non_field_errors']:
    #             render_properties['msg'] = "A subplan already exists with this name, year and type."
    #         else:
    #             render_properties['msg'] = "An unknown error occurred while submitting the document."
    #
    # return render(request, 'createsubplan.html', context=render_properties)


# Will need to look into merging with create subplan later...
# Currently acts as a liason between the two functions
# Modification of manage_courses to work for subplans
# editing subplans is currently pending.
def manage_subplans(request):
    # Reads the 'action' attribute from the url (i.e. manage/?action=Add) and determines the submission method
    action = request.GET.get('action', 'Add')

    subplan = requests.get(request.build_absolute_uri('/api/model/subplan/?format=json')).json()
    # If POST request, redirect the received information to the backend:
    render_properties = {
        'msg': None,
        'is_error': False
    }

    if request.method == 'POST':
        model_api_url = request.build_absolute_uri('/api/model/subplan/')
        post_data = request.POST
        perform_function = post_data.get('perform_function')

        # If the request came from list.html (from the add, edit and delete button from the courses list page)
        # Edit is pending the relevant story issue.
        if perform_function == 'retrieve view from selected':
            if action == 'Edit':
                # TODO: edit subplans
                render_properties['msg'] = 'Not yet Implemented!'

            elif action == 'Delete':
                ids_to_delete = post_data.getlist('id')
                rest_api = None
                for id_to_delete in ids_to_delete:
                    rest_api = requests.delete(model_api_url + id_to_delete + '/')

                if rest_api is None:
                    render_properties['is_error'] = True
                    render_properties['msg'] = 'Please select a Subplan to delete!'
                else:
                    if rest_api.status_code == 204:
                        render_properties['msg'] = 'Subplan successfully deleted!'
                    else:
                        render_properties['is_error'] = True
                        render_properties['msg'] = "Failed to delete Subplan. " \
                                                   "An unknown error has occurred. Please try again."

    return render(request, 'managesubplans.html', context={'action': action, 'subplan': subplan,
                                                          'render': render_properties})
