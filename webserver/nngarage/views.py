from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from forms import UserForm
from django.db import transaction
from models import *
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
from django.utils.encoding import smart_str
from flask_driver import *
from django.http import HttpResponseRedirect
import mimetypes
import requests
from django.views.decorators.csrf import csrf_exempt


# The homepage view
@login_required
def index(request):
    context = {}
    context['username'] = request.user.username
    return render(request, 'nngarage/control_panel.html', context)


@transaction.atomic
def registration(request):
    context = {}
    if request.method == 'GET':  # Indicate that use wants to register
        context['form'] = UserForm()
        return render(request, 'nngarage/signup.html', context)

    form = UserForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        print form
        return render(request, 'nngarage/signup.html', context)

    # load the cleaned data from the form
    data = form.cleaned_data

    # use the cleaned data to create actural user instance
    new_user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password1'],
                                        first_name=data['first_name'], last_name=data['last_name'])

    new_user.save()

    # Use the previous created user ins to login
    new_user = authenticate(username=data['username'], password=data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))  # redirect to the the homepage


@login_required
@transaction.atomic
def add_task(request):
    if request.method == 'GET':
        return render(request, 'nngarage/task_creation.html')

    context = {}
    if 'name' not in request.POST or not request.POST['name']:
        err = "Missing task name"
        context['task_form_error'] = err
        print err
        return render(request, 'nngarage/task_creation.html', context=context)

    if 'parameter' not in request.FILES or not request.FILES['parameter']:
        err = "Missing task parameter"
        context['task_form_error'] = err
        print err
        return render(request, 'nngarage/task_creation.html', context=context)

    if 'train_in' not in request.FILES or not request.FILES['train_in']:
        err = "Missing task training input"
        context['task_form_error'] = err
        print err
        return render(request, 'nngarage/task_creation.html', context=context)

    if 'test_in' not in request.FILES or not request.FILES['test_in']:
        err = "Missing task test input"
        context['task_form_error'] = err
        print err
        return render(request, 'nngarage/task_creation.html', context=context)

    if 'learning_rate' not in request.POST or not request.POST['learning_rate']:
        err = "Missing learning rate"
        print err
        return render(request, 'nngarage/task_creation.html', context=context)

    if 'out_dim' not in request.POST or not request.POST['out_dim']:
        err = "Missing output dimension"
        print err
        return render(request, 'nngarage/task_creation.html', context=context)

    if 'num_iter' not in request.POST or not request.POST['num_iter']:
        err = "Missing number of iteration"
        print err
        return render(request, 'nngarage/task_creation.html', context=context)

    # Initialize local variables
    task_name = request.POST['name']
    para_file = request.FILES['parameter']
    train_in_file = request.FILES['train_in']
    test_in = request.FILES['test_in']
    learning_rate = float(request.POST['learning_rate'])
    out_dim = int(request.POST['out_dim'])
    num_iter = int(request.POST['num_iter'])

    # Initialize author variable
    author = User.objects.get(username=request.user.get_username())

    parameter = FileBase(author=author, name=task_name + '_parameter', type='PARAM', content=para_file)
    parameter.save()

    train_in = FileBase(author=author, name=task_name + '_train_in', type='TRAIN_IN', content=train_in_file)
    train_in.save()

    test_in = FileBase(author=author, name=task_name + '_test_in', type='TEST_IN', content=test_in)
    test_in.save()

    task = Task(author=author, name=task_name, parameter=parameter, train_in=train_in, test_in=test_in,
                learning_rate=learning_rate, out_dim=out_dim, num_iter=num_iter, train_out=train_in, test_out=test_in, model=train_in)
    task.save()

    user_name = request.user.username
    # Update on March 30
    # In order to fix bug related to confict file names
    # Use the following file name instead of the file names in HTTP forms
    # The format is 'files/file_name_and_extension'
    # parameter_name = parameter.content.name
    # train_in_name = train_in.content.name
    # test_in_name = test_in.content.name
    r = run_exp(task_name, user_name, request.FILES['parameter'].name, request.FILES['train_in'].name,
                request.FILES['test_in'].name, learning_rate, num_iter, out_dim)
    if (r.status_code != 200):
        raise Http404

    context['task_creation_status_feedback'] = "New task is added successfully."
    return HttpResponseRedirect('/nngarage/')


@login_required
@transaction.atomic
def get_tasks(request):
    username = request.user.username
    tasks = Task.get_tasks(User.objects.get(username=username))
    context = {"tasks": tasks}
    print context
    return render(request, 'tasks.json', context, content_type='application/json')


