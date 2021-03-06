def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def model(X, w_hs, w_o):
    h = tf.nn.sigmoid(tf.matmul(X, w_hs[0])) # this is a basic mlp, think 2 stacked logistic regressions
    for w_h in w_hs[1:]:
    	h = tf.nn.sigmoid(tf.matmul(h, w_h))
    return tf.matmul(h, w_o) # note that we dont take the softmax at the end because our cost fn does that for u

def run_mlp(input_weight = [10]):
	mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
	trX, trY, teX, teY = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels

	X = tf.placeholder("float", [None, 784])
	Y = tf.placeholder("float", [None, 10])

	w_hs = []
	w_hs.append(init_weights([784, input_weight[0]]))
	for i in xrange(len(input_weight)-1):
		w_hs.append(init_weights([input_weight[i], input_weight[i+1]]))

	w_o = init_weights([input_weight[-1], 10])

	py_x = model(X, w_hs, w_o)

	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y)) # compute costs
	train_op = tf.train.GradientDescentOptimizer(0.05).minimize(cost) # construct an optimizer
	predict_op = tf.argmax(py_x, 1)

	sess = tf.Session()
	init = tf.initialize_all_variables()
	sess.run(init)

	for i in range(100):
	    for start, end in zip(range(0, len(trX), 128), range(128, len(trX), 128)):
	        sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end]})
	    print i, np.mean(np.argmax(teY, axis=1) ==
	                     sess.run(predict_op, feed_dict={X: teX, Y: teY}))
