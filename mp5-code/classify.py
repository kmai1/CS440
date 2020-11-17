# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set

return - a list containing predicted labels for dev_set
"""

import numpy as np

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters
    # w_i=w_i+α⋅(y−y_hat)⋅x_i

    alpha = learning_rate
    #piazza 1035
    W = np.zeros(len(train_set[0]))
    b = 0
    counter = 0
    for iteration in range(max_iter):
        for i in range(len(train_set)):
            x_i =  train_set[i]
            # corresponding label
            y = 1 if(train_labels[i]) else -1  # true/false value 1 or 0
            # same dim doesnt matter order
            weight = np.dot(x_i, W) + b
            activation_value = np.sign(weight)
            # if equal dont update weights, do nothing
            if activation_value == y:
                continue
            weight_vector = alpha * y * x_i
            b += alpha * y
            W += weight_vector
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    W, b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    temp_weight = np.dot(dev_set, W) + b
    labels = []
    for weight in temp_weight:
        if (weight >= 0):
            labels.append(1)
        else:
            labels.append(0)
    return labels


def classifyKNN(train_set, train_labels, dev_set, k):
    # TODO: Write your code here
    #use np.linalg.norm for euclidean distance
    labels = []

    for i in range(len(dev_set)):
        #dist between curr and training_set
        distance = []
        for j in range(len(train_set)):
            distance.append(np.linalg.norm(dev_set[i] - train_set[j]))
        sortedDist = list(distance)
        sortedDist.sort()
        # finds if more labels are 1 or 0, more 1 avg > 0.5, more 0 < 0.5, if = then make it 0
        avgOfDist = 0
        for x in range(0, k):
            idx = distance.index(sortedDist[x])
            avgOfDist += train_labels[idx]
        avgOfDist /= k
        # > bc = 0 is 0
        if avgOfDist > 0.5:
            labels.append(1)
        else:
            labels.append(0)
    return labels
