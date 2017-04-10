import os
import sys
import time
import tensorflow as tf
from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets

mnist = read_data_sets("data", one_hot=True, reshape=False, validation_size=0)

class batch_norm(object):
    def __init__(self, epsilon=1e-5, momentum=0.9, name="batch_norm"):
        with tf.variable_scope(name):
            self.epsilon = epsilon
            self.momentum = momentum
            self.name = name

    def __call__(self, x, train=True):
        return tf.contrib.layers.batch_norm(x,
                          decay=self.momentum,
                          updates_collections=None,
                          epsilon=self.epsilon,
                          scale=True,
                          is_training=train,
                          scope=self.name)

if __name__ == '__main__':
    # input image
    x = tf.placeholder(tf.float32, [None, 28, 28, 1])
    # labels
    y_ = tf.placeholder(tf.float32, [None, 10])
    # weight and bias
    w1 = tf.Variable(tf.truncated_normal([784, 300], stddev=0.1))
    b1 = tf.Variable(tf.ones([300])/10.0)
    bn = batch_norm(name="layer1")
    y1 = tf.nn.relu(bn(tf.matmul(tf.reshape(x, [-1, 784]), w1) + b1))
    # y1 = tf.nn.dropout(y1, 0.5) 
    w2 = tf.Variable( tf.truncated_normal([300, 10], stddev=0.1))
    b2 = tf.Variable(tf.ones([10])/10.0)
    bn2 = batch_norm(name="layer2")
    y = tf.nn.softmax(bn2(tf.matmul(y1, w2) + b2))
    loss = -tf.reduce_sum(y_ * tf.log(y))
    # compare
    is_correct = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    # count accuracy
    accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
    # optimize
    optimizer = tf.train.GradientDescentOptimizer(0.003)
    train_step = optimizer.minimize(loss)
    # init and gpu options
    init = tf.global_variables_initializer()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.2)
    config = tf.ConfigProto(gpu_options=gpu_options, allow_soft_placement=True)
    sess = tf.Session(config=config)
    sess.run(init)
    test_x, test_y = mnist.test.images, mnist.test.labels
    max_tac = 0
    for i in range(50000):
        batch_x, batch_y = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x:batch_x, y_:batch_y})
        if i % 500 == 0:
            ac, l = sess.run([accuracy, loss], feed_dict={x:batch_x, y_:batch_y})
            tac = sess.run(accuracy, feed_dict={x:test_x, y_:test_y})
            if max_tac - tac > 0.2:
                break
            if tac > max_tac:
                max_tac = tac
            print("accuracy is %f, loss is %f. test accuracy is %f" % (ac, l, tac))

