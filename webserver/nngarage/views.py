from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from forms import UserForm
from django.db import transaction
from models import *
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


# The homepage view
@login_required
def index(request):
    return render(request, 'nngarage/control_panel.html')


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
    if 'name' not in request.POST or not request.POST['name']:
        print "Missing task name"
        raise Http404
    if 'model' not in request.FILE or not request.FILE['model']:
        print "Missing model"
        raise Http404
    if 'parameter' not in request.FILE or not request.FILE['parameter']:
        print "Missing parameter"
        raise Http404

    # Initialize local variables
    task_name = request.POST['name']
    model_file = request.FILE['model']
    para_file = request.FILE['parameter']
    train_in_file = request.FILE['train_in']
    test_in = request.FILE['test_in']

    # Initialize author variable
    author = User.objects.get(username=request.user.get_username())

    model = FileBase(author=author, name=task_name + '\'s model', type='MODEL', content=model_file)
    model.save()

    parameter = FileBase(author=author, name=task_name + '\'s parameter', type='PARAM', content=para_file)
    parameter.save()

    train_in = FileBase(author=author, name=task_name + '\'s train_in', type='TRAIN_IN', content=train_in_file)
    train_in.save()

    test_in = FileBase(author=author, name=task_name + '\'s test_in', type='TEST_IN', content=test_in)
    test_in.save()

    task = Task(author=author, name=task_name, model=model, parameter=parameter, train_in=train_in, test_in=test_in)
    task.save()

    return HttpResponse('New task is added successfully.')


'''
def download_file(request):
    if request.method != 'GET':
        raise Http404
    o = FileBase.objects.get(file_name='testfile')
    # filename = __file__ # Select your file here.
    # wrapper = FileWrapper(file(filename))
    # response = HttpResponse(wrapper, content_type='text/plain')
    # response['Content-Length'] = os.path.getsize(filename)
    # return response
    file_data = open("/Users/amaliujia/virenv/mysite/mysite/media/files/1.png").read()
    response = HttpResponse(file_data, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('1.png')
    # response['X-Sendfile'] = smart_str("../mysite/media/files/1.png")
    return response
'''
