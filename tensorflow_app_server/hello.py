from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! -- from TensorFlow application server in BIC\'s Yahoo Cluster'

@app.route('/run_net_proc')
def run_net_proc():
    # TODO: Perform tensor flow
    print request.args.get('data')
    return "The result"

if __name__ == '__main__':
    app.run()
