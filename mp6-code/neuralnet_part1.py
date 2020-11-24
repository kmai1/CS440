# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
"""
This is the main entry point for MP6. You should only modify code
within this file and neuralnet_part2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch


class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network

        @param lrate: The learning rate for the model.
        @param loss_fn: A loss function defined in the following way:
            @param yhat - an (N,out_size) tensor
            @param y - an (N,) tensor
            @return l(x,y) an () tensor that is the mean loss
        @param in_size: Dimension of input
        @param out_size: Dimension of output

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size
        We recommend setting the lrate to 0.01 for part 1

        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        # CAN CHANGE 32 to 64 128 etc if need higher acc
        self.model = torch.nn.Sequential(
            torch.nn.Linear(in_size, 128), #input layer
            torch.nn.ReLU(), # activation fn
            torch.nn.Linear(128, out_size), #output later
        )
        # optimizer !?!?!
        #
        # torch.nn.Sequential(
        #
        # ) # SGD hasb etter results than adam?
        self.optimizer = torch.optim.SGD(self.parameters(), lr=lrate, momentum = 0.9)


    def forward(self, x):
        """ A forward pass of your neural net (evaluates f(x)).

        @param x: an (N, in_size) torch tensor

        @return y: an (N, out_size) torch tensor of output from the network
        """

        return self.model(x)
        # #what is this?
        # return torch.ones(x.shape[0], 1)

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        # clear grad
        self.optimizer.zero_grad()

        pred_y = self.forward(x)

        #loss of this
        loss = self.loss_fn(pred_y, y)
        loss.backward()
        # might need .backward
        self.optimizer.step()

        return loss


def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M,) torch tensor
    @param n_iter: int, the number of iterations of training
    @param batch_size: The size of each batch to train on. (default 100)

    # return all of these:

    @return losses: Array of total loss at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: A NeuralNet object

    # NOTE: This must work for arbitrary M and N
    """
    # standaridze data?? formuka = phi = (x - mu) / sigma
    train_set = (train_set - train_set.mean()) / train_set.std()
    dev_set = (dev_set - dev_set.mean())/ dev_set.std() #maybe its train_set.mean() and train_set.std()


    learning_rate = 0.01 # can try 0.0001 as well
    loss_fn = torch.nn.CrossEntropyLoss()
    in_size = len(train_set[0])
    out_size = 2 # 2 labels?
    net = NeuralNet(learning_rate, loss_fn, in_size, out_size)

    #return stuff
    losses = []

    for x in range(n_iter):
        #step train set
        loss_to_add = net.step(train_set, train_labels)
        losses.append(loss_to_add)
    out = net(dev_set)
    best_index = torch.argmax(out, 1)
    yhats = np.array(best_index)

    return losses, yhats, net
