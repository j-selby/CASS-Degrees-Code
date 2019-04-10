from django.shortcuts import render
import os


# Create your views here.
# I added a very simple sample request handler, this is very simple and all it does is load index.html from templates.
def index(request):

    button1 = {'url': "/api/model/degree/", 'img': "../static/img/create_plan_img.png", 'label': "Create Plan"}
    button2 = {'url': "/api/model/subplan/", 'img': "../static/img/create_subplan_img.png", 'label': "Create Subplan"}
    button3 = {'url': "", 'img': "../static/img/create_list_img.png", 'label': "Create List"}
    button4 = {'url': "", 'img': "../static/img/open_existing_img.png", 'label': "Open Existing"}
    button5 = {'url': "/api/model/course/", 'img': "../static/img/manage_courses_img.png", 'label': "Manage Courses"}

    buttons = [button1, button2, button3, button4, button5]
    return render(request, 'index.html', context={'buttons': buttons})
