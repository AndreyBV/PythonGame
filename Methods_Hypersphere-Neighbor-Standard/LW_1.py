 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

rootDir = os.path.dirname(os.path.abspath(__file__))
 

# Загрузка и преобразование ихсодных данных
def DataSet():
    df = pd.read_excel(rootDir + '\DataSet_LW_1.xlsx', sheet_name='Лист2', dtype=str)
    listResult = df["Строковое представление"].tolist()
    listResult = [x for x in listResult if str(x) != 'nan']
    inputList = []

    for x in [list(x) for x in listResult if type(x) == str]:
        inputList.append([0 if int(y) == 0 else int(y) for y in x])
    A = inputList[:5]
    B = inputList[5:-6]    
    At = inputList[-6:-3]
    Bt = inputList[-3:]

    print("\nОбучающая выборка А:")
    for el in A: 
        print(np.array(el).reshape(7,5)) 
    print("\nОбучающая выборка Б:")
    for el in B: 
        print(np.array(el).reshape(7,5))
    print("\nТестовая выборка А:")
    for el in At: 
        print(np.array(el).reshape(7,5)) 
    print("\nТестовая выборка Б:")
    for el in Bt: 
        print(np.array(el).reshape(7,5))

    # Возвращает список образцовых букв, их тестовых значений
    return (A,B,At,Bt)
 
# Метод ближайшего соседа
def NeighbourNextDoor(data):
    A = np.array(data[0])
    B = np.array(data[1])
    At = np.array(data[2])
    Bt = np.array(data[3])

    for elem in At:
        # Списки вычесленных растояний
        As = []
        Bs = []
        # Определяем минимальные расстояния (k=1)
        for el in A:
            As.append(np.linalg.norm(el - elem))
        for el in B:
            Bs.append(np.linalg.norm(el - elem))       
        # print("AS")
        # print(As)
        if min(As) < min(Bs):
            print("Похоже на А")
        elif min(As) == min(Bs):
            print("Не ясно")
        else:
            print("Похоже на Б") 
    
    for elem in Bt:
        As = []
        Bs = []
        for el in A:
            As.append(np.linalg.norm(el - elem))
        for el in B:
            Bs.append(np.linalg.norm(el - elem)) 
        if min(As) < min(Bs):
            print("Похоже на А")
        elif min(As) == min(Bs):
            print("Не ясно")
        else:
            print("Похоже на Б")

# Метод эталонов
def Etalon(data):
    A = np.array(data[0])
    B = np.array(data[1])
    At = np.array(data[2])
    Bt = np.array(data[3])

    # Вычисление эталонных значений (центров)
    etalA = np.mean(A, axis = 0)
    etalB = np.mean(B, axis = 0)  

    for elem in At:
        # Определение расстояний до эталонынх значений
        As = np.linalg.norm(etalA - elem)       
        Bs = np.linalg.norm(etalB - elem)
        if As < Bs:
            print("Похоже на А")
        elif As == Bs:
            print("Не ясно")
        else:
            print("Похоже на Б") 

    for elem in Bt:
        As = np.linalg.norm(etalA - elem)       
        Bs = np.linalg.norm(etalB - elem)
        if As < Bs:
            print("Похоже на А")
        elif As == Bs:
            print("Не ясно")
        else:
            print("Похоже на Б") 


# Метод гиперсферы (дробящихся эталонов)
def HyperSphere(data):
    A = np.array(data[0])
    B = np.array(data[1])
    At = np.array(data[2])
    Bt = np.array(data[3])

    # Вычисление эталонных занчений
    etalA = np.mean(A, axis = 0)
    etalB = np.mean(B, axis = 0)
    # Определение расстояний каждого элмента класса до эталонного значения
    farSA = []
    for el in A:
        farSA.append(np.linalg.norm(el - etalA))
    farSB = []
    for el in B:
        farSB.append(np.linalg.norm(el - etalB))
    # Формирование радиусов гиперсфер
    farA = max(farSA)
    farB = max(farSB)

    # intercep = []
    # for el in A:
    #     doA = np.linalg.norm(el - etalA) 
    #     doB = np.linalg.norm(el - etalB)
    #     if doA < farA and doB < farB:
    #         intercep.append(el)
    # # print(intercep)  

    # если будет пересечения вынести в рекурсию
    for el in At:
        # вычисление расстояний до эталонов, чтобы определить принадлежность к гиперсфере
        doA = np.linalg.norm(el - etalA) 
        doB = np.linalg.norm(el - etalB)
        # print(doA)
        # print(doB)
        if doA < farA and doB < farB:
            print("Не ясно")
        elif doA < farA:
            print("Похоже на А")
        elif doB < farB:
            print("Похоже на Б")
       
        else:
            print("За пределами разумного")
    for el in Bt:
        doA = np.linalg.norm(el - etalA) 
        doB = np.linalg.norm(el - etalB)
        # print(doA)
        # print(doB)
        if doA < farA and doB < farB:
            print("Не ясно")
        elif doA < farA:
            print("Похоже на А")
        elif doB < farB:
            print("Похоже на Б")
        else:
            print("За пределами разумного")

def main():
    data = DataSet()
    print("\nМетод эталонов:")
    Etalon(data)
    print("\nМетод соседа:")
    NeighbourNextDoor(data)
    print("\nМетод гиперсферы:")
    HyperSphere(data)
   
  
if __name__ == '__main__': 
    main()








# def RemoveOneElem(At):
#     list_At_mini = []
#     for el in At:
#         list_now = []
#         for i in range(len(el)):
#             at_mini = [x for z, x in enumerate(el) if z != i]

#             list_now.append(at_mini)
#         list_At_mini.append(list_now)
#     # print(list_At_mini) 
#     print(At)
#     print('------')
#     print(len(list_At_mini[0]))
#     return list_At_mini


    # list_A_mini = RemoveOneElem(A)
    # list_B_mini = RemoveOneElem(B)
    # list_At_mini = RemoveOneElem(At)
    # list_Bt_mini =RemoveOneElem(Bt)

    # print(len(list_A_mini))
    # print(len(A))