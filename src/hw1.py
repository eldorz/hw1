"""
All tensorflow objects, if not otherwise specified, should be explicity
created with tf.float32 datatypes. Not specifying this datatype for variables and
placeholders will cause your code to fail some tests.

For the specified functionality in this assignment, there are generally high
level Tensorflow library calls that can be used. As we are assessing tensorflow,
functionality that is technically correct but implemented manually, using a
library such as numpy, will fail tests. If you find yourself writing 50+ line
methods, it may be a good idea to look for a simpler solution.

Along with the provided functional prototypes, there is another file,
"train.py" which calls the functions listed in this file. It trains the
specified network on the MNIST dataset, and then optimizes the loss using a
standard gradient decent optimizer. You can run this code to check the models
you create.

"""

import tensorflow as tf
import math

def input_placeholder():
    """
    This placeholder serves as the input to the model, and will be populated
    with the raw images, flattened into single row vectors of length 784.

    The number of images to be stored in the placeholder for each minibatch,
    i.e. the minibatch size, may vary during training and testing, so your
    placeholder must allow for a varying number of rows.

    :return: A tensorflow placeholder of type float32 and correct shape
    """
    return tf.placeholder(dtype=tf.float32, shape=[None, 784],
                          name="image_input")

def target_placeholder():
    """
    This placeholder serves as the output for the model, and will be
    populated with targets for training, and testing. Each output will
    be a single one-hot row vector, of length equal to the number of
    classes to be classified (hint: there's one class for each digit)

    The number of target rows to be stored in the placeholder for each
    minibatch, i.e. the minibatch size, may vary during training and
    testing, so your placeholder must allow for a varying number of
    rows.

    :return: A tensorflow placeholder of type float32 and correct shape
    """
    return tf.placeholder(dtype=tf.float32, shape=[None, 10],
                          name="image_target_onehot")

def onelayer(X, Y, layersize=10):
    """
    Create a Tensorflow model for logistic regression (i.e. single layer NN)

    :param X: The  input placeholder for images from the MNIST dataset
    :param Y: The output placeholder for image labels
    :return: The following variables should be returned  (variables in the
    python sense, not in the Tensorflow sense, although some may be
    Tensorflow variables). They must be returned in the following order.
        w: Connection weights
        b: Biases
        logits: The input to the activation function
        preds: The output of the activation function (a probability
        distribution over the 10 digits)
        batch_xentropy: The cross-entropy loss for each image in the batch
        batch_loss: The average cross-entropy loss of the batch
    """
    x_size = X.get_shape()[1].value
    
    # he initialisation, var(W) = 2 / n(in)
    var = 2 / x_size
    std_dev = math.sqrt(var) 

    w = tf.Variable(tf.random_normal([x_size, layersize], stddev = std_dev),
        name = "weights", 
        dtype = tf.float32)
    b = tf.Variable(tf.zeros([layersize]), name = "biases", dtype = tf.float32)
    logits = tf.matmul(X, w) + b
    batch_xentropy = tf.losses.softmax_cross_entropy(
        onehot_labels = Y,
        logits = logits)
    batch_loss = tf.reduce_mean(batch_xentropy)
    preds = tf.nn.softmax(logits)

    return w, b, logits, preds, batch_xentropy, batch_loss

