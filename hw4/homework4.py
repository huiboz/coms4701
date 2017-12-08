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


#10000/10000 [==============================] - 4s 393us/step
#[1.45028288230896, 0.4945]
def build_multilayer_nn():
    nn = Sequential()
    nn.add(Flatten(input_shape=(32,32,3)))
    hidden = Dense(units=100, activation="relu")
    nn.add(hidden)
    output = Dense(units=10, activation="softmax")
    nn.add(output)
    return nn



def train_multilayer_nn(model, xtrain, ytrain_1hot):
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    model.fit(xtrain, ytrain_1hot, epochs=20, batch_size=32)

#10000/10000 [==============================] - 27s 3ms/step
#[0.75384073019027709, 0.73880000000000001]
def build_convolution_nn():
    nn = Sequential()
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same",input_shape=(32,32,3)))
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    nn.add(MaxPooling2D(pool_size=(2, 2)))
    nn.add(Dropout(0.25))
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    nn.add(MaxPooling2D(pool_size=(2, 2)))
    nn.add(Dropout(0.5))
    nn.add(Flatten())
    nn.add(Dense(units=250, activation="relu"))
    nn.add(Dense(units=100, activation="relu"))
    nn.add(Dense(units=10, activation="softmax"))
    return nn


def train_convolution_nn(model, xtrain, ytrain_1hot):
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    model.fit(xtrain, ytrain_1hot, epochs=25, batch_size=32)


def get_binary_cifar10():
    pass


def build_binary_classifier():
    pass


def train_binary_classifier():
    pass


if __name__ == "__main__":
    xtrain, ytrain_1hot, xtest, ytest_1hot = load_cifar10()
    nn = build_convolution_nn()
    train_convolution_nn(nn, xtrain, ytrain_1hot)
    print(nn.evaluate(xtest, ytest_1hot))

    #print(ytrain_1hot[1:3])


    # Write any code for testing and evaluation in this main section.
