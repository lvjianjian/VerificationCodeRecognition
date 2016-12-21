#!/usr/bin
# -*- coding: utf-8 -*-
# Deep Convolutional Network using Keras

import pandas as pd
import numpy as np
import keras.layers.core as core
import keras.layers.convolutional as conv
import keras.models as models
import keras.utils.np_utils as kutils
import VerificationCodeGenerator as generator
import VerificationCodeSpliter2 as spilter
import os
import shutil
import Param as param
import string


#main

# if(os.path.isdir("image")):
#     shutil.rmtree("image")
# if(os.path.isdir("image2")):
#     shutil.rmtree("image2")
# if(os.path.isdir("matrix")):
#     shutil.rmtree("matrix")
# os.mkdir("image")
# os.mkdir("image2")
# os.mkdir("matrix")
#
# #使用的字体
# Fonts = ["/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-BI.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-C.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-L.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-M.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-LI.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-MI.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-R.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-RI.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-B.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-BI.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf"
#     ,"/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-RI.ttf"]
#
# basepath = param.PROJECTBASEPATH
#
# # 生成训练样例图片
# generator.gene_AllVerificationCodeWithNoise(1000, basepath + "image/",
#                                     Fonts)
#
# #生成测试样例图片
# generator.gene_AllVerificationCodeWithNoise(10, basepath + "image2/",
#                                     Fonts)
#
#
# #训练图片转csv
# spilter.split(basepath+"image/", basepath + "matrix/train.csv")
#
# #测试图片转csv
# spilter.split(basepath + "image2/", basepath + "matrix/test.csv")

# The competition datafiles are in the directory ../input
# Read competition data files:

dict1={}
dict={}
i = 0
for j in range(10):
    dict1[i] = i
    dict1[str(i)] = i
    dict[i] = str(i)
    i += 1
for v in string.lowercase:
    dict1[v] = i
    dict[i] = v
    i += 1
for v in string.uppercase:
    dict1[v] = i
    dict[i] = v
    i += 1


def toIndex(c):
    return dict1[c]


def num2Y(nums):
    """
    将数字还原成字母或数字
    :param nums:
    :return:
    """
    list = []
    for num in nums:
        list.append(dict[num])
    return list

def Y2matrix(y):
    """
    将含字符的输出集合转成矩阵
    :param y:
    :return:
    """
    matrix = np.zeros((y.shape[0], 62), dtype=bool)
    for i in range(len(y)):
        matrix[i][toIndex(y[i][0])] = 1
    return matrix

if __name__ == '__main__':

    train_df_self = pd.read_csv("matrix/train_all_noise_10000.csv").values
    test = pd.read_csv("matrix/train_all_noise_1000.csv").values

    train_df_kaggle = pd.read_csv('kaggle/train.csv').values

    # print train_df_kaggle.size
    # train = train_df_kaggle.append(train_df_self)
    # train = train_df_kaggle
    train = train_df_self
    nb_epoch = 3 # Change to 100

    batch_size = 128
    img_rows, img_cols = 28, 28

    nb_filters_1 = 32 # 64
    nb_filters_2 = 64 # 128
    nb_filters_3 = 128 # 256
    nb_conv = 3

    trainX = train[:, 1:].reshape(train.shape[0], img_rows, img_cols, 1)
    trainX = trainX.astype(float)
    trainX /= 255.0

    trainY = Y2matrix(train[:,:1])

    nb_classes = trainY.shape[1]

#=====================
    # cnn = models.Sequential()
    #
    # cnn.add(conv.Convolution2D(nb_filters_1, nb_conv, nb_conv,  activation="relu", input_shape=(28, 28, 1), border_mode='same'))
    # cnn.add(conv.Convolution2D(nb_filters_1, nb_conv, nb_conv, activation="relu", border_mode='same'))
    # cnn.add(conv.MaxPooling2D(pool_size=(2, 2)))
    #
    # cnn.add(conv.Convolution2D(nb_filters_2, nb_conv, nb_conv, activation="relu", border_mode='same'))
    # cnn.add(conv.Convolution2D(nb_filters_2, nb_conv, nb_conv, activation="relu", border_mode='same'))
    # cnn.add(conv.MaxPooling2D(pool_size=(2, 2)))
    #
    # #cnn.add(conv.Convolution2D(nb_filters_3, nb_conv, nb_conv, activation="relu", border_mode='same'))
    # #cnn.add(conv.Convolution2D(nb_filters_3, nb_conv, nb_conv, activation="relu", border_mode='same'))
    # #cnn.add(conv.Convolution2D(nb_filters_3, nb_conv, nb_conv, activation="relu", border_mode='same'))
    # #cnn.add(conv.Convolution2D(nb_filters_3, nb_conv, nb_conv, activation="relu", border_mode='same'))
    # #cnn.add(conv.MaxPooling2D(strides=(2,2)))
    #
    # cnn.add(core.Flatten())
    # cnn.add(core.Dropout(0.2))
    # cnn.add(core.Dense(128, activation="relu")) # 4096
    # cnn.add(core.Dense(nb_classes, activation="softmax"))
#==============
    cnn = models.Sequential()

    cnn.add(conv.Convolution2D(32, 5, 5, activation='relu', input_shape=(28, 28, 1)))
    cnn.add(conv.MaxPooling2D(pool_size=(2,2)))

    cnn.add(conv.Convolution2D(32, 3, 3, activation='relu'))
    cnn.add(conv.MaxPooling2D())

    cnn.add(core.Flatten())

    cnn.add(core.Dense(output_dim=128, activation='relu'))
    cnn.add(core.Dropout(0.5))

    cnn.add(core.Dense(output_dim=62, activation='softmax'))

    cnn.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    cnn.summary()
    #categorical_crossentropy
    cnn.fit(trainX, trainY, batch_size=batch_size, nb_epoch=nb_epoch, verbose=1)


    # testX = test.reshape(test.shape[0], 28, 28, 1)
    # testX = testX.astype(float)
    # testX /= 255.0
    #
    # yPred = cnn.predict_classes(testX)
    #
    # np.savetxt('mnist-vggnet.csv', np.c_[range(1,len(yPred)+1),yPred], delimiter=',', header = 'ImageId,Label', comments = '', fmt='%d')

    # print test
    # print test[:,0]
    # testY = kutils.to_categorical(test[:, 0])
    # print testY
    testY = Y2matrix(test[:,:1])
    testX = test[:, 1:].reshape(test.shape[0], 28, 28, 1)
    testX = testX.astype(float)
    testX /= 255.0

    # yPred = cnn.predict_classes(testX)
    # print textY
    #save model
    # json = cnn.to_json()

    # f = open("model/kaggle_model.json", mode="w")
    # f.write(json)
    # f.flush()
    # f.close()
    # cnn.save_weights("model/kaggle_model.weights")
    loss_and_metrics = cnn.evaluate(testX, testY, batch_size = batch_size)
    print loss_and_metrics
    # print yPred

    # np.savetxt('mnist-vggnet.csv', np.c_[range(1,len(yPred)+1),yPred], delimiter=',', header = 'ImageId,Label', comments = '', fmt='%d')

