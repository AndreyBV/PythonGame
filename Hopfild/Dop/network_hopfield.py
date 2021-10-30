
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from tqdm import tqdm
import os

rootDir = os.path.dirname(os.path.abspath(__file__))

class HopfieldNetwork(object):      
    # Распределение весов модели
    def train_weights(self, train_data):
        print("Start to train weights...")
        num_data =  len(train_data)
        self.num_neuron = train_data[0].shape[0]
        
        # Инициализация весов (формирование матрицы из нулей с указанным количество нейронов) 
        W = np.zeros((self.num_neuron, self.num_neuron))
        # Вычисление расстояний
        rho = np.sum([np.sum(t) for t in train_data]) / (num_data*self.num_neuron)
        
        # Использование правила Хебба
        for i in tqdm(range(num_data)):
            t = train_data[i] - rho
            W += np.outer(t, t)
        
        # Установка диагональных элементов в 0 в матрице весов
        diagW = np.diag(np.diag(W))
        W = W - diagW
        W /= num_data
        
        self.W = W 
    
    # Предсказание с помощью модели
    def predict(self, data, num_iter=20, threshold=0, asyn=False):
        print("Start to predict...")
        self.num_iter = num_iter
        self.threshold = threshold
        self.asyn = asyn
        
        # Копирование исходного набора данных
        copied_data = np.copy(data)
        
        # Формирование прогнозного списка с использованием индикации (прогресс-бара)
        predicted = []
        for i in tqdm(range(len(data))):
            predicted.append(self._run(copied_data[i]))
        return predicted
    
    def _run(self, init_s):
        if self.asyn==False:
            """
            Synchronous update
            """
            # Инициализация фнукции энергии
            s = init_s # Результат предсказацния
            e = self.energy(s)
            
            for i in range(self.num_iter):
                # Обновление s
                s = np.sign(self.W @ s - self.threshold)
                # Перерасчет функции энергии
                e_new = self.energy(s)
                
                # Если s сошлось
                if e == e_new:
                    return s
                # Обновление результата функции энергии
                e = e_new
            return s
        else:
            """
            Asynchronous update
            """
            # Инициализация функции энергии
            s = init_s
            e = self.energy(s)
            
            for i in range(self.num_iter):
                for j in range(100):
                    # Выбор произовльного нейроно
                    idx = np.random.randint(0, self.num_neuron) 
                    # Обновление s
                    s[idx] = np.sign(self.W[idx].T @ s - self.threshold)
                
                # Перерасчет функции энергии
                e_new = self.energy(s)
                
                # s is converged
                if e == e_new:
                    return s
                # Update energy
                e = e_new
            return s
    
    # Функция энергии
    def energy(self, s):
        return -0.5 * s @ self.W @ s + np.sum(s * self.threshold)

    # Функция отображения весов
    def plot_weights(self):
        plt.figure(figsize=(6, 5))
        w_mat = plt.imshow(self.W, cmap=cm.coolwarm)
        plt.colorbar(w_mat)
        plt.title("Network Weights")
        plt.tight_layout()
        plt.savefig(rootDir + "\weights.png")
        plt.show()