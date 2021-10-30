from minisom import MiniSom
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.preprocessing import scale

root_dir = os.path.dirname(os.path.abspath(__file__))


# Загрузка датасета с цифрами
digits = datasets.load_digits(n_class=10)
# получение матрицы, где каждая строка идентифицирует цифру
data = digits.data  
# print(digits)
# Стандартизация набора данных
data = scale(data)
# Формирование целевого списка цифр, где num[i] - цифра, представленная data[i]
num = digits.target  


# Инициализация и обучение SOM
    # Указываем размеры карты, количество элементов входных векторов
    # 8x8 - размеры изображений
size_map = 30
som = MiniSom(size_map, size_map, 64, 
                sigma=4, # Распрострнанение функции 
                learning_rate=0.5, # Начальная скорость обучения
                neighborhood_function='triangle', # Функция взвешивания окрестностей карты ('gaussian', 'mexican_hat', 'bubble', 'triangle')
                topology='rectangular', # Топология карты ('rectangular', 'hexagonal')
                activation_distance='euclidean' # Способ измерения расстояния для активации карты ('euclidean', 'cosine', 'manhattan', 'chebyshev')
                )
# Инициализация весов
som.pca_weights_init(data)
# Обучение SOM на базе подаваемых данных с заданным количеством итераций. Также можно указать случайный порядок выбора образцов и возможность вывода этапов обучения.
som.train(data, 5000, random_order=True, verbose=True)  


# Отображение цифр в нормальном виде
plt.figure(figsize=(8, 8))
wmap = {}
im = 0
for x, t in zip(data, num):  
    # Получения коортежа координат нейрона победителя
    win = som.winner(x)
    # Формирование карты
    wmap[win] = im
    # отображение цифры из тренировочной выборки на плоте
    plt.text(win[0]+.5,  win[1]+.5,  str(t),
              color=plt.cm.rainbow(t / 10.), 
              fontdict={'weight': 'bold',  'size': 8})
    im = im + 1
plt.axis([0, som.get_weights().shape[0], 0,  som.get_weights().shape[1]])
plt.savefig(root_dir + '\som_digts.png')
plt.show()


# Отображение цифр в рукописном виде
plt.figure(figsize=(8, 8), facecolor='white')
cnt = 0
for j in range(size_map): 
    for i in range(size_map):
        # Формирование карты для рукописных цифр, при этому убираем рамку и деления
        plt.subplot(size_map, size_map, cnt+1, frameon=False,  xticks=[],  yticks=[])
        if (i, j) in wmap:
            plt.imshow(digits.images[wmap[(i, j)]],
                       cmap='Greys', interpolation='nearest')
        else:
            plt.imshow(np.zeros((8, 8)),  cmap='Greys')
        cnt = cnt + 1
# plt.tight_layout() # Изменение рзарера фигуры (убирает отступы по краям)
plt.savefig(root_dir + '\som_digts_imgs.png')
plt.show()