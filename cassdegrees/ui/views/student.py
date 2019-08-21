from api.models import ProgramModel
from django.forms import model_to_dict
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils import timezone

import zlib
import base64
import json


def compress(dct):
    """ Takes a dictionary and returns a base64 encoding of the contained data

    :param dct: The dictionary to compress
    :return <str>:
    """
    return base64.b64encode(zlib.compress(bytes(json.dumps(dct), 'utf-8'), 9)).decode('utf-8')


def decompress(string):
    """ Takes a base64 string and returns a dict of the contained data

    :param string: The base64 encoding of the compressed dictionary
    :return <dict>:
    """
    return json.loads(zlib.decompress(base64.b64decode(string)))


def load_messages(cookies):
    """ Takes a dict of cookies and reads regular and error messages from them, deleting them from the original dict

    :param cookies: The dictionary to read the cookies from
    :return dict: A dictionary containing both messages that can be fed in to the render settings
    """

    render_settings = {}
    error = cookies.get('error_message', None)
    if error:
        render_settings['error'] = error
        try:
            del cookies['error_message']
        except KeyError:
            pass
    message = cookies.get('message', None)
    if message:
        render_settings['msg'] = message
        try:
            del cookies['message']
        except KeyError:
            pass

    return render_settings


# Static page for student landing
def student_index(request):
    # Load up the error and regular messages to render in the plan
    render_settings = load_messages(request.session)

    # Generate a list of name-date tuples for all plans saved in the cookies
    plans = [
        {'name':plan[5:], 'date': decompress(val)['date']}
        for plan, val in request.session.items() if plan[:5] == "plan:"
    ]

    return render(request, 'student_index.html', context={'plans': plans, 'render': render_settings})


# Delete the requested plan
def student_delete(request):
    plan_name = request.GET.get('plan', None)

    if plan_name is not None:
        try:
            del request.session['plan:'+plan_name]
        except KeyError:
            pass

    return redirect(student_index)


# Creation page. Also sends program metadata.
def student_create(request):
    id_to_view = request.GET.get('id', None)

    # Create a plan if an ID is specified
    if id_to_view:
        # Create a new cookie in the default plan location containing compressed relevant plan details
        request.session['plan:'] = compress(
            {'program_id': int(id_to_view), 'date': timezone.now().strftime('%d/%m/%Y')}
        )

        # Redirect to the student edit page and add the '?plan=' url parameter
        response = redirect(student_edit)
        response['Location'] += '?plan='
        return response
    # Render the creation homepage if an ID is not specified
    else:
        return render(request, 'student_create.html', context={'programs': ProgramModel.objects.filter(publish=True)})


# Main edit page. Sends program metadata for specific course chosen.
def student_edit(request):
    plan_name = request.GET.get('plan', None)

    # Load up the error and regular messages to render in the plan
    render_settings = load_messages(request.session)

    # If no plan name is specified, redirect them to the plan creation page
    if plan_name is None:
        request.session['error_message'] = 'No plan name given'
        return redirect(student_index)
    # If the user submits a POST request
    if request.method == "POST":
        new_plan_name = request.POST.get('plan_name', None)

        # If the plan name changed, delete the old one and create the new one
        if new_plan_name != plan_name:
            plans = [plan[5:] for plan in request.session.keys() if plan[:5] == "plan:"]
            if new_plan_name in plans:
                new_plan = {key: request.POST[key] for key in request.POST.keys()
                            if key != 'csrfmiddlewaretoken' and key != 'plan_name'
                }
                render_settings['error'] = 'A plan already exists with that name. Please choose a different name.'
                return render(request, 'student_edit.html', context={'plan': new_plan,
                                                                     'program': {},
                                                                     'render': render_settings,
                                                                     'superuser': request.user.is_authenticated})
            else:
                new_plan = {key: request.POST[key] for key in request.POST.keys()
                            if key != 'csrfmiddlewaretoken' and key != 'plan_name'
                }
                new_plan['date'] = timezone.now().strftime('%d/%m/%Y')
                request.session['plan:'+new_plan_name] = compress(new_plan)

                try:
                    del request.session['plan:' + plan_name]
                except KeyError:
                    pass
        # If the plan name stayed the same, update the old plan
        else:
            new_plan = {key: request.POST[key] for key in request.POST.keys()
                        if key != 'csrfmiddlewaretoken' and key != 'plan_name'
            }
            new_plan['date'] = timezone.now().strftime('%d/%m/%Y')
            request.session['plan:' + new_plan_name] = compress(new_plan)
        request.session['message'] = 'Successfully saved'
        return redirect('/edit/?plan='+new_plan_name)
    # If the user submits a get request
    else:
        # Decompress and read the plan from the cookies
        compressed_plan = request.session.get("plan:"+plan_name, '')
        if compressed_plan:
            plan = decompress(compressed_plan)
            plan['name'] = plan_name

            # Get the program that was specified in the plan
            try:
                instance = model_to_dict(ProgramModel.objects.get(id=plan['program_id']))
            except ProgramModel.DoesNotExist:
                render_settings['error'] = 'This program plan is not valid. Please create a new Program Plan'
                instance = {}

            return render(request, 'student_edit.html', context={'plan': plan,
                                                                 'program': instance,
                                                                 'render': render_settings,
                                                                 'superuser': request.user.is_authenticated})
        else:
            request.session['error_message'] = 'Invalid plan name given'
            return redirect(student_index)
