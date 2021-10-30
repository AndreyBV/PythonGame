import numpy as np
import matplotlib.pyplot as plt
import neurolab as nl
import sys
import os
import pandas as pd
import math
import random as rnd
import time
from threading import Thread
from pprint import pprint
from pandas import ExcelWriter
from pandas import ExcelFile
import queue as queue
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
import matplotlib #подключаем библиотеку matplotlib целиком
import matplotlib.pyplot as plt #подключаем из большой библиотеки модуль pyplot, который является аналогом МАТЛАБА. МАТЛАБ - это язык программирования и набор программ для математиков. Этот модуль питона пытается её заменить. Присваиваем ему короткое имя plt.
# from datetime import datetime #подключаем функцию для преобразования дат в нужный формат.
from datetime import datetime, timedelta
from urllib.parse import urlencode #urlencode требуется для формирования строки, которая улетит на Финам в качестве запроса.
from urllib.request import urlopen #с помощью urlopen будем отсылать запрос на Финам и получать текстовый ответ.

import skimage.data
from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage.transform import resize
from sklearn.metrics import mean_squared_error as sk_MSE


rootDir = os.path.dirname(os.path.abspath(__file__))
img_resize = 50
power_noise = 1
type_net = "ham"

def DataSet():
    df = pd.read_excel(rootDir + '\DataSet.xlsx', sheet_name='Лист1', dtype=str)
    # df["Объект"] = df["Объект"].astype(str)
    # df["Результат"] = df["Результат"].astype(str)
    listObject = df["Объект"].tolist()
    listResult = df["Результат"].tolist()
    # print(df)
    # print(df.dtypes)
    inputList = []
    for x in [list(x) for x in listObject if type(x) == str]:
        inputList.append([-1 if int(y) == 0 else int(y) for y in x])
    return (inputList, [x for x in listResult if type(x) == str])

def GetDataImg():
    # Получеаем изображения из библиотеки skimage
    camera = skimage.data.camera()
    astronaut = rgb2gray(skimage.data.astronaut())
    horse = skimage.data.horse()
    coffee = rgb2gray(skimage.data.coffee())

    # Объединяем данные в общий массив
    data = [camera, astronaut, horse, coffee]

    # Преобразование изображений для использования в нейронной сети
    print("Start to data preprocessing...")
    data = [preprocessing(img) for img in data]
    return data

# Формирование тестового набора данных (добавление шумов в изображения)
def noise_img(input, corruption_level):
    corrupted = np.copy(input)
    # Использование биноминального распределения для создания шумов
    inv = np.random.binomial(n=power_noise, p=corruption_level, size=len(input))
    for i, v in enumerate(input):
        if inv[i]:
            corrupted[i] = -1 * v 
    return corrupted


# Подготовка изображения для исопльзования в сети
def preprocessing(img, w=img_resize, h=img_resize):
    # Изменение размеров изображения
    img = resize(img, (w,h), mode='reflect')

    # Применение к изображению пороговой обработки
    thresh = threshold_mean(img)
    binary = img > thresh
    shift = 2*(binary*1)-1 # Boolian to int

    # Применение изменений к изображению
    flatten = np.reshape(shift, (w*h))
    return flatten

# Перобразование формы массива
def reshape(data):
    dim = int(np.sqrt(len(data)))
    data = np.reshape(data, (dim, dim))
    return data

# Отображение результата тестирования 
def plot(data, test, predicted, figsize=(5, 6)):
    # Формирование массивов исходных изображений, тестовых и предсказанных
    data = [reshape(d) for d in data]
    test = [reshape(d) for d in test]
    predicted = [reshape(d) for d in predicted]

    fig, axarr = plt.subplots(len(data), 3, figsize=figsize)
    for i in range(len(data)):
        if i==0:
            axarr[i, 0].set_title('Train data')
            axarr[i, 1].set_title("Input data")
            axarr[i, 2].set_title('Output data')

        axarr[i, 0].imshow(data[i])
        axarr[i, 0].axis('off')
        axarr[i, 1].imshow(test[i])
        axarr[i, 1].axis('off')
        axarr[i, 2].imshow(predicted[i])
        axarr[i, 2].axis('off')

    plt.tight_layout()
    plt.savefig(rootDir + "\hopfield_test.png")
    plt.show()

def MSE_Error(listData, listPredict):
    # listData = [x for l in listData for x in l]
    # listData = [x for l in listPredict for x in l]
    # msef = nl.error.MSE()
    # mse_res = msef(np.array(listData), np.array(listPredict))

    mse_err = sk_MSE(listData, listPredict)
    print("\nError MSE: " + str(mse_err))
    # print(listData)
    # for i in range(len(listData)):
    #     msef = nl.error.MSE()
    #     # print(listData)
    #     # print()
    #     data_test_err = ([listData[i], ])
    #     # print(data_test_err)
    #     mse_res = msef(np.array(listData[i]), np.array(listPredict[i]))
    #     print(mse_res)


