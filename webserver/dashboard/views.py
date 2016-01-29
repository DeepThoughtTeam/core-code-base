from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.

def index(request):
    context = {}
    return render(request, 'dashboard/welcome.html', context)


def app_server(request):
    r_app = requests.get("http://legend02.pc.cc.cmu.edu:8000")
    r = HttpResponse(r_app.text)

    return r
