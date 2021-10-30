#!/usr/bin/env python

import pandas as pd
import os
from train_art import data_train
from test_art import data_test
# from art import train
# import art
# from art import data_train, data_test
# import train as train_art
# import test as test_art
# from lapart import train,test
import skimage
from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt

img_resize = 50
power_noise = 1

# Корневой каталог
root_dir = os.path.dirname(os.path.abspath(__file__))

def DataSet():
    df = pd.read_excel(root_dir + '\DataSet.xlsx', sheet_name='Лист1', dtype=str)
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
def NoiseImg(input, corruption_level):
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
    pred = []
    for i in predicted:
        i = int(i)
        print(i)
        if i >= 0:
            pred.append(data[i])
        else:
            pred.append(np.zeros([img_resize, img_resize], dtype = int) )

    # predicted = [reshape(d) for d in predicted]
    # print(data[0].shape)
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
        axarr[i, 2].imshow(pred[i])
        axarr[i, 2].axis('off')

    plt.tight_layout()
    plt.savefig(root_dir + "\hopfield_test.png")
    plt.show()

def ART(ds, ts):

     # Список для результатов предсказания
    listPredict = []
    # Формирование тренировочного набора
    listData = np.asarray([row.tolist() for row in ds])
    # Формирование тестовго набора
    listDataTest = np.asarray([row.tolist() for row in ts])

    # train_data = pd.read_csv(root_dir + '/sample-data/train-example.csv').values
    # test_data = pd.read_csv(root_dir + '/sample-data/test-example.csv').values
    # # print(listData)
    # # print(listDataTest)
    # x = train_data[:,1:4]
    # y = test_data[:,1:4]
    # print(x)
    # print(y)



    r = 0.3
    Tmatrix = data_train(listData,rho=r) #,beta=0.000001,alpha=1.0,nep=1)
    print("Матрица весов:")
    print(Tmatrix)
    T = data_test(listDataTest,Tmatrix,rho=r) #,beta=0.000001,alpha=1.0,nep=1)
    print("Результат прогнозирования:")
    print(T["Template"])
    return T["Template"].tolist()




def main():
    # ds = DataSet()
    ds = GetDataImg()
    ts = [NoiseImg(img, 0.3) for img in ds]

    print("\t\t\n--------- ART ---------")
    x_train = []
    y_train = []
    x_test = []
    pd = ART(ds, ts)
    # pd = NNHopfield(ds, ts)
    plot(ds, ts, pd)

if __name__ == '__main__': 
    main()
