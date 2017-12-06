import numpy as np
import tensorflow as tf
from keras.datasets import cifar10
from keras import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras import optimizers


def load_cifar10():
    train, test = cifar10.load_data()
    xtrain, ytrain = train
    xtest, ytest = test

    ytrain_1hot = np.zeros((ytrain.shape[0],10))

    for i in range(ytrain.shape[0]):
        ytrain_1hot[i][ytrain[i][0]] = 1;

    ytest_1hot = np.zeros((ytest.shape[0],10))

    for i in range(ytest.shape[0]):
        ytest_1hot[i][ytest[i][0]] = 1;


    xtrain_normalize = np.zeros((xtrain.shape[0],xtrain.shape[1],xtrain.shape[2],xtrain.shape[3]))
    for i in range(xtrain.shape[0]):
        xtrain_normalize[i] = xtrain[i] / 255.0

    xtest_normalize = np.zeros((xtest.shape[0],xtest.shape[1],xtest.shape[2],xtest.shape[3]))
    for i in range(xtest.shape[0]):
        xtest_normalize[i] = xtest[i] / 255.0




    return xtrain_normalize, ytrain_1hot, xtest_normalize, ytest_1hot


def build_multilayer_nn():
    pass


def train_multilayer_nn(model, xtrain, ytrain):
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    model.fit(xtrain, ytrain_1hot, epochs=30, batch_size=32)


def build_convolution_nn():
    pass


def train_convolution_nn():
    pass


def get_binary_cifar10():
    pass


def build_binary_classifier():
    pass


def train_binary_classifier():
    pass


if __name__ == "__main__":
    xtrain, ytrain_1hot, xtest, ytest_1hot = load_cifar10()

    print(ytrain_1hot[1:3])


    # Write any code for testing and evaluation in this main section.
