from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpRequest

from api.models import CourseModel, ProgramModel, SubplanModel
from api.views import search

import json


def report_section(request):
    # Retrieve all courses and store them in a list.
    all_courses = CourseModel.objects.all()
    all_courses_list = list()

    # Key: course code,
    # Value: dictionary with key as program and/or subplan, value as list of programs/subplans dependent on course.
    all_dependencies = dict()

    # Convert all QuerySet results to Python dictionaries.
    for course in all_courses:
        all_courses_list.append(model_to_dict(course))

    # Sort all courses by order of course codes.
    all_courses_list = sorted(all_courses_list, key=lambda i: i['code'])

    # Generate an internal request to search api made by Jack
    gen_request = HttpRequest()

    # Determine all the subplans and programs that depends on any courses.
    for course in all_courses_list:
        gen_request.GET = {'select': 'code,year,name,rules', 'from': 'subplan', 'rules': course['code']}
        # subplans which depend on course where its code is equal to course['code']
        subplans = json.loads(search(gen_request).content.decode())
        gen_request.GET = {'select': 'code,year,name,rules', 'from': 'program', 'rules': course['code']}
        # programs which depend on course where its code is equal to course['code']
        programs = json.loads(search(gen_request).content.decode())
        all_dependencies[course['code']] = {
            'subplans': subplans,
            'programs': programs
        }

    return render(request, 'staff/report/coursereport.html',
                  context={
                      'courses': all_courses_list,
                      'dependencies': all_dependencies
                  })
