from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from forms import UserForm, NetDescUploadForm
from django.db import transaction
from django.contrib.auth.models import User
from models import Profile, NetDescription
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse


# The homepage view
@login_required
def index(request):
    return render(request, 'nngarage/onboard_test.html')


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

    # Use the previous created user ins to create a profile ins
    p = Profile.objects.create(user=User.objects.get(username=data['username']))
    p.save()

    # Use the previous created user ins to login
    new_user = authenticate(username=data['username'], password=data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))  # redirect to the the homepage


@login_required
def get_nn_desc(request, username=""):
    if username != "":
        u = User.objects.get(username=username)
        nn_desc_metas = NetDescription.get_net_desc_meta(username)

        context = {"net_desc_metas": nn_desc_metas}
        return render(request, 'net_desc_metas.json', context, content_type='application/json')


@login_required
def add_nn_desc(request):
    if 'content' not in request.POST or not request.POST['content']:
        raise Http404
    else:
        form = NetDescUploadForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {'form': form}
            return render(request, 'nngarage/control_panel.html', context)

        form.author = User.objects.get(username=request.user.get_username())
        form.save()

        return render(request, 'nngarage/control_panel.html', context)