from flask import Flask
from flask import request
import tensorflow as tf
import numpy as np
import input_data
from util import *
from subprocess import Popen, PIPE
from six.move import urllib

app = Flask(__name__)

def file_manager(filename="", filepath="files/"):
    SOURCE_URL = "http://argonne.pc.cc.cmu.edu:8000/nngarage/exp-download?name="
    # TODO:find file first
    # download_file
    real_filename, _ = urllib.request.urlretrieve(SOURCE_URL + filename, filepath)
    return filepath + real_filename

def run_exp(name, weights, train, test):
    weights_path = file_manager(weights)
    train_path = file_manager(train)

    # train
    process = Popen(['python', 'minist.py'], stdout=PIPE, stderr=PIPE)
    _, _ = process.communicate()

    # test
    process = Popen(['python', 'minist.py'], stdout=PIPE, stderr=PIPE)
    _, _ = process.communicate()


@app.route("/tensor/run", methods=['POST'])
def run():
    if request.method == 'POST':
        task_name = request.form["name"]
        weights = request.form["weights"]
        train = request.form["p1"]
        test = request.form["p2"]
        try:
          thread.start_new_thread(run_exp, (name, weights, train, test, ))
        except:
          return "wrong"
    return "done"

@app.route("/")
def hello():
    process = Popen(['python', 'minist.py'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout

if __name__ == "__main__":
    app.run(port=int("5001"))
