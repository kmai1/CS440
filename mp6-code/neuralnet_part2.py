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
within this file and neuralnet_part1 -- the unrevised staff files will be used for all other
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
        """

        # REFERENCE : https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        # CAN CHANGE 32 to 64 128 etc if need higher acc
        # self.model = torch.nn.Sequential(
        #     torch.nn.Conv2d(3, 6, 5),
        #     torch.nn.ReLU(),
        #     torch.nn.Conv2d(6, 16, 5)
        # )
        self.conv1 = torch.nn.Conv2d(3, 6, 5)
        self.pool = torch.nn.MaxPool2d(2, 2)
        self.conv2 = torch.nn.Conv2d(6, 16, 5)
        self.fc1 = torch.nn.Linear(16 * 5 * 5, 120)
        self.fc2 = torch.nn.Linear(120, 84)
        self.fc3 = torch.nn.Linear(84, 2)
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
        # print(self.model)
        x = x.view(-1,3,32,32)
        # print(x.size())
        # x = self.conv1(x)
        # print(x.size())
        # x = torch.nn.functional.relu(x)
        # print(x.size())
        # x = self.pool(x)
        x = self.pool(torch.nn.functional.relu(self.conv1(x)))
        # print(x.size())
        x = self.pool(torch.nn.functional.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = torch.nn.functional.relu(self.fc1(x))
        # print("error")
        x = torch.nn.functional.relu(self.fc2(x))
        # print("here")
        x = self.fc3(x)
        # print("here")
        return x


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

    model's performance could be sensitive to the choice of learning_rate. We recommend trying different values in case
    your first choice does not seem to work well.
    """
    # standaridze data?? formuka = phi = (x - mu) / sigma
    train_set = (train_set - train_set.mean()) / train_set.std()
    dev_set = (dev_set - dev_set.mean())/ dev_set.std() #maybe its train_set.mean() and train_set.std()


    learning_rate = 0.04 # can try 0.0001 as well
    loss_fn = torch.nn.CrossEntropyLoss()
    in_size = len(train_set[0])
    out_size = 2 # 2 labels?

    # train_set = train_set.view(100, 3, 32, 32)
    # dev_set = train_set.view(100, 3, 32, 32)

    net = NeuralNet(learning_rate, loss_fn, in_size, out_size)

    #return stuff
    losses = []
    for x in range(80): # try hard coding n_iter teo 40 50 60 ... maybe increate acc
        #step train set
        print(x)
        loss_to_add = net.step(train_set, train_labels)
        losses.append(loss_to_add)

    out = net(dev_set)
    best_index = torch.argmax(out, 1)
    yhats = np.array(best_index)

    return losses, yhats, net
