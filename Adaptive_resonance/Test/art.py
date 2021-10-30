#!/usr/bin/env python

import pandas as pd
import os
# from train_art import data_train
# from test_art import data_test
from art import train
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
    plt.savefig(root_dir + "\hopfield_test.png")
    plt.show()

def ART(x_train, y_train, x_test):
    # rA,rB = 0.8,0.8
    # TA,TB,L,t = train_art.lapArt_train(x_train,y_train,rhoA=rA,rhoB=rB,memory_folder='templates',update_templates=False)
    # C,T,Tn,df,t = test_art.lapArt_test(x_test,rhoA=rA,rhoB=rB,memory_folder='templates')
    
    train_data = pd.read_csv(root_dir + '/train-example.csv').values
    test_data = pd.read_csv(root_dir + '/test-example.csv').values
    x = train_data[:,1:3]
    y = test_data[:,1:3]
    print(x)
    print(y)



    r = 0.9
    Tmatrix = art.train_art(x,rho=r) #,beta=0.000001,alpha=1.0,nep=1)
    print(Tmatrix)
    T = art.test.art_test(y,Tmatrix,rho=r) #,beta=0.000001,alpha=1.0,nep=1)
    print(T)




def main():
    # ds = DataSet()
    ds = GetDataImg()
    ts = [NoiseImg(img, 0.3) for img in ds]
    print(ds)

    print("\t\t\n--------- ART ---------")
    x_train = []
    y_train = []
    x_test = []
    ART(x_train, y_train, x_test)
    # pd = NNHopfield(ds, ts)
    plot(ds, ts, pd)

if __name__ == '__main__': 
    main()
