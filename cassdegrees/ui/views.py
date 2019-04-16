from django.http import HttpResponse
from django.shortcuts import render
import os
import requests
import csv
from io import TextIOWrapper


# Create your views here.
# I added a very simple sample request handler, this is very simple and all it does is load index.html from templates.
def index(request):

    # add button parameters to be rendered on the main menu
    # TODO: Update URLs once initial page views are created
    buttons = [
        {'url': "/api/model/degree/", 'img': "../static/img/create_plan_img.png", 'label': "Create Plan"},
        {'url': "/create_subplan/", 'img': "../static/img/create_subplan_img.png", 'label': "Create Subplan"},
        {'url': "", 'img': "../static/img/create_list_img.png", 'label': "Create List"},
        {'url': "/list/", 'img': "../static/img/open_existing_img.png", 'label': "Open Existing"},
        {'url': "/list/?view=Course", 'img': "../static/img/manage_courses_img.png", 'label': "Manage Courses"}
    ]

    return render(request, 'index.html', context={'buttons': buttons})


def planList(request):
    """ Generates a table based on the JSON objects stored in 'data'

    NOTE: For the page to generate the tabs correctly, the api table data must be put in the context
    under the dictionary {'data': {'RELATION': RELATION_DATA, ...}}. To link to the actual data correctly,
    ensure the RELATION text is the same as what is called in the API (e.g. /api/model/RELATION/?format=json)

    :param request:
    :return <class django.http.response.HttpResponse>:
    """
    degree = requests.get(request.build_absolute_uri('/api/model/degree/?format=json')).json()
    subplan = requests.get(request.build_absolute_uri('/api/model/subplan/?format=json')).json()
    course = requests.get(request.build_absolute_uri('/api/model/course/?format=json')).json()

    return render(request, 'list.html', context={'data': {'Degree': degree, 'Subplan': subplan, 'Course': course}})


# I went through this tutorial to create the form html file and this view:
# https://docs.djangoproject.com/en/2.2/topics/forms/
# Hope this serves as an inspiration for when we make proper views and functions to submit course information
def sampleform(request):
    # If POST request, redirect the received information to the backend:
    if request.method == 'POST':
        # Hard coding url is a bad practice; this is only a temporary measure for this demo sampleform.
        model_api_url = 'http://127.0.0.1:8000/api/model/sample/'
        post_data = request.POST
        actual_request = post_data.get('_method')

        # This method of transferring data to the API was inspired by:
        # https://stackoverflow.com/questions/11663945/calling-a-rest-api-from-django-view
        if actual_request == "post":
            # Create a python dictionary with exactly the same fields as the model (in this case, sampleModel)
            samplefields = \
                {
                    'id': post_data.get('id'),
                    'text': post_data.get('text')
                }
            # Submit a POST request to the sample API with samplefields as data (basically a new record)
            rest_api = requests.post(model_api_url, data=samplefields)

            if rest_api.status_code == 201:
                return HttpResponse('Record successfully added!')
            else:
                return HttpResponse('Failed to submit!')

        elif actual_request == "patch":
            id_to_edit = post_data.get('id')
            # Patch requests (editing an already existing resource only requires fields that are changed
            samplefields = \
                {
                    'text': post_data.get('text')
                }

            rest_api = requests.patch(model_api_url + id_to_edit + '/', data=samplefields)

            if rest_api.status_code == 200:
                return HttpResponse('Record successfully edited!')
            else:
                return HttpResponse('Failed to edit record!')

        else:
            id_to_delete = post_data.get('id')

            rest_api = requests.delete(model_api_url + id_to_delete + '/')

            if rest_api.status_code == 204:
                return HttpResponse('Record successfully deleted!')
            else:
                return HttpResponse('Failed to delete record!')

    else:
        return render(request, 'sampleform.html')


def create_subplan(request):
    return render(request, 'createsubplan.html')


