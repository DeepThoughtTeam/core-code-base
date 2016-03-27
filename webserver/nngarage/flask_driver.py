import requests
from django.http import HttpResponse, Http404

def run_exp(task_name="", weights="", train="", test=""):
    params = {}
    params['name'] = task_name
    params['weights'] = weights
    params['train'] = train
    params['test'] = test
    r = requests.post("http://legend02.pc.cc.cmu.edu:5000/tensor/run", data=params)
    return r
