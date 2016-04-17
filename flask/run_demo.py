'''
	run_mlp:
	when load a model, need to specify the shape of model
'''

import tensorflow as tf
import numpy as np
import input_data
import sys, json

class INPUT_FLAG:
	def __init__(self):
		self.input_dim, self.trX, self.trY, self.teX, self.teY = \
		None, None, None, None, None

def update_data_flag(
	input_flag,
	train_dir = "",
	test_dir = "",
	opt = "",
	output_dim = 2,
	mode = "train"):

	if opt == "mnist" or opt == "MNIST":
		mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
		input_flag.trX, input_flag.trY, input_flag.teX, input_flag.teY = \
		mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels
	else:
		if mode == "train":
			try:
				train_data = np.loadtxt(open(train_dir,"rb"), delimiter=",", dtype=float)
			except:
				train_data = np.loadtxt(open(train_dir,"rb"), delimiter=" ", dtype=float)
			input_flag.trX, input_flag.trY = train_data[:, :-1], train_data[:, -1]
			input_flag.trY.astype(int)
			temp_tr = np.zeros((len(input_flag.trY), output_dim))
			for i in range(len(input_flag.trY)):
				temp_tr[i, input_flag.trY[i]] = 1
			input_flag.trY = temp_tr
			input_flag.teX, input_flag.teY = input_flag.trX, input_flag.trY
		elif mode == "test":
			try:
				test_data = np.loadtxt(open(test_dir,"rb"), delimiter=",", dtype=float)
			except:
				test_data = np.loadtxt(open(test_dir,"rb"), delimiter=" ", dtype=float)
			input_flag.teX, input_flag.teY = test_data[:, :-1], test_data[:, -1]
			input_flag.teY.astype(int)
			temp_te = np.zeros((len(input_flag.teY), output_dim))
			for i in range(len(input_flag.teY)):
				temp_te[i, input_flag.teY[i]] = 1
			input_flag.teY = temp_te
	input_flag.input_dim = np.size(input_flag.teX, 1)

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def model(X, input_dim, hidden_param, output_dim, activation_func = "relu"):
	w_h, bias = [None] * len(hidden_param), [None] * (len(hidden_param) + 1)
	w_h[0] = init_weights([input_dim, hidden_param[0]])
	bias[0] = init_weights([hidden_param[0]])
	for i in range(1, len(hidden_param)):
		w_h[i] = init_weights([hidden_param[i-1], hidden_param[i]])
		bias[i] = init_weights([hidden_param[i]])
	
        print hidden_param[-1], type(hidden_param[-1])
        print output_dim, type(output_dim)
	w_o = init_weights([hidden_param[-1], output_dim])
	bias[-1] = init_weights([output_dim])
	
	def activation(act_func, X, hidden_param, w_h, w_o, bias):
		a = act_func(tf.matmul(X, w_h[0]) + bias[0])
		for i in range(1, len(hidden_param)):
			a = act_func(tf.matmul(a, w_h[i]) + bias[i])
		return tf.matmul(a, w_o) + bias[-1]

	if activation_func == "relu":
		return (w_h, w_o, activation(tf.nn.relu, X, hidden_param, w_h, w_o, bias))
	elif activation_func == "sigmoid":
		return (w_h, w_o, activation(tf.nn.sigmoid, X, hidden_param, w_h, w_o, bias))