# inspired by the samepleform function created by Daniel Jang
def manage_courses(request):
    # Reads the 'action' attribute from the url (i.e. manage/?action=Add) and determines the submission method
    actions = ['Add', 'Edit', 'Delete']
    action = request.GET.get('action', 'Add')

    courses = requests.get(request.build_absolute_uri('/api/model/course/?format=json')).json()
    courses = [{'code': course} for course in set([x['code'] for x in courses])]
    # If POST request, redirect the received information to the backend:
    render_properties = {
        'msg': None,
        'is_error': False
    }
    if request.method == 'POST':
        model_api_url = request.build_absolute_uri('/api/model/course/')
        post_data = request.POST
        # actual_request = post_data.get('_method')

        if action == 'Add':
            # Create a python dictionary with exactly the same fields as the model (in this case, CourseModel)
            offered_sems = post_data.getlist('semesters[]')
            course_instance = \
                {
                    'code': post_data.get('code'),
                    'year': post_data.get('year'),
                    'name': post_data.get('name'),
                    'units': post_data.get('units'),
                    'offeredSem1': 'semester1' in offered_sems,
                    'offeredSem2': 'semester2' in offered_sems
                }
            # Submit a POST request to the course API with course_instance as data
            rest_api = requests.post(model_api_url, data=course_instance)
            if rest_api.status_code == 201:
                render_properties['msg'] = 'Course successfully added!'
            else:
                render_properties['is_error'] = True
                # detects if the course already exists
                if 'The fields code, year must make a unique set.' in rest_api.json()['non_field_errors']:
                    render_properties['msg'] = "The course you are trying to create already exists!"
                else:
                    render_properties['msg'] = "Unknown error while submitting document. Please try again."

        # to be implemented, currently has the sample model code
        elif action == 'Edit':
            id_to_edit = post_data.get('id')
            # Patch requests (editing an already existing resource only requires fields that are changed
            course_instance = \
                {
                    'text': post_data.get('text')
                }

            rest_api = requests.patch(model_api_url + id_to_edit + '/', data=course_instance)

            if rest_api.status_code == 200:
                render_properties['msg'] = 'Course information successfully modified!'
            else:
                render_properties['is_error'] = True
                render_properties['msg'] = "Failed to edit course information (unknown error). Please try again."

        # to be implemented, currently has the sample model code
        elif action == 'Delete':
            id_to_delete = post_data.get('id')

            rest_api = requests.delete(model_api_url + id_to_delete + '/')

            if rest_api.status_code == 204:
                render_properties['msg'] = 'Course successfully deleted!'
            else:
                render_properties['is_error'] = True
                render_properties['msg'] = "Failed to delete course. An unknown error has occurred. Please try again."

    return render(request, 'managecourses.html', context={'action': action, 'courses': courses,
                                                          'render': render_properties, 'actions': actions})


def bulk_data_upload(request):
    context = {}
    context['upload_type'] = ['Courses', 'Subplans']
    content_type = request.GET.get('type')
    print(content_type)

    if content_type in context['upload_type']:
        context['current_tab'] = content_type

    if request.method == 'POST':
        base_model_url = request.build_absolute_uri('/api/model/')

        # Open file in text mode:
        # https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
        uploaded_file = TextIOWrapper(request.FILES['uploaded_file'], encoding=request.encoding)

        # Reading the TSV using the csv import module came from:
        # https://stackoverflow.com/questions/13992971/reading-and-parsing-a-tsv-file-then-manipulating-it-for-saving-as-csv-efficie

        uploaded_file = csv.reader(uploaded_file, delimiter='%')

        # First row contains the column type headings (code, name etc). We can't add them to the db.
        first_row_checked = False

        # Check if any errors or successes appear when uploading the files.
        # Used for determining type of message to show to the user on the progress of their file upload.
        any_error = False
        any_success = False
        for row in uploaded_file:
            if first_row_checked:

                if content_type == 'Courses':
                    if len(row) != 6:
                        any_error = True
                        break

                    course_instance = \
                        {
                            'code': row[0],
                            'year': int(row[1]),
                            'name': row[2],
                            'units': int(row[3]),
                            'offeredSem1': bool(row[4]),
                            'offeredSem2': bool(row[5])
                        }

                    # Submit a POST request to the course API with course_instance as data
                    rest_api = requests.post(base_model_url + 'course/', data=course_instance)
                    if rest_api.status_code == 201:
                        any_success = True
                        print('Successfully added!')
                    else:
                        any_error = True
                        print(rest_api.text)

                elif content_type == 'Subplans':
                    if len(row) != 5:
                        any_error = True
                        break

                    subplan_instance = \
                        {
                            'code': row[0],
                            'year': int(row[1]),
                            'name': row[2],
                            'units': int(row[3]),
                            'planType': str(row[4])
                        }
                    rest_api = requests.post(base_model_url + 'subplan/', data=subplan_instance)
                    if rest_api.status_code == 201:
                        any_success = True
                        print('Successfully added!')
                    else:
                        any_error = True
                        print(rest_api.text)

            else:
                first_row_checked = True

        # Display error messages depending on the level of success of bulk upload.
        # There are 3 categories: All successful, some successful or none successful.
        if any_success and not any_error:
            context['user_msg'] = "All items has been added successfully!"
            context['err_type'] = "success"

        elif any_success and any_error:
            context['user_msg'] = "Some items could not be added. Have you added them already? Please check the " \
                       + content_type + \
                       " list and try manually adding ones that failed through the dedicated forms."
            context['err_type'] = "warn"

        elif not any_success and any_error:
            context['user_msg'] = "All items failed to be added. " \
                       "Either you have already uploaded the same contents, or the format of the file is incorrect. " \
                       "Please try again."
            context['err_type'] = "error"
        else:
            print(any_success)
            print(any_error)

    return render(request, 'bulkupload.html', context=context)
