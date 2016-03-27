import numpy as np
import tensorflow as tf


saved_model_path = "model.ckpt"

# x = tf.placeholder(tf.float32)
# y = tf.placeholder(tf.float32)

w = tf.Variable(tf.zeros([1, 1], dtype=tf.float32))
b = tf.Variable(tf.ones([1, 1], dtype=tf.float32))
# y_hat = tf.add(b, tf.matmul(x, w))

saver = tf.train.Saver()  # defaults to saving all variables - in this case w and b

with tf.Session() as sess:
    # Here's where you're restoring the variables w and b.
    # Note that the graph is exactly as it was when the variables were
    # saved in a prior training run.
    ckpt = tf.train.get_checkpoint_state(saved_model_path)
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
    else:
        print "...no checkpoint found..."


# # Create some variables.
# v1 = tf.Variable(..., name="v1")
# v2 = tf.Variable(..., name="v2")
# ...
# # Add ops to save and restore all the variables.
# saver = tf.train.Saver()

# # Later, launch the model, use the saver to restore variables from disk, and
# # do some work with the model.
# with tf.Session() as sess:
#   # Restore variables from disk.
#   saver.restore(sess, "/tmp/model.ckpt")
#   print("Model restored.")
#   # Do some work with the model