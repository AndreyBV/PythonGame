
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

rootDir = os.path.dirname(os.path.abspath(__file__))

# Суть оценки информативности признаков, сводиться к тому, чтобы понять 
# на сколько корректно работает распознование без какого-либо признака

def DataSet():
    df = pd.read_excel(rootDir + '\DataSet_LW_1.xlsx',
                       sheet_name='Лист2', dtype=str)
    listResult = df["Строковое представление"].tolist()
    listResult = [x for x in listResult if str(x) != 'nan']
    inputList = []

    for x in [list(x) for x in listResult if type(x) == str]:
        inputList.append([0 if int(y) == 0 else int(y) for y in x])
    A = inputList[:5]
    B = inputList[5:-6]
    At = inputList[-6:-3]
    Bt = inputList[-3:]

    list_A_mini = RemoveOneElem(A)
    list_B_mini = RemoveOneElem(B)
    list_At_mini = RemoveOneElem(At)
    list_Bt_mini = RemoveOneElem(Bt)

    # print(At)
    # print(list_At_mini)

    print("\nОбучающая выборка А:")
    for el in A:
        print(np.array(el).reshape(7, 5))
    print("\nОбучающая выборка Б:")
    for el in B:
        print(np.array(el).reshape(7, 5))
    print("\nТестовая выборка А:")
    for el in At:
        print(np.array(el).reshape(7, 5))
    print("\nТестовая выборка Б:")
    for el in Bt:
        print(np.array(el).reshape(7, 5))

    return (A, B, At, Bt, list_A_mini, list_B_mini, list_At_mini, list_Bt_mini)


def NeighbourNextDoor(data):
    A = np.array(data[0])
    B = np.array(data[1])
    At = np.array(data[2])
    Bt = np.array(data[3])

    # Получение 
    list_A_mini = np.array(data[4])
    list_B_mini = np.array(data[5])
    list_At_mini = np.array(data[6])
    list_Bt_mini = np.array(data[7])

    # n = 1
    # list_effective_count = []
    # list_tmp_A = []
    # list_tmp_B = []

    # Словарь информативности признаков
    dict_params = dict()
    for i in range(35):
        dict_params[i] = []

    for elem_boss in list_At_mini:
        print(elem_boss)
        # list_tmp_A = []
        # print("Обучающий массив - тест А ", elem_boss[0])
        count = 0
        for elem in elem_boss:
            count_A = 0
            # Список расстояний
            # 175 значений 35*5
            As = []
            Bs = []
            for el in list_A_mini:
                for e in el:
                    As.append(np.linalg.norm(e - elem))
            for el in list_B_mini:
                for e in el:
                    Bs.append(np.linalg.norm(e - elem))
            # print(len(As))
            if min(As) < min(Bs):
                pass
                # print("Похоже на А", n)
                count_A = count_A + 1
            elif min(As) == min(Bs):
                pass
                # print("Не ясно" , n)
            else:
                pass
                # print("Похоже на Б" , n)
            # print(count_A)
            dict_params[count].append(count_A)
            # n = n + 1
            count = count + 1
        # list_tmp_A.append(count_A)

    # print(dict_params)
    # list_effective_count.append(list_tmp_A)

    for elem_boss in list_Bt_mini:
        # list_tmp_B = []
        # print("Обучающий массив - тест Б ", elem_boss[0])
        count = 0
        for elem in elem_boss:
            count_B = 0
            As = []
            Bs = []
            for el in list_A_mini:
                for e in el:
                    As.append(np.linalg.norm(e - elem))
            for el in list_B_mini:
                for e in el:
                    Bs.append(np.linalg.norm(e - elem))
            if min(As) < min(Bs):
                pass
                # print("Похоже на А" , n)
            elif min(As) == min(Bs):
                pass
                # print("Не ясно", n)
            else:
                pass
                # print("Похоже на Б", n)
                count_B = count_B + 1
            # print(count_B)
            dict_params[count].append(count_B)
            # n = n + 1
            count = count + 1
        # list_tmp_B.append(count_B)

    # print(dict_params)
    # list_effective_count.append(list_tmp_B)

    # n = 1
    for el in dict_params.keys():
        dict_params[el] = sum(dict_params[el])/6
        # print(n, sum(el)/6)
        # n = n + 1
    print(
        np.reshape(list(dict_params.values()), (7, 5))
    )

# Отбрасываение признака 
# В каждом новом элементе списка удаляется последующий элемент (признак)
def RemoveOneElem(data):
    list_data_mini = []
    for el in data:
        list_now = []
        for i in range(len(el)):
            data_mini = [x for z, x in enumerate(el) if z != i]
            # print(data_mini)
            # print(len(data_mini))
            list_now.append(data_mini)
        list_data_mini.append(list_now)
    return list_data_mini


def main():
    data = DataSet()
    print("\nЭффективность признаков:")
    NeighbourNextDoor(data)


if __name__ == '__main__':
    main()