@login_required
def get_task_detailed(request, task_name):
    context = {}
    # context['train_out_name'] = 'aa'
    # context['test_out_name'] = 'bb'
    # context['model_name'] = 'cc'
    # return render(request, 'nngarage/task_inspection.html', context)
    context['task_name'] = task_name
    task_ins = Task.objects.get(name=task_name)

    if task_ins.parameter != None:
        context['para_name'] = task_ins.parameter.name

    if task_ins.train_in != None:
        context['train_in_name'] = task_ins.train_in.name

    if task_ins.train_out != None:
        context['train_out_name'] = task_ins.train_out.name

    if task_ins.test_in != None:
        context['test_in_name'] = task_ins.train_in.name

    if task_ins.test_out != None:
        context['test_out_name'] = task_ins.test_out.name

    if task_ins.model != None:
        context['model_name'] = task_ins.model.name

    context['learning_rate'] = task_ins.learning_rate
    context['out_dim'] = task_ins.out_dim
    context['num_iter'] = task_ins.num_iter

    return render(request, 'nngarage/task_inspection.html', context)


@login_required
def get_file_dump(request, file_name):
    file_ins = FileBase.objects.get(name=file_name)
    print file_ins.content.name
    data = ""
    with open(file_ins.content.path, 'r') as myfile:
        data = [i.replace('\n', '<br>') for i in myfile.readlines()]
    return HttpResponse(data)


@login_required
def download_file(request, file_name):
    file_ins = FileBase.objects.get(name=file_name)
    file_data = open(file_ins.content.path).read()
    response = HttpResponse(file_data, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_ins.content.name)
    return response


def files(request):
    return "OK"


@csrf_exempt
@transaction.atomic
def get_task_update(request):
    if request.method == 'GET':
        return HttpResponse("Get task update request should be POST.")

    if 'token' not in request.POST or not request.POST['token']:
        err = "Missing token"
        return HttpResponse("Missing token")
    elif request.POST['token'] != "lafyyjveotnehialteikeniotjim":
        return HttpResponse("Token error!")

    if 'username' not in request.POST or not request.POST['username']:
        err = "Missing username"
        return HttpResponse("Missing username")

    if 'name' not in request.POST or not request.POST['name']:
        err = "Missing task name"
        return HttpResponse("Missing task name")
    
    task_name = request.POST['name']

    if 'status' not in request.POST or not request.POST['status']:
        err = "Missing status"
        return HttpResponse("Missing status")
    
    user_ins = User.objects.get(username=request.POST['username'])
    task_ins = Task.objects.get(author=user_ins, name=task_name)

    if request.POST['status'] == 'Failed':
        task_ins.completed_status = "Failed"
        task_ins.save()
        return HttpResponse("Task update successfully")

    if 'model' not in request.FILES or not request.FILES['model']:
        err = "Missing task model"
        return HttpResponse("Missing task model")

    if 'train_out' not in request.FILES or not request.FILES['train_out']:
        err = "Missing task training output"
        return HttpResponse("Missing task training output")

    if 'test_out' not in request.FILES or not request.FILES['test_out']:
        err = "Missing task test input"
        return HttpResponse("Missing task test output")

    
    train_out_file = request.FILES['train_out']
    test_out_file = request.FILES['test_out']
    model = request.FILES['model']

    print task_ins

    model = FileBase(author=user_ins, name=task_name + '_model', type='MODEL', content=model)
    model.save()
    print "model saved"
    train_out = FileBase(author=user_ins, name=task_name + '_train_out', type='TRAIN_OUT', content=train_out_file)
    train_out.save()
    print "train file saved"
    test_out = FileBase(author=user_ins, name=task_name + '_test_out', type='TEST_OUT', content=test_out_file)
    test_out.save()
    print "test file saved"

    task_ins.train_out = train_out
    task_ins.test_out = test_out
    task_ins.model = model
    task_ins.finish_time = datetime.datetime.now()
    task_ins.completed_status = "Completed"

    task_ins.save()

    # task_ins(train_out=train_out, test_out=test_out, model=model, finish_time=datetime.datetime.now())
    print "update finish"
    return HttpResponse("Task update successfully")


def exp_download(request):
    if request.method != 'GET' or "name" not in request.GET or not request.GET["name"]:
        raise Http404
    print "Request download_file: %s" % request.GET["name"]
    real_filename = "/home/deepbic/workspace/core-code-base/webserver/files/files/" + request.GET["name"] 
    file_data = open(real_filename).read()
    response = HttpResponse(file_data, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(request.GET["name"])
    return response
