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

@login_required
def add_file(request, user_id=0):
  if 'file' not in request.FILES or 'name' not in request.POST:
    print "file post fail, lack name or file field"
    raise Http404
  file = request.FILES['file']
  name = request.POST['name']

  with transaction.atomic():
      new_file = FileBase(file_content=file, file_name=name, file_type=0)
      user_file = UserFile(user_id=user_id, file_id=new_file.pk)
      new_file.save()
      user_file.save()
  return HttpResponse("OK")

@login_required
def get_exp_list(request):
    return HttpResponse("OK")


@login_required
def get_exp_info(request):
    return HttpResponse("OK")

@login_required
def run_exp(request):
    ret = requests.post("http://localhost:5000/tensor/run", data={'id': 1, 'path': 'None', 'p1': 'a', 'p2': 'a', 'p1': 'a'})
    if ret.status_code == 200:
        return HttpResponse("OK")
    raise Http404

def upload_expriment_file(request):
  if 'file' not in request.FILES or 'name' not in request.POST:
    print "file post fail, lack name or file field"
    raise Http404
  file = request.FILES['file']
  name = request.POST['name']
  user_id = request.POT['id']

  with transaction.atomic():
      new_file = FileBase(file_content=file, file_name=name, file_type=1)
      user_file = UserFile(user_id=user_id, file_id=new_file.pk)
      new_file.save()
      user_file.save()
  return HttpResponse("OK")

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
  #response['X-Sendfile'] = smart_str("../mysite/media/files/1.png")
  return response