'''
	warning: when run XOR experiment, num_iter should be large
'''
def run_mlp(
	hidden_weights = [12], 
	lr = 0.003, 
	num_iter = 5, 
	train_dir = "",
	test_dir = "",
	output_dim = 2,
	saved_model_path = "model.ckpt",
	saved_weights_path = "weights.json",
	mode = "train",
	output_file = "out_file",
	opt = "user_data"):

	input_flag = INPUT_FLAG()
	if opt == "mnist":
		output_dim = 11
		update_data_flag(input_flag, "", "", opt, output_dim)
	else:
		update_data_flag(input_flag, train_dir, test_dir, output_dim, mode = mode)

	trX, trY, teX, teY, input_dim = input_flag.trX, input_flag.trY, \
	input_flag.teX, input_flag.teY, input_flag.input_dim

	X = tf.placeholder("float", [None, input_dim])
	Y = tf.placeholder("float", [None, output_dim])
        
        print "I am in run_mlp"
        print "hidden_weights is ", hidden_weights, "output_dim is ", output_dim
	w_hs, w_o, activation = model(X, input_dim, hidden_weights, output_dim)

	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(activation, Y))
	# construct an optimizer, choice of learning rate
	optimizer = tf.train.RMSPropOptimizer(lr, 0.9).minimize(cost)

	saver = tf.train.Saver()
	sess = tf.Session()
	sess.run(tf.initialize_all_variables())

	out = open(output_file,'w')
	if mode == "test":
		saver.restore(sess, saved_model_path)
		out.write(str(np.mean(np.argmax(teY, axis=1) == \
			sess.run(tf.argmax(activation, 1), feed_dict={X: teX, Y: teY}))))
	elif mode == "train":
		for i in range(num_iter):
			if opt == "mnist" or opt == "MNIST":
				for start, end in zip(range(0, len(trX), 50), range(50, len(trX), 50)):\
				sess.run(optimizer, feed_dict={X: trX[start:end], Y: trY[start:end]})
			else:
				sess.run(optimizer, feed_dict={X: trX, Y: trY})
			out.write(str(i) + ": "+ str(np.mean(np.argmax(trY, axis=1) == \
				sess.run(tf.argmax(activation, 1), feed_dict={X: trX, Y: trY})))+"\n")
			# print i,"'th loss: ",sess.run(cost, feed_dict={X: trX, Y: trY})
		# save session
		saver.save(sess, saved_model_path)
		# save weights as json
		weights = sess.run(w_hs)
		weights.append(sess.run(w_o))
		for i in range(len(weights)):
			weights[i] = weights[i].tolist()
		# print weights
		with open(saved_weights_path, 'w') as f:
			json.dump({'weights':weights}, f)
	else:
		fsock = open('error.log', 'w')
		sys.stderr = fsock
		raise ValueError('Unidentified Option!')
	out.close()

def run_mlp_train(h_weights=[], lr = 0.001, it=500, train="", o_dim=2, model_path="", weights_path="", output=""):
	run_mlp(lr=lr, hidden_weights=h_weights, num_iter=it, train_dir=train, output_dim=o_dim, mode="train", saved_model_path=model_path, saved_weights_path=weights_path, output_file=output)

def run_mlp_test(h_weights=[], test="", model_path="", o_dim=2, output=""):
	run_mlp(hidden_weights=h_weights, test_dir=test, saved_model_path=model_path ,mode="test", output_dim=2, output_file=output)
	
def main():
	# # MNIST
	# hidden_weights = [300, 65, 20]
	# # train / test
	# run_mlp(
	# 	hidden_weights,
	# 	num_iter = 5,
	# 	mode = "test",
	# 	opt = "mnist",
	# 	saved_model_path = "model.ckpt",
	# output_file = "output.txt")

	# XOR

	# train
	run_mlp(
		hidden_weights = [3,5], 
		num_iter = 10, 
		train_dir = "sample_train.txt", 
		output_dim = 2,
		mode = "train",
		saved_model_path = "model.ckpt",
		saved_weights_path = "weights.json",
		output_file = "output.txt"
		)

	# # test
	# run_mlp(
	# 	hidden_weights = [6],
	# 	test_dir = "sample_train.txt",
	# 	saved_model_path = "model.ckpt",
	# 	output_dim = 2,
	# 	mode = "test",
	# 	output_file = "output.txt"
	# 	)

if __name__ == "__main__":
	main()
