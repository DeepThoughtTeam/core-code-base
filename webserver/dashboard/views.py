from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
import requests


# Create your views here.

def index(request):
    context = {}
    return render(request, 'dashboard/welcome.html', context)


def about(request):
    return render(request, 'dashboard/about.html')


@csrf_exempt
def proc_net_info(request):
    print "proc_net_info"
    print request.POST
    content = request.body
    print content
    r_app = requests.post("http://legend02.pc.cc.cmu.edu:8000/run_net_proc", data=content)
    r = HttpResponse(r_app.text)

    return r


def app_server(request):
    r_app = requests.get("http://legend02.pc.cc.cmu.edu:8000")
    r = HttpResponse(r_app.text)

    return r
