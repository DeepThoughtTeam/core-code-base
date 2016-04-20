import numpy as np
import tensorflow as tf
import os, pickle

def one_hot(y, output_dim):
	oh_y = np.zeros((len(y), output_dim))
	for i in range(len(y)):
		oh_y[i, int(y[i])] = 1
	return oh_y

def parse_input(input_file="data/param.txt"):
	try:
		train_data = np.loadtxt(open(input_file,"rb"), delimiter=",", dtype=float)
	except:
		train_data = np.loadtxt(open(input_file,"rb"), delimiter=" ", dtype=float)
	return train_data[:, :-1], one_hot(train_data[:,-1], 2)

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.1))

def model(X, input_dim, hidden_weights, output_dim, act_func = tf.nn.relu):
	w_h, bias = [None] * len(hidden_weights), [None] * (len(hidden_weights) + 1)
	w_h[0] = init_weights([input_dim, hidden_weights[0]])
	bias[0] = init_weights([hidden_weights[0]])
	for i in range(1, len(hidden_weights)):
		w_h[i] = init_weights([hidden_weights[i-1], hidden_weights[i]])
		bias[i] = init_weights([hidden_weights[i]])
	w_o = init_weights([hidden_weights[-1], output_dim])
	bias[-1] = init_weights([output_dim])
	
	acs = []
	a = act_func(tf.matmul(X, w_h[0]) + bias[0])
	acs.append(a)
	for i in range(1, len(hidden_weights)):
		a = act_func(tf.matmul(a, w_h[i]) + bias[i])
		acs.append(a)
	acs.append(act_func(tf.matmul(a, w_o) + bias[-1]))	
	return (w_h, w_o, tf.matmul(a, w_o) + bias[-1], acs)

def mlp(
	train_x = None,
	train_y = None,
	test_x = None,
	test_y = None,
	hidden_weights = [3],
	output_dim = 2,
	lr = 0.01,
	num_iter= 10,
	saved_model_path = "model.ckpt",
	saved_weights_path = "weights.json",
	out_file = 'output',
	mode = "train"
	):

	if mode=="train":
		input_dim = train_x.shape[1]
	elif mode=="test":
		input_dim = test_x.shape[1]
	X = tf.placeholder("float", [None, input_dim])
	Y = tf.placeholder("float", [None, output_dim])
	w_hs, w_o, activation, acs = model(X, input_dim, hidden_weights, output_dim)
	cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(activation, Y))
	optimizer = tf.train.RMSPropOptimizer(lr, 0.9).minimize(cost)
	saver = tf.train.Saver()
	sess = tf.Session()
	sess.run(tf.initialize_all_variables())
	out = open(out_file, 'w')
	if mode == "train":
		for i in range(num_iter):
			sess.run(optimizer, feed_dict={X:train_x , Y:train_y})
			print i,":",sess.run(cost, feed_dict={X: train_x, Y: train_y})
		saver.save(sess, saved_model_path)
		weights = sess.run(w_hs)
		weights.append(sess.run(w_o))
		for i in range(len(weights)):
			weights[i] = weights[i].T.tolist()
		# print weights 
		with open(saved_weights_path, 'w') as f:
			pickle.dump(weights, f)

		# remove unnecessary files
		os.remove(saved_model_path+".meta")
		os.remove("checkpoint")

		correct_prediction = tf.equal(tf.argmax(activation, 1), tf.argmax(Y, 1))
		acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
		out.write("training acc: " + str(sess.run(acc, feed_dict={X: train_x, Y: train_y})))
	elif mode == "test":
		print "start testing ... \n"
		saver.restore(sess, "model.ckpt")
		activations = sess.run(acs, feed_dict={X: test_x, Y: test_y})
		out.write("testing accuracy: " + str(np.mean(np.argmax(test_y, axis=1) == \
			np.argmax(activations[-1], 1))) + "\n")
		activations[-1] = np.maximum(activations[-1], 0)
		out.write("hidden layers setting: " + ' '.join(str(i) for i in hidden_weights) + '\n\n')
		out.write("################## activations ################## \n")
		out.write("* each row corresponds to one instance  \n\n")
		for i in range(len(activations)):
			if i != len(activations)-1:
				out.write("hidden layer %d: \n" % i)
			else:	
				out.write("output layer: \n")
			np.savetxt(out, activations[i], fmt='%0.3f')
			out.write('\n')
	out.close()



def run_mlp_train(h_weights=[], lr = 0.001, it=500, train="", o_dim=2, model_path="", weights_path="", output=""):
	x, y = parse_input(train)
	mlp(train_x = x,
		train_y = y,
		lr=lr, 
		hidden_weights=h_weights, 
		num_iter=it, 
		output_dim=o_dim, 
		saved_model_path=model_path, 
		saved_weights_path=weights_path, 
		out_file=output,
		mode="train"
		)

def run_mlp_test(h_weights=[], test="", model_path="", o_dim=2, output=""):
	x, y = parse_input(test)
	mlp(
		test_x = x,
		test_y = y,
		hidden_weights=h_weights, 
		output_dim=o_dim, 
		saved_model_path=model_path, 
		out_file=output,
		mode="test"
		)

def main():
	data_dir = "data/diamod_train.txt"
 
	# # train
	# run_mlp_train(
	# h_weights=[5,5], 
	# 	lr=0.01, 
	# 	it=1000, 
	# 	train=data_dir, 
	# 	o_dim=2, 
	# 	model_path="model.ckpt", 
	# 	weights_path="weights.json", 
	# 	output="output"
	# 	)
	
	# test
	run_mlp_test(
		h_weights=[5,5], 
		test=data_dir, 
		model_path="model.ckpt", 
		o_dim=2, 
		output="output")

if __name__ == "__main__":
	main()