def twolayer(X, Y, hiddensize=30, outputsize=10):
    """
    Create a Tensorflow model for a Neural Network with one hidden layer

    :param X: The  input placeholder for images from the MNIST dataset
    :param Y: The output placeholder for image labels
    :return: The following variables should be returned in the following order.
        W1: Connection weights for the first layer
        b1: Biases for the first layer
        W2: Connection weights for the second layer
        b2: Biases for the second layer
        logits: The inputs to the activation function
        preds: The outputs of the activation function (a probability
        distribution over the 10 digits)
        batch_xentropy: The cross-entropy loss for each image in the batch
        batch_loss: The average cross-entropy loss of the batch
    """
    x_size = X.get_shape()[1].value

    # he initialisation, var(W) = 2 / n(in)
    var1 = 2 / x_size
    std_dev1 = math.sqrt(var1)
    var2 = 2 / hiddensize
    std_dev2 = math.sqrt(var2) 

    w1 = tf.Variable(
        tf.random_normal([x_size, hiddensize], stddev = std_dev1), 
        name = "layer_1_weights", dtype = tf.float32)
    b1 = tf.Variable(tf.zeros([hiddensize]), 
        name = "layer_1_biases", dtype = tf.float32)
    w2 = tf.Variable(
        tf.random_normal([hiddensize, outputsize], stddev = std_dev2), 
        name = "layer_2_weights", dtype = tf.float32)
    b2 = tf.Variable(tf.zeros([outputsize]), 
        name = "layer_2_biases", dtype = tf.float32)
    layer1_activation = tf.matmul(X, w1) + b1
    layer1_output = tf.nn.relu(layer1_activation)
    logits = tf.matmul(layer1_output, w2) + b2
    batch_xentropy = tf.losses.softmax_cross_entropy(
        onehot_labels = Y,
        logits = logits)
    batch_loss = tf.reduce_mean(batch_xentropy)
    preds = tf.nn.softmax(logits)
    return w1, b1, w2, b2, logits, preds, batch_xentropy, batch_loss

def convnet(X, Y, convlayer_sizes=[10, 10], \
        filter_shape=[3, 3], outputsize=10, padding="same"):
    """
    Create a Tensorflow model for a Convolutional Neural Network. The network
    should be of the following structure:
    conv_layer1 -> conv_layer2 -> fully-connected -> output

    :param X: The  input placeholder for images from the MNIST dataset
    :param Y: The output placeholder for image labels
    :return: The following variables should be returned in the following order.
        conv1: A convolutional layer of convlayer_sizes[0] filters of shape filter_shape
        conv2: A convolutional layer of convlayer_sizes[1] filters of shape filter_shape
        w: Connection weights for final layer
        b: biases for final layer
        logits: The inputs to the activation function
        preds: The outputs of the activation function (a probability
        distribution over the 10 digits)
        batch_xentropy: The cross-entropy loss for each image in the batch
        batch_loss: The average cross-entropy loss of the batch

    hints:
    1) consider tf.layer.conv2d
    2) the final layer is very similar to the onelayer network. Only the input
    will be from the conv2 layer. If you reshape the conv2 output using tf.reshape,
    you should be able to call onelayer() to get the final layer of your network
    """
    image_x = X.get_shape()[1].value
    image_y = X.get_shape()[2].value
    conv1 = tf.layers.conv2d(
        inputs = X,
        filters = convlayer_sizes[0],
        kernel_size = filter_shape,
        padding = "same",
        activation = tf.nn.relu,
        name = "conv1")
    conv2 = tf.layers.conv2d(
        inputs = conv1,
        filters = convlayer_sizes[1],
        kernel_size = filter_shape,
        padding = "same",
        activation = tf.nn.relu,
        name = "conv2")
    conv2_vector = tf.reshape(conv2, 
        [-1, image_x * image_y * convlayer_sizes[1]])
    w, b, logits, preds, batch_xentropy, batch_loss = onelayer(conv2_vector, Y, 
        outputsize)

    return conv1, conv2, w, b, logits, preds, batch_xentropy, batch_loss 

def train_step(sess, batch, X, Y, train_op, loss_op, summaries_op):
    """
    Run one step of training.

    :param sess: the current session
    :param batch: holds the inputs and target outputs for the current minibatch
    batch[0] - array of shape [minibatch_size, 784] with each row holding the
    input images
    batch[1] - array of shape [minibatch_size, 10] with each row holding the
    one-hot encoded targets
    :param X: the input placeholder
    :param Y: the output target placeholder
    :param train_op: the tensorflow operation that will run one step of training
    :param loss_op: the tensorflow operation that will return the loss of your
    model on the batch input/output

    :return: a 3-tuple: train_op_result, loss, summary
    which are the results of running the train_op, loss_op and summaries_op
    respectively.
    """
    train_result, loss, summary = \
        sess.run([train_op, loss_op, summaries_op], feed_dict={X: batch[0], Y: batch[1]})
    return train_result, loss, summary
