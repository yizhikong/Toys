import os
import sys
import time
import tensorflow as tf
from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets

mnist = read_data_sets("data", one_hot=True, reshape=False, validation_size=0)

if __name__ == '__main__':
    # input image
    x = tf.placeholder(tf.float32, [None, 28, 28, 1])
    # labels
    y_ = tf.placeholder(tf.float32, [None, 10])
    # weight and bias
    w = tf.Variable( tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    # output
    y = tf.nn.softmax(tf.matmul(tf.reshape(x, [-1, 784]), w ) + b)
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
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.1)
    config = tf.ConfigProto(gpu_options=gpu_options, allow_soft_placement=True)
    sess = tf.Session(config=config)
    sess.run(init)
    test_x, test_y = mnist.test.images, mnist.test.labels
    for i in range(2000):
        batch_x, batch_y = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x:batch_x, y_:batch_y})
        if i % 200 == 0:
            ac, l = sess.run([accuracy, loss], feed_dict={x:batch_x, y_:batch_y})
            tac = sess.run(accuracy, feed_dict={x:test_x, y_:test_y})
            print("accuracy is %f, loss is %f. test accuracy is %f" % (ac, l, tac))

