from __future__ import print_function

import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
from custom_lstm import CustomBasicLSTMCell
import numpy as np

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

'''
To classify images using a reccurent neural network, we consider every image
row as a sequence of pixels. Because MNIST image shape is 28*28px, we will then
handle 28 sequences of 28 steps for every sample.
'''

# Parameters
learning_rate = 0.001
training_iters = 1000#100000
batch_size = 128
display_step = 10

# Network Parameters
n_input = 28 # MNIST data input (img shape: 28*28)
n_steps = 28 # timesteps
n_hidden = 15 # hidden layer num of features
n_classes = 10 # MNIST total classes (0-9 digits)

# tf Graph input
x = tf.placeholder("float", [None, n_steps, n_input])
y = tf.placeholder("float", [None, n_classes])

# Define weights
weights = tf.Variable(tf.random_normal([n_hidden, n_classes]))

biases = tf.Variable(tf.random_normal([n_classes]))





# Prepare data shape to match `rnn` function requirements
# Current data input shape: (batch_size, n_steps, n_input)
# Required shape: 'n_steps' tensors list of shape (batch_size, n_input)

# Permuting batch_size and n_steps
xi = tf.transpose(x, [1, 0, 2 ])
    # Reshaping to (n_steps*batch_size, n_input)
xi = tf.reshape(xi, [-1, n_input])

# Split to get a list of 'n_steps' tensors of shape (batch_size, n_input)
xi = tf.split(0, n_steps, xi)


yi = y    
# Define a lstm cell with tensorflow
#lstm_cell = rnn_cell.BasicLSTMCell(n_hidden, forget_bias=1.0)
lstm_cell = CustomBasicLSTMCell(n_hidden)
# Get lstm cell output
outputs, final_state = rnn.rnn(lstm_cell, xi, dtype=tf.float32)
#h_fc1_reshaped = tf.reshape(h_fc1, [1,-1,256])
#xi = tf.reshape(xi,[128,-1,28])
#outputs, states = tf.nn.dynamic_rnn(lstm_cell, xi, sequence_length = n_steps,dtype=tf.float32)
# Linear activation, using rnn inner loop last output
#return tf.matmul(outputs[-1], weights[ 'out']) + biases['out']

#pred = RNN(x, weights, biases)
pred = tf.matmul(outputs[-1], weights) + biases
# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
#optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

#using tf.gradients:

#params = [weights,biases,lstm_cell.matrix,lstm_cell.bias]
#params = tf.trainable_variables()
gradient = tf.gradients(cost,params)
opt = tf.train.AdamOptimizer(learning_rate)
optimizer = opt.apply_gradients(zip(gradient,params))

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initializing the variables
init = tf.initialize_all_variables()

# Launch the graph
sess = tf.InteractiveSession()
sess.run(init)
step = 1
counter = 0

# Keep training until reach max iterations
while counter < 50:#step * batch_size < training_iters:
    batch_x, batch_y = mnist.train.next_batch(batch_size)
    r ,c= batch_x.shape
    print(counter)
    counter += 1
    # Reshape data to get 28 seq of 28 elements
    batch_x = batch_x.reshape((batch_size, n_steps, n_input))
    # Run optimization op (backprop)
    sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
    if step % display_step == 0:
        # Calculate batch accuracy
        acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y})
        # Calculate batch loss
        loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y})
        print("Iter " + str(step*batch_size) + ", Minibatch Loss= " + \
        "{:.6f}".format(loss) + ", Training Accuracy= " + \
        "{:.5f}".format(acc))
        step += 1
        
        
print("Optimization Finished!")

# Calculate accuracy for 128 mnist test images
test_len = 128
test_data = mnist.test.images[:test_len].reshape((-1, n_steps, n_input))
test_label = mnist.test.labels[:test_len]
print("Testing Accuracy:", \
sess.run(accuracy, feed_dict={x: test_data, y: test_label}))


if True:
    a_inputs = sess.run(xi, feed_dict={x: batch_x, y: batch_y})

    a_lstm_cell_output = sess.run(outputs, feed_dict={x: batch_x, y: batch_y})

    a_lstm_cell_output = sess.run(outputs[-1], feed_dict={x: batch_x, y: batch_y})    
    a_lstm_states = sess.run(final_state, feed_dict={x: batch_x, y: batch_y})

    a_outputs = batch_y