def NNHamming(ds, ts):
    # Список для результатов предсказания
    listPredict = []
    # Формирование тренировочного набора
    listData = [row.tolist() for row in ds]
    # print(len(listData))
    # Формирование тестовго набора
    listDataTest = [row.tolist() for row in ts]
    # print(listData)

    # Competitive - соревнование 
    # PureLin - линейный сигмоид
    # max_init / max_iter
    net = nl.net.newhem(listData, transf=nl.trans.PureLin(),  max_iter=50, delta=0,)



    # testList = listData
    # out = net.sim(testList)
    # print("\n\t\tРезультат прогнозирования на обучающей выборке: ")
    # print(out)
    # i = 0
    # for x in out:
    #     # print(str(i +1) + ")    Вектор-объект: \n  " + str(listData[i]))
        
    #     # print("Вектор-результат: \n  " + str(x))
    #     maxEl = max(x)
    #     if list(x).count(maxEl) > 1:
    #         print("\tРЕУЗЛЬТАТ: не удалось распознать объект!")
    #     else:
    #         maxIndex = list(x).index(maxEl)
    #         listPredict.append(listData[maxIndex])
    #         # print("\tРЕУЗЛЬТАТ: " + str(listResult[maxIndex]))
    #     # print("\tОЖИДАЛОСЬ: " + str(listResult[i]))
    #     i += 1

   
    
    listPredict = []
    testList = listDataTest
    out = net.sim(testList)
    # print("\n\n\t\tРезультат прогнозирования на тестовой выборке: ")
    i = 0
    for x in out:
        # print(str(i + 1) + ")    Вектор-объект: \n  " + str(listDataTest[i]))
        
        print(str(x))
        maxEl = max(x)
        if list(x).count(maxEl) > 1:
            print("\tРЕУЗЛЬТАТ: не удалось распознать объект!")
        else:
            maxIndex = list(x).index(maxEl)
            listPredict.append(listData[maxIndex])
            # print("\tРЕУЗЛЬТАТ: " + str(listResultTest[maxIndex]))
        # print("\tОЖИДАЛОСЬ: " + str(listResultTest[i]))
        i += 1

    MSE_Error(listData, listPredict)



    return listPredict


def NNHopfield(ds, ts):
    # Список для результатов предсказания
    listPredict = []
    # Формирование тренировочного набора
    listData = [row.tolist() for row in ds]
    # print(len(listData))
    # Формирование тестовго набора
    listDataTest = [row.tolist() for row in ts]
    # print(listData)

    # Competitive - соревнование 
    # PureLin - линейный сигмоид
    # max_init / max_iter
    print("ssssssssssssssss")
    print(listData)
    net = nl.net.newhop(listData, max_init=20)


    # testList = listData
    # out = net.sim(testList)
    # print("\n\t\tРезультат теста из обучающей выборки: ")
    # print(out)
    # i = 0
    # for x in out:
    #     # print(str(i +1) + ")    Вектор-объект: \n  " + str(listData[i]))
        
    #     print("Вектор-результат: \n  " + str(x))
    #     maxEl = max(x)
    #     if list(x).count(maxEl) > 1:
    #         print("\tРЕУЗЛЬТАТ: не удалось распознать объект!")
    #     else:
    #         maxIndex = list(x).index(maxEl)
    #         # print("\tРЕУЗЛЬТАТ: " + str(listResult[maxIndex]))
    #     # print("\tОЖИДАЛОСЬ: " + str(listResult[i]))
    #     i += 1
    
    # MSE_Error(listData, listPredict)
    # listPredict = []

    testList = listDataTest
    out = net.sim(testList)
    # print("\n\n\t\tРезультат прогнозирования на тестовой выборке: ")
    i = 0
    for x in out:
        # print(str(i + 1) + ")    Вектор-объект: \n  " + str(listDataTest[i]))
        x = np.array(x)
        # x = list(x.reshape(img_resize, img_resize))
        # print(x)

        print(str(x))
        # maxEl = max(x)
        # if list(x).count(maxEl) > 1:
        #     print("\tРЕУЗЛЬТАТ: не удалось распознать объект!")
        # else:
        #     # maxIndex = list(x).index(maxEl)
        listPredict.append(x)
            # print("\tРЕУЗЛЬТАТ: " + str(listResultTest[maxIndex]))
        # print("\tОЖИДАЛОСЬ: " + str(listResultTest[i]))
        i += 1
    
    MSE_Error(listData, listPredict)

    return listPredict    



def main():


    ds = DataSet()
    ds = GetDataImg()
    ts = [noise_img(img, 0.3) for img in ds]
  
    # # if type_net == "ham":
    # print("\t\t\n--------- Hamming ---------")
    # pd = NNHamming(ds, ts)
    # plot(ds, ts, pd)
    # # if type_net == "hop":
    print("\t\t\n--------- Hopfield ---------")
    pd = NNHopfield(ds, ts)
    print(pd)
    plot(ds, ts, pd)

if __name__ == '__main__': 
    main()

