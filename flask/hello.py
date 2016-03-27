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

app = Flask(__name__)

def buildPath(filename, task_name, user_name):
    return "files/" + user_name + "_" + task_name + "_" + filename

def file_manager(filename="", task_name="", user_name="", filepath="files/"):
    #SOURCE_URL = "http://argonne.pc.cc.cmu.edu:8000/nngarage/exp-download?name="
    SOURCE_URL = "http://localhost:8000/nngarage/exp-download?name="
    # TODO:find file first
    # download_file
    target_file = buildPath(filename, task_name, user_name)
    real_filename, _ = urllib.request.urlretrieve(SOURCE_URL + filename, target_file)
    return target_file

# def run_mlp(
# 	hidden_weights = [12],
# 	lr = 0.002,
# 	num_iter = 5,
# 	train_dir = "",
# 	test_dir = "",
# 	output_dim = 2,
# 	saved_model_path = "model.ckpt",
# 	saved_weights_path = "weights.pckl",
# 	mode = "train",
# 	output_file = "out_file",
# 	opt = "user_data"):

def run_exp(name="", user_name="", weights="", train="", test=""):
    #weights_path = file_manager(weights, name, user_name)
    #train_path = file_manager(train, name, user_name)
    #test_path = file_manager(test, name, user_name)

    print "Start training..."
    # train
    model_output = buildPath("model.ckpt", name, user_name)
    weights_output = buildPath("weights.pckl", name, user_name)
    output = buildPath("output.txt", name, user_name)
    run_mlp(hidden_weights=[5,6], num_iter=5000, train_dir="sample_train.txt", output_dim=2, mode="train", saved_model_path="1", saved_weights_path="2", output_file="3")
    # train_thread = Thread(target=run_mlp, args=(weights_path, 5000, train_path, 2, "train", model_output, weights_output, output))
    # train_thread.start()
    # train_thread.join()

    # process = Popen(['python', 'run_demo.py'], stdout=PIPE, stderr=PIPE)
    # _, _ = process.communicate()

    print "Start testing..."
    # test
    # process = Popen(['python', 'run_demo.py'], stdout=PIPE, stderr=PIPE)
    # _, _ = process.communicate()

    # upload


@app.route("/tensor/run", methods=['POST'])
def run():
    if request.method == 'POST':
        task_name = request.form["name"]
        weights = request.form["weights"]
        train = request.form["train"]
        test = request.form["test"]
        print test, train, weights, task_name
        try:
          tensor_thread = Thread(target=run_exp, args=())
          tensor_thread.daemon = True
          tensor_thread.start()
          #thread.start_new_thread(run_exp, (task_name, weights, train, test,))
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
    app.run(port=int("5001"))
