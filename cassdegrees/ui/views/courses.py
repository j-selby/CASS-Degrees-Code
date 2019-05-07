from api.models import CourseModel, SubplanModel, ProgramModel
from api.views import search

from django.http import HttpResponseNotFound, HttpRequest
from django.shortcuts import render, redirect

from ui.forms import EditCourseFormSnippet
import json


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

    # Generate an internal request to search api made by Jack
    gen_request = HttpRequest()

    # Grab all the courses in the database
    gen_request.GET = {'select': 'id,code,year', 'from': 'course'}
    courses = json.loads(search(gen_request).content.decode())

    ids_to_delete = data.getlist('id')  # ids of all the courses that were selected to be deleted
    courses_to_delete = [c for c in filter(lambda c: c['id'] in map(int, ids_to_delete), courses)]  # [dict]
    used_subplans = dict()  # {subplan id (int): [course] (list(dict))}
    used_subplans_info = dict()  # {subplan_id (int): subplan information (str)}
    used_programs = dict()  # {program id (int): [subplan/course] (list(dict))}
    used_programs_info = dict()  # {program id (int): program information (str)}

    def check_course(prog_or_sub, used_prog_or_sub, used_prog_or_sub_info, c):
        """ Checks if a course c is in a program/subplan and keeps track of it

        :param prog_or_sub: a list of programs/subplans that depend on c
        :type prog_or_sub: dict
        :param used_prog_or_sub: {program/subplan id (int) -> a list of subplans/courses (list)}
        :type used_prog_or_sub: dict
        :param used_prog_or_sub_info: {program/subplan id (int) -> program/subplan information (str)}
        :type used_prog_or_sub_info: dict
        :param c: course
        :type c: dict
        :return: None
        """
        if len(prog_or_sub) > 0:  # if the course with code equal to c['code'] is used on any program/subplan
            # dont delete the course and keep track of which subplans/programs are dependent on course c
            for ps in prog_or_sub:
                if ps['id'] not in used_prog_or_sub:
                    used_prog_or_sub[ps['id']] = [c]
                else:
                    used_prog_or_sub[ps['id']] += [c]
                # used for error message composition later
                used_prog_or_sub_info[ps['id']] = ps['name'] + ' (' + ps['code'] + ') ' + 'in ' + str(ps['year'])

    for c in courses_to_delete:
        gen_request.GET = {'select': 'code', 'from': 'course', 'code': c['code']}
        duplicate_courses = json.loads(search(gen_request).content.decode())
        if len(duplicate_courses) == 1:  # if there is only one course instance with code equal to c['code']
            # checks subplans' rules for courses
            gen_request.GET = {'select': 'id,code,name,year,rules', 'from': 'subplan', 'rules': c['code']}
            subplans = json.loads(search(gen_request).content.decode())  # subplans that depend on c['code']
            check_course(subplans, used_subplans, used_subplans_info, c)
            # check programs' rules for courses
            gen_request.GET = {'select': 'id,code,name,year,rules', 'from': 'program', 'rules': c['code']}
            programs = json.loads(search(gen_request).content.decode())  # programs that depend on c['code']
            check_course(programs, used_programs, used_programs_info, c)

    # checks programs' rules for subplans
    gen_request.GET = {'select': 'id,code,name,year,rules', 'from': 'program'}
    programs = json.loads(search(gen_request).content.decode())
    for p in programs:
        subplan_id_rules = [s_id for ids in [r['ids'] for r in p['rules'] if r['type'] == 'subplan'] for s_id in ids]
        for subplan_id in subplan_id_rules:
            if subplan_id in used_subplans:  # if this subplan with subplan_id is affected by the selected courses
                # keep track of which program is affected and via which subplan
                if p['id'] not in used_programs:
                    used_programs[p['id']] = used_subplans[subplan_id]
                else:
                    used_programs[p['id']] += used_subplans[subplan_id]
                used_programs_info[p['id']] = p['name'] + ' (' + p['code'] + ') ' + 'in ' + str(p['year'])

    def compose_message(start_msg, content, content_info):
        """ Composes error message when a course(s) is in any program/subplan

        :param start_msg: start of the message
        :type start_msg: str
        :param content: {program/subplan id (int) -> list of programs/subplans (list)}
        :type content: dict
        :param content_info: {program/subplan id (int)-> program/subplan information (list)}
        :type content_info: dict
        :return: composed message (str)
        """
        msg = start_msg
        for content_id, elems in content.items():
            is_plural = len(elems) > 1
            msg += '{} uses: {}\n'.format(content_info[content_id], (', ' if is_plural else '')
                                          .join([e['code'] + ' in ' + str(e['year']) for e in elems]))
        return msg
    if not used_subplans and not used_programs:  # if no programs/subplans are using the selected courses then delete
        for c in courses_to_delete:
            instances.append(CourseModel.objects.get(id=c['id']))
    else:
        # compose ui error message
        error_msg = ''
        if used_programs:
            error_msg += compose_message('The Program(s):\n', used_programs, used_programs_info)
        if used_programs and used_subplans:
            error_msg += 'and\n'
        if used_subplans:
            error_msg += compose_message('The Subplan(s):\n', used_subplans, used_subplans_info)
        return redirect('/list/?view=Course&error=Failed to Delete Course(s)!\n' + error_msg)

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
