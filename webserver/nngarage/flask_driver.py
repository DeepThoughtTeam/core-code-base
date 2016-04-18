import requests
from django.http import HttpResponse, Http404

def run_exp(task_name="", user_name="", weights="", train="", test="", learning_rate=0.01, out_dim=2, num_iter=10):
    SOURCE_URL = "http://legend02.pc.cc.cmu.edu:53026/tensor/run"
    # SOURCE_URL = "http://localhost:5001/tensor/run"
    params = {}
    params['task_name'] = task_name
    params['user_name'] = user_name
    params['weights'] = weights
    params['train'] = train
    params['test'] = test
    # newly added
    params['learning_rate'] = learning_rate
    params['out_dim'] = out_dim
    params['num_iter'] = num_iter
    with open("/home/deepbic/workspace/core-code-base/webserver/tmp_data.txt", 'w') as f:
        f.write("out_dim=" + str(params['out_dim']))
        f.write("num_iter=" + str(params['num_iter']))

    r = requests.post(SOURCE_URL, data=params)
    return r
