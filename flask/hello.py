from flask import Flask
from flask import request
import tensorflow as tf
import numpy as np
import input_data
from util import *
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route("/tensor", methods=['GET'])
def tensor():
    print "start"
    return "done"

@app.route("/")
def hello():
    process = Popen(['python', 'minist.py'], stdout=PIPE, stderr=PIPE) 
    stdout, stderr = process.communicate()
    return stdout	

if __name__ == "__main__":
    app.run(port=int("5001"))
