from skimage.util.shape import view_as_blocks
import cv2
from sklearn.datasets import load_digits
from sklearn.linear_model import Perceptron
import sys
import os
import random
import gc   #Gabage collector for cleaning deleted data from memory
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score
from colorama import Fore, Back, Style
import colorama 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.neural_network import MLPClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import layers
from keras import models
from keras.applications import InceptionResNetV2
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array, load_img

# Основные параметры 
# размеры сжатия изображений
nrows = 150 
ncolumns = 150
channels = 3  
# Колиество изображений для обучения
nImgTrain = 80
nCat = int(nImgTrain / 2)
nDog= int(nImgTrain - nCat)
nImgTest = 10

# Пути к обучающим и тестовым файлам
rootDir = os.path.dirname(os.path.abspath(__file__))
train_dir = rootDir + '\input\\train'
test_dir = rootDir + '\input\\test'

# Формирование обучающей и тестовой выборки
def LoadData():
    train_asfs = [rootDir + '\input\\train\{}'.format(i) for i in os.listdir(train_dir) if 'asf' in i]  #get asf images
    train_sngs = [rootDir + '\input\\train\{}'.format(i) for i in os.listdir(train_dir) if 'sng' in i]  #get sng images
    test_imgs = [rootDir + '\input\\test\{}'.format(i) for i in os.listdir(test_dir)] #get test images
    train_imgs = train_asfs[: nDog] + train_sngs[: nCat]  # slice the dataset and use 2000 in each class
    random.shuffle(train_imgs)  # shuffle it randomly
    return test_imgs, train_imgs

# Подготовка изображений
def ProcessingImg(list_of_images, nImg):
    X = [] # Изображения
    y = [] # Метки изображений
    
    for image in list_of_images:
        image = r'{0}'.format(image) 
        img = cv2.imread(image, channels)
        # Преобразование изображений в единый формат
        resizeImg = cv2.resize(img, (nrows,ncolumns), interpolation=cv2.INTER_CUBIC)
        X.append(resizeImg) 
        # Формирование меток изображений
        if 'asf' in image:
            y.append(1)
        elif 'sng' in image:
            y.append(0)
 
    # Конвертация списка в массив нампи
    X = np.array(X)
    y = np.array(y)

    return X, y

#  Формирование тренировочной и валидационной выборки
def FormationTrainTestDataSet(X, y): 
    xTrain, xValid, yTrain, yValid = train_test_split(X, y, test_size=0.25, random_state=42) 
    return xTrain, xValid, yTrain, yValid

# Обучение модели 
def TrainModel(xTrain, yTrain, xValid, yValid):
    # Получение размера массива обучающей и валидационной выборки
    ntrain = len(xTrain)
    nval = len(xValid)
    # Размер пакетов загоняемых в нейронную сеть
    batch_size = 32  

    # Использование светрочной нейронной сети, обученная на огромной базе изображений
    conv_base = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=(150,150,3))
    # Получение сводки
    # conv_base.summary()
    # Формирование перцептрона
    model = models.Sequential()
    model.add(conv_base)
    # Преоброзование матрицы изображения в одномерный массив
    model.add(layers.Flatten())
    # Подключение полностью связанных нейронных слоев (т.е. средний слой содержит 256 узлов и фун. активации RELU, н выходе получаем 1 сигмоидный узел)
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))  #Sigmoid function at the end because we have just two classes
    conv_base.trainable = False
    # Компиляция модели (функция потери - измеряет насколько точная модель во время обучения, 
    # Оптимайзер - то как модель обновляется на основе данных, которые она видит
    # Метрики - используются для контроля качества обучения и тестироваия)
    model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])
    # Препроцессинг (предварительная обработка изображений)
    train_datagen = ImageDataGenerator(rescale=1./255,  
                                    rotation_range=40,
                                    width_shift_range=0.2,
                                    height_shift_range=0.2,
                                    shear_range=0.2,
                                    zoom_range=0.2,
                                    horizontal_flip=True,
                                    fill_mode='nearest')
    val_datagen = ImageDataGenerator(rescale=1./255) 

    # На баез массива изображений и их меток, генерируются пакеты дополнительных данных
    train_generator = train_datagen.flow(xTrain, yTrain,batch_size=batch_size)
    val_generator = val_datagen.flow(xValid, yValid, batch_size=batch_size)

    # Обучение модели
    history = model.fit_generator(train_generator,
                                steps_per_epoch=ntrain // batch_size,
                                epochs=20,
                                validation_data=val_generator,
                                validation_steps=nval // batch_size)
                                
    # Сохранение обученной модели в файл для дальнейшего повторного использования
    # model.save_weights(rootDir + '\model_wieghts.h5')
    model.save(rootDir + 'model_keras.h5')
    return model

# Испытание обученной модели
def Predictions(model, test_imgs):
    pass
    # Подготовка изображений
    nTestImg = 20
    indexStartImg = random.randrange(1, 10)
    listImg = test_imgs[0:nTestImg]
    xTest, yTest = ProcessingImg(listImg, nImgTest) 
    print(xTest.shape)
    test_datagen = ImageDataGenerator(rescale=1./255)

    # Вывод тестируемых изображений, а также результата их предсказания
    i = 0
    nColImg = 5
    text_labels = []
    form = plt.figure()
    form.canvas.set_window_title('Лабораторная работа №3 - Распознование объектов по изображениям')
    for batch in test_datagen.flow(xTest, batch_size=1):
        pred = model.predict(batch)
        schedule = form.add_subplot(int(nTestImg/nColImg), nColImg, i+1)
        if pred > 0.5:
            schedule.set_title("Асфальт")
        else:
            schedule.set_title("Снег")
        schedule.get_xaxis().set_visible(False)
        schedule.get_yaxis().set_visible(False)
        imgplot = schedule.imshow(batch[0])
        i += 1
        if i % nTestImg == 0:
            break
    plt.show()

def main():
    colorama.init()
    test_imgs, train_imgs = LoadData()
    X, y = ProcessingImg(train_imgs, nImgTrain)
    print(f"X-Shape: {X.shape}")
    print(f"y-Shape: {y.shape}")
    xTrain, xValid, yTrain, yValid = FormationTrainTestDataSet(X, y)
    model = TrainModel(xTrain, yTrain, xValid, yValid)
    # model = keras.models.load_model(rootDir + 'model_keras.h5')
    Predictions(model, test_imgs)

  
def print_mark(style, text):
    print(style + text)
    print(Style.RESET_ALL)

if __name__ == '__main__': 
    main()