

import numpy as np
np.random.seed(1)
from matplotlib import pyplot as plt
import skimage.data
from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage.transform import resize
import network_hopfield as network
import os

rootDir = os.path.dirname(os.path.abspath(__file__))

# Формирование тестового набора данных (добавление шумов в изображения)
def noise_img(input, corruption_level):
    corrupted = np.copy(input)
    # Использование биноминального распределения для создания шумов
    inv = np.random.binomial(n=1, p=corruption_level, size=len(input))
    for i, v in enumerate(input):
        if inv[i]:
            corrupted[i] = -1 * v
    return corrupted


# Подготовка изображения для исопльзования в сети
def preprocessing(img, w=128, h=128):
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

def main():
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

    # Создание нейронной сети Хопфилда, запуск распределения весов
    model = network.HopfieldNetwork()
    model.train_weights(data)

    # Формирование тестовго набора
    test = [noise_img(img, 0.3) for img in data]
    # Предсказание изображения на основе зашумленных данных
    predicted = model.predict(test, num_iter=20, threshold=0, asyn=False)
    # print(predicted)
    # Отображене результатов
    print("Show prediction results...")
    print(predicted[0])
    plot(data, test, predicted)
    # print("Show network weights matrix...")
    # model.plot_weights()

if __name__ == '__main__':
    main()
