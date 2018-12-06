# CODE IS MODIFIED FROM HERE  https://github.com/easy-tensorflow/easy-tensorflow/tree/master/6_Convolutional_Neural_Network/code
#----------------------------------------

import tensorflow as tf

import numpy as np

from ops import *
from utils import *
from Generate_ytrain import load_data


class Network():
    def __init__(self, restore=False):
        self.restore = restore

    def run_network(self):
        # Data Dimensions
        img_h = img_w = 4  # Puzzles are images are 4x4x26 images
        img_d = 26
        img_size_flat = img_h * img_w * img_d  # 4x4x26=416, the total number of pixels
        # Load MNIST data
        if not self.restore:
            x_train, y_train, x_valid, y_valid = load_data()
            print("Size of:")
            print("- Training-set:\t\t{}".format(len(y_train)))
            #print("- Validation-set:\t{}".format(len(y_valid)))

        # Hyper-parameters
        logs_path = "./logs"  # path to the folder that we want to save the logs for Tensorboard
        lr = 0.001  # The optimization initial learning rate
        epochs = 5  # Total number of training epochs
        batch_size = 50  # Training batch size
        display_freq = 1  # Frequency of displaying the training results

        # Network Configuration
        # 1st Convolutional Layer
        filter_size1 = 2  # Convolution filters are 5 x 5 pixels.
        num_filters1 = 100  # There are 16 of these filters.
        stride1 = 1  # The stride of the sliding window

        # 2nd Convolutional Layer
        filter_size2 = 4  # Convolution filters are 5 x 5 pixels.
        num_filters2 = 50  # There are 32 of these filters.
        stride2 = 1  # The stride of the sliding window

        # Fully-connected layer.
        h1 = 1000  # Number of neurons in fully-connected layer.

        # Create the network graph
        # Placeholders for inputs (x), outputs(y)
        with tf.name_scope('Input'):
            self.x = tf.placeholder(tf.float32, shape=[None, img_h, img_w, img_d], name='X')
            self.y = tf.placeholder(tf.float32, shape=[None, img_h, img_w, img_d], name='Y')

        layer_flat = flatten_layer(self.x)
        fc1 = fc_layer(layer_flat, 400, 'FC1', use_relu=True)
        fc2 = fc_layer(fc1, 400, 'FC2', use_relu=True)
        fc3 = fc_layer(fc2, 400, 'FC3', use_relu=True)
        output = fc_layer(fc3, img_size_flat, 'OUT', use_relu=False)
        z = tf.shape(self.y)
        output_logits = tf.reshape(output, z)
        '''
        conv1 = conv_layer(x, filter_size1, num_filters1, stride1, name='conv1')
        
        #pool1 = max_pool(conv1, ksize=2, stride=2, name='pool1')
        conv2 = conv_layer(conv1, filter_size2, num_filters2, stride2, name='conv2')
        #pool2 = max_pool(conv2, ksize=2, stride=2, name='pool2')
        
        layer_flat = flatten_layer(conv1)
        fc1 = fc_layer(layer_flat, h1, 'FC1', use_relu=True)
        output = fc_layer(fc1, img_size_flat, 'OUT', use_relu=False)
        z=tf.shape(y)
        print(x.get_shape(), conv1.get_shape(), conv2.get_shape(), layer_flat.get_shape(), fc1.get_shape(), output.get_shape())
        output_logits = tf.reshape(output, z)
        '''

        # Define the loss function, optimizer, and accuracy
        with tf.variable_scope('Train'):
            with tf.variable_scope('Loss'):
                self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=self.y, logits=output_logits), name='loss')
            tf.summary.scalar('loss', self.loss)
            with tf.variable_scope('Optimizer'):
                self.optimizer = tf.train.AdamOptimizer(learning_rate=lr, name='Adam-op').minimize(self.loss)
            with tf.variable_scope('Accuracy'):

                self.correct_prediction = tf.equal(tf.round(tf.nn.sigmoid(output_logits)), tf.round(self.y), name='correct_pred')
                self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32), name='accuracy')
            tf.summary.scalar('accuracy', self.accuracy)
            with tf.variable_scope('Prediction'):
                # Network predictions
                self.cls_prediction = output_logits

        # Creating the op for initializing all variables
        init = tf.global_variables_initializer()
        # Merge all summaries
        merged = tf.summary.merge_all()

        if not self.restore:
            # Launch the graph (session)
            with tf.Session() as sess:
                sess.run(init)
                global_step = 0
                summary_writer = tf.summary.FileWriter(logs_path, sess.graph)
                # Number of training iterations in each epoch
                num_tr_iter = int(len(y_train) / batch_size)
                for epoch in range(epochs):
                    print('Training epoch: {}'.format(epoch + 1))
                    x_train, y_train = randomize(x_train, y_train)
                    for iteration in range(num_tr_iter):
                        global_step += 1
                        start = iteration * batch_size
                        end = (iteration + 1) * batch_size
                        x_batch, y_batch = get_next_batch(x_train, y_train, start, end)

                        # Run optimization op (backprop)
                        feed_dict_batch = {self.x: x_batch, self.y: y_batch}
                        sess.run(self.optimizer, feed_dict=feed_dict_batch)

                        if iteration % display_freq == 0:
                            # Calculate and display the batch loss and accuracy
                            loss_batch, acc_batch, summary_tr = sess.run([self.loss, self.accuracy, merged],
                                                                         feed_dict=feed_dict_batch)
                            summary_writer.add_summary(summary_tr, global_step)

                            print("iter {0:3d}:\t Loss={1:.2f},\tTraining Accuracy={2:.01%}".
                                  format(iteration, loss_batch, acc_batch))

                    # Run validation after every epoch
                    feed_dict_valid = {self.x: x_valid, self.y: y_valid}
                    loss_valid, acc_valid, summary_val = sess.run([self.loss, self.accuracy, merged], feed_dict=feed_dict_valid)
                    summary_writer.add_summary(summary_val, global_step)
                    print('---------------------------------------------------------')
                    print("Epoch: {0}, validation loss: {1:.2f}, validation accuracy: {2:.01%}".
                          format(epoch + 1, loss_valid, acc_valid))
                    print('---------------------------------------------------------')

                # Test the network when training is done

                feed_dict_test = {self.x: x_valid, self.y: y_valid}
                ls_pred = sess.run(self.cls_prediction, feed_dict=feed_dict_test)

                loss_test, acc_test = sess.run([self.loss, self.accuracy], feed_dict=feed_dict_test)
                print('---------------------------------------------------------')
                print("Test loss: {0:.2f}, test accuracy: {1:.01%}".format(loss_test, acc_test))
                print('---------------------------------------------------------')

                # Plot some of the correct and misclassified examples
                cls_pred = sess.run(self.cls_prediction, feed_dict=feed_dict_test)
                cls_true = np.argmax(y_valid, axis=1)

                saver = tf.train.Saver()
                saver.save(sess, "saved_model")

    def predict(self, test_data):
        with tf.Session() as sess:
            saver = tf.train.Saver()
            saver.restore(sess, "saved_model")
            feed_dict_test = {self.x: test_data, self.y: test_data}
            prediction = sess.run(self.cls_prediction, feed_dict=feed_dict_test)
        return prediction