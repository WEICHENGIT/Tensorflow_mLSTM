# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import random
import tensorflow as tf
import time
import os
import numpy as np
import io


class DataLoader():

    def __init__(self, data_dir, batch_size, seq_length):

        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length

        input_file = os.path.join(data_dir, "input.txt")

        self.read_data(input_file)
        self.create_batches()
        self.reset_batch_pointer()


    def read_data(self, input_file):

        # read the input file as bytes
        with io.open(input_file, 'rb') as f:
            data = np.array(bytearray(f.read()), dtype='int32')

        self.data = data

    def create_batches(self):

        # calculate no. of batches, same as above
        self.num_batches = int(self.data.size / (self.batch_size * self.seq_length))

        # give error message if tensor is too small
        if self.num_batches == 0:
            assert False, "Not enough data. Make seq_length and batch_size small."

        # make the data into an equal number of batches, a chunk of the data will probably be chopped off at the end
        self.data = self.data[:self.num_batches * self.batch_size * self.seq_length]

        # ydata is 1-d numpy array containing the targets. This is a shifted version of x where the ith element of ydata is the i+1th element of xdata and very last
        # element of ydata is the first element of xdata.
        xdata = self.data
        ydata = np.copy(self.data)
        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]

        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1), self.num_batches, 1)

    # load the next batch and increment the counter
    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0
