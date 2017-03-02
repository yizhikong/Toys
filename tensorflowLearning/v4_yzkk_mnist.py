import os
import sys
import time
import math
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
    x = tf.placeholder(tf.float32, [None, 28, 28, 1], name='input_image')
    # labels
    y_ = tf.placeholder(tf.float32, [None, 10], name='label')
    # weight and bias
    with tf.name_scope('conv1'):
        w1 = tf.Variable(tf.truncated_normal([6, 6, 1, 6], stddev=0.1), name='w1')
        b1 = tf.Variable(tf.ones([6])/10.0, name='b1')
        tf.summary.histogram('w1', w1)
        bn1 = batch_norm(name="layer1")
        cy1 = tf.nn.conv2d(x, w1, strides=[1,2,2,1], padding='SAME') + b1
        y1 = tf.nn.relu(tf.nn.dropout(bn1(cy1), 1))
        print(y1.get_shape())
    # layer2, y1 is 14x14
    with tf.name_scope('conv2'):
        w2 = tf.Variable(tf.truncated_normal([5, 5, 6, 12], stddev=0.1), name='w2')
        b2 = tf.Variable(tf.ones([12])/10.0, name='b2')
        tf.summary.histogram('w2', w2)
        bn2 = batch_norm(name="layer2")
        cy2 = tf.nn.conv2d(y1, w2, strides=[1,2,2,1], padding='SAME') + b2
        y2 = tf.nn.relu(tf.nn.dropout(bn2(cy2), 1))
        print(y2.get_shape())
    # layer3, y2 is 7x7
    with tf.name_scope('conv3'):
        w3 = tf.Variable(tf.truncated_normal([3, 3, 12, 24], stddev=0.1), name='w3')
        b3 = tf.Variable(tf.ones([24])/10.0, name='b3')
        tf.summary.histogram('w3', w3)
        bn3 = batch_norm(name="layer3")
        cy3 = tf.nn.conv2d(y2, w3, strides=[1,1,1,1], padding='SAME') + b3
        y3 = tf.nn.relu(tf.nn.dropout(bn3(cy3), 1))
        print(y3.get_shape())
        y3 = tf.reshape(y3, [-1, 7*7*24])
    # full connect
    with tf.name_scope('full_connect1'):
        w4 = tf.Variable(tf.truncated_normal([7*7*24, 200], stddev=0.1), name='w4')
        b4 = tf.Variable(tf.ones([200])/10.0, name='b4')
        bn4 = batch_norm(name="layer4")
        y4 = tf.nn.relu(tf.nn.dropout(bn4(tf.matmul(y3, w4) + b4), 1))
        print(y4.get_shape()) 
    with tf.name_scope('full_connect2'):
        w5 = tf.Variable(tf.truncated_normal([200, 10], stddev=0.1), name='w5')
        b5 = tf.Variable(tf.ones([10])/10.0, name='b5')
        bn5 = batch_norm(name="layer5")
        y = tf.nn.softmax(tf.nn.dropout(bn5(tf.matmul(y4, w5) + b5), 1))
        print(y.get_shape())
        loss = -tf.reduce_sum(y_ * tf.log(y))
    tf.summary.scalar('loss', loss)
    # compare
    is_correct = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    # count accuracy
    accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
    tf.summary.scalar('accuracy', accuracy)
    # optimize
    max_lr = 0.003
    min_lr = 0.0001
    lr = tf.placeholder(tf.float32)
    optimizer = tf.train.AdamOptimizer(lr)
    train_step = optimizer.minimize(loss)
    # init and gpu options
    init = tf.global_variables_initializer()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.2)
    config = tf.ConfigProto(gpu_options=gpu_options, allow_soft_placement=True)
    merge = tf.summary.merge_all()
    sess = tf.Session(config=config)
    summary_writer = tf.summary.FileWriter('../logs', sess.graph)
    sess.run(init)
    test_x, test_y = mnist.test.images, mnist.test.labels
    max_tac = 0
    for i in range(5000):
        batch_x, batch_y = mnist.train.next_batch(100)
        learning_rate = min_lr + (max_lr - min_lr) * math.exp(-i/5000.0) 
        sess.run(train_step, feed_dict={x:batch_x, y_:batch_y, lr:learning_rate})
        s, ac, l = sess.run([merge, accuracy, loss], feed_dict={x:batch_x, y_:batch_y})
        summary_writer.add_summary(s, i)
        if i % 500 == 0:
            tac = sess.run(accuracy, feed_dict={x:test_x, y_:test_y})
            if max_tac - tac > 0.2:
                break
            if tac > max_tac:
                max_tac = tac
            print("accuracy is %f, loss is %f. test accuracy is %f" % (ac, l, tac))

