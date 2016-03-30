from flask import Flask
from flask import request
import tensorflow as tf
import numpy as np
import input_data
from util import *
from subprocess import Popen, PIPE
from six.moves import urllib
from threading import Thread
from run_demo import *
from multiprocessing.pool import ThreadPool
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

app = Flask(__name__)

def buildPath(filename, task_name, user_name):
    return "files/" + user_name + "_" + task_name + "_" + filename


def file_manager(filename="", task_name="", user_name="", filepath="files/"):
    #SOURCE_URL = "http://argonne.pc.cc.cmu.edu:8000/nngarage/exp-download?name="
    SOURCE_URL = "http://argonne.pc.cc.cmu.edu:80/nngarage/exp-download?name="
    # TODO:find file first
    # download_file
    target_file = buildPath(filename, task_name, user_name)
    real_filename, _ = urllib.request.urlretrieve(SOURCE_URL + filename, target_file)
    print real_filename, target_file
    return target_file


def parse_weights(filename):
    try: 
        with open(filename, "r") as r:
            for line in r:
                line = line.rstrip()
                tokens = line.split(",")
                ret = []
                for token in tokens:
                    ret.append(int(token))
                return ret
    except:
        return None

# def run_mlp_test(h_weights=[], test="", model_path="", o_dim=2, output=""):
def run_exp(name="", user_name="", weights="", train="", test=""):
    weights_path = file_manager(weights, name, user_name)
    train_path = file_manager(train, name, user_name)
    test_path = file_manager(test, name, user_name)

    print "Start training..."
    # train
    weights = parse_weights(weights_path)
    if weights == None:
        register_openers()
        datagen, headers = multipart_encode({"token":"lafyyjveotnehialteikeniotjim", "username":user_name, "name":name, "status":"Failed"})
        request = urllib2.Request("http://argonne.pc.cc.cmu.edu:80/nngarage/get-task-update", datagen, headers)
        urllib2.urlopen(request)
        return
	
    print "weights: "
    print weights
    model_output = buildPath("model.ckpt", name, user_name)
    weights_output = buildPath("weights.pckl", name, user_name)
    train_output = buildPath("train_output.txt", name, user_name)
    test_output = buildPath("test_output.txt", name, user_name)

    train_thread = Thread(target=run_mlp_train, args=(weights, 5000, train_path, 2, model_output, weights_output, train_output))
    train_thread.start()
    train_thread.join()

    print "Start testing..."
    test_thread = Thread(target=run_mlp_test, args=(weights, test_path, model_output, 2, test_output))
    test_thread.start()
    test_thread.join()

    register_openers()
    datagen, headers = multipart_encode({"token":"lafyyjveotnehialteikeniotjim", "username":user_name, "name":name, "model": open(model_output, "rb"), "train_out": open(train_output, "rb"), "test_out": open(test_output, "rb"), "status":"Completed"})
    request = urllib2.Request("http://argonne.pc.cc.cmu.edu:80/nngarage/get-task-update", datagen, headers)
    # Actually do the request, and get the response
    urllib2.urlopen(request)

@app.route("/tensor/run", methods=['POST'])
def run():
    if request.method == 'POST':
        task_name = request.form["task_name"]
        user_name = request.form["user_name"]
        weights = request.form["weights"]
        train = request.form["train"]
        test = request.form["test"]
        print test, train, weights, task_name
        try:
          tensor_thread = Thread(target=run_exp, args=(task_name, user_name, weights, train, test))
          tensor_thread.daemon = True
          tensor_thread.start()
        except:
          print "Spwan thread fail..."
          return "wrong"
    return "done"

@app.route("/")
def hello():
    process = Popen(['python', 'minist.py'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout

if __name__ == "__main__":
#    print file_manager("1.png", "tasks1", "user1")
    app.run(host='legend02.pc.cc.cmu.edu', port=53026)
    #app.run(port=int("8000"))
