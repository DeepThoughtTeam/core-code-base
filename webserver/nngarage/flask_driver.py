import requests
from django.http import HttpResponse, Http404

def run_exp(task_name="", user_name="", weights="", train="", test=""):
    #SOURCE_URL = "http://legend02.pc.cc.cmu.edu:5000/tensor/run"
    SOURCE_URL = "http://localhost:5001/tensor/run"
    params = {}
    params['task_name'] = task_name
    params['user_name'] = user_name
    params['weights'] = weights
    params['train'] = train
    params['test'] = test
    print params
    r = requests.post(SOURCE_URL, data=params)
    return r
