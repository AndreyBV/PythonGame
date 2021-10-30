
import pygame
import random
import math
from ModelGame import Unit, Aggressor, Altruist, Egoist, Food,  Wall, Hero, Container, WareHouse, ChargingStation
from pprint import pprint

pygame.init()
sizeMap = {'x': 1366,'y': 768}
screen = pygame.display.set_mode(tuple(sizeMap.values()))
clock = pygame.time.Clock()

sizeChunks = 40
chunks = []
listHero = []
listContainer = []
listWareHouse = []
listChargingStation = []

def CreateChunks():
    for i in range(sizeMap['x'] // sizeChunks + 5):
        chunks.append([])
        for j in range(sizeMap['y'] // sizeChunks + 5):
            chunks[i].append([])

def ChunksDrawTmp():
    print(len(chunks[0]))
    for i in range(sizeMap['x'] // sizeChunks + 1):
        pygame.draw.aaline(screen, (20,20,20), [sizeChunks + i * sizeChunks, 0], [sizeChunks + i * sizeChunks, sizeMap['y']])
        for j in range(sizeMap['y'] // sizeChunks + 1):
            pygame.draw.aaline(screen, (20,20,20), [0, sizeChunks + j * sizeChunks], [sizeMap['x'], sizeChunks + j * sizeChunks])
    
def CheckCollision():
    for i in range(sizeMap['x'] // sizeChunks + 1):
        for j in range(sizeMap['y'] // sizeChunks + 1):
            pass

# Перерисовка юнитов
def RedrawingUnit():
    # ChunksDrawTmp()
    for wareHouse in listWareHouse:
        pygame.draw.circle(screen, wareHouse.color, tuple(wareHouse.position.values()), wareHouse.size)
    for chargingStation in listChargingStation:
        pygame.draw.circle(screen, chargingStation.color, tuple(chargingStation.position.values()), chargingStation.size)
        # food.TestLife()
    for container in listContainer:
        if len(listContainer) < 4:
            GenerateContainers(10)
        if not container.clean:
            pygame.draw.circle(screen, container.color, tuple(container.position.values()), container.size)
        else:
            listContainer.remove(container)
            for i in range(len(chunks)):
                for j in range(len(chunks[0])): 
                    for unit in chunks[i][j]:
                        if type(unit) is Container and unit == container:
                            chunks[i][j].remove(container)
    for unit in listHero:
        unit.Move(chunks, sizeChunks, sizeMap, pygame, screen)
        # unit.MoveToTarget(None, chunks, sizeChunks, sizeMap)
        # Отображение поля зрения героев
        if unit.hp > 0:
            pygame.draw.circle(screen, unit.colorMax, tuple(unit.position.values()), unit.overviewRadius, 1)
        # отрисовка героев
        pygame.draw.circle(screen, unit.color, tuple(unit.position.values()), unit.size)
        unit.TestLife(chunks, 10)
        # unit.DrawHp(pygame, screen)

def CleanContainers():
    pass
    # for container in listContainer:
    #     if container.clean:


# Инициализация юнитов игры
def UnitInit(amountOfWareHouse, amountOfChargingStation, amountOfContainers, amountOfHeros):
    CreateChunks()
    GenerateWareHouse(amountOfWareHouse)
    GenerateChargingStation(amountOfChargingStation)
    GenerateContainers(amountOfContainers)
    GenerateHeros(amountOfHeros)
  
def GenerateContainers(amountOfContainers):
    # Генерируем контейнеры
    while amountOfContainers > 0:
        size = 12
        x, y = random.randint(10,1256), random.randint(10,768)
        # x, y = UnitsOverlayTest(size, listChargingStation)
        # x, y = UnitsOverlayTest(size, listWareHouse, x, y)
        container = Container( {'x': x, 'y': y}, (50,50,50), size)
        chunks[container.position['x'] // sizeChunks][container.position['y'] // sizeChunks].append(container)
        listContainer.append(container)
        amountOfContainers -= 1
def GenerateWareHouse(amountOfWareHouse):
    # Генерируем склад
    while amountOfWareHouse > 0:
        wareHouse = WareHouse( {'x': random.randint(10,1256), 'y': random.randint(10,768)}, (0,0,0), 100)
        chunks[wareHouse.position['x'] // sizeChunks][wareHouse.position['y'] // sizeChunks].append(wareHouse)
        listWareHouse.append(wareHouse)
        amountOfWareHouse -= 1
def GenerateChargingStation(amountOfChargingStation):
    # Генерируем зарядные станции
    while amountOfChargingStation > 0:
        size = 50
        x, y = random.randint(10,1256), random.randint(10,768)
        # x, y = UnitsOverlayTest(size, listWareHouse)
        chargingStation = ChargingStation( {'x': x, 'y': y}, (220,20,60), size)
        chunks[chargingStation.position['x'] // sizeChunks][chargingStation.position['y'] // sizeChunks].append(chargingStation)
        listChargingStation.append(chargingStation)
        amountOfChargingStation -= 1
def GenerateHeros(amountOfHeros):
    # Генерируем персонажей
    while amountOfHeros > 0:
        size = 10
        # x, y = UnitsOverlayTest(size, listChargingStation)
        x, y = 700, 350
        speed = 4
        # typeHero = 0
        color = (0, 191, 255)
        hero = Hero({'x': x, 'y': y}, 10000, speed, 50, 20, color, size)

        chunks[hero.position['x'] // sizeChunks][hero.position['y'] // sizeChunks].append(hero)
        listHero.append(hero)
        amountOfHeros -= 1
 
#  Проверка перекрытия юнитов
def UnitsOverlayTest(sizeNewObj, listObjectsOnMap, x = None, y = None):
    flag = True
    while(flag):
        if x == None and y == None:
            x = random.randint(100,1266)
            y = random.randint(100,668)
        for objOnMap in listObjectsOnMap:
            len = (((objOnMap.position['x'] - x) ** 2) + ((objOnMap.position['y'] - y) ** 2)) ** (1/2)
            if len <= (objOnMap.size + sizeNewObj):
                flag = True
                break
            else:
                flag = False
                continue  
    return x, y

def main():
    running = True
    UnitInit(1, 2, 15, 8)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((10, 130, 80))
        
        RedrawingUnit()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main() 