
import pygame
import random
import math
from ModelGame import Unit, Aggressor, Altruist, Egoist, Food,  Wall, Hero
from pprint import pprint

pygame.init()
sizeMap = {'x': 1366,'y': 768}
screen = pygame.display.set_mode(tuple(sizeMap.values()))
clock = pygame.time.Clock()

sizeChunks = 40
chunks = []
listHero = []
listWalls = []
listFood = []

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

    for wall in listWalls:
        pygame.draw.circle(screen, wall.color, tuple(wall.position.values()), wall.size)
    for food in listFood:
        pygame.draw.circle(screen, food.color, tuple(food.position.values()), food.size)
        food.TestLife()
        # food.DrawHp(pygame, screen)
    for unit in listHero:
        unit.Move(chunks, sizeChunks, sizeMap, pygame, screen)
        # Отображение поля зрения героев
        if unit.hp > 0:
            pygame.draw.circle(screen, unit.colorMax, tuple(unit.position.values()), unit.overviewRadius, 1)
        # отрисовка героев
        pygame.draw.circle(screen, unit.color, tuple(unit.position.values()), unit.size)
        unit.TestLife()

        # unit.DrawHp(pygame, screen)

    # for i in range(len(chunks)):
    #     for j in range(len(chunks[0])): 
    #         for unit in chunks[i][j]:
    #             if type(unit) is Wall or type(unit) is Food:
    #                 pass
    #                 pygame.draw.circle(screen, unit.color, tuple(unit.position.values()), unit.size)
    #             if type(unit).__bases__[0] is Hero:
    #                 pass
    #                 unit.Move(chunks, sizeChunks, sizeMap, pygame, screen)
    #                 # Отображение поля зрения героев
    #                 if unit.hp > 0:
    #                     pygame.draw.circle(screen, unit.colorMax, tuple(unit.position.values()), unit.overviewRadius, 1)
    #                 # отрисовка героев
    #                 pygame.draw.circle(screen, unit.color, tuple(unit.position.values()), unit.size)
    #                 unit.TestLife()
                
             


# Инициализация юнитов игры
def UnitInit(amountOfWalls, amountOfFood, amountOfHeros):
    CreateChunks()
    GenerateWalls(amountOfWalls)
    GenerateFood(amountOfFood)
    GenerateHeros(amountOfHeros)

def GenerateWalls(amountOfWalls):
    # Генерируем стены
    while amountOfWalls > 0:
        wall = Wall( {'x': random.randint(10,1256), 'y': random.randint(10,768)}, (50,50,50), random.randint(5,80))
        # wall = Wall( {'x': 1100, 'y': 500}, (50,50,50), random.randint(5,80))
        chunks[wall.position['x'] // sizeChunks][wall.position['y'] // sizeChunks].append(wall)
        listWalls.append(wall)
        amountOfWalls -= 1

def GenerateFood(amountOfFood):
    # Генерируем еду
    while amountOfFood > 0:
        size = 15
        x, y = UnitsOverlayTest(size, listWalls)
        food = Food({'x': x, 'y': y}, (100,20,130), size, 500, 5)
        chunks[food.position['x'] // sizeChunks][food.position['y'] // sizeChunks].append(food)
        listFood.append(food)
        amountOfFood -= 1

def GenerateHeros(amountOfHeros):
    # Генерируем персонажей
    while amountOfHeros > 0:
        size = 10
        x, y = UnitsOverlayTest(size, listWalls)
        # x, y = 1050, 450
        speed = 4
        typeHero = random.randint(0,2)
        # typeHero = 0
        hero = None
        if typeHero == 0:
            color = (94, 180, 35)
            hero = Altruist({'x': x, 'y': y}, 6000, speed, 50, 20, color, size)
        elif typeHero == 1: 
            color = (35, 94, 180)
            hero = Egoist({'x': x, 'y': y}, 5000, speed, 80, 10, color, size)
            # hero.hp -= 2500
        elif typeHero == 2: 
            pass
            color = (180, 94, 35)
            hero = Aggressor({'x': x, 'y': y}, 8000, speed, 120, 20, color, size)
        chunks[hero.position['x'] // sizeChunks][hero.position['y'] // sizeChunks].append(hero)
        listHero.append(hero)
        amountOfHeros -= 1
   

#  Проверка перекрытия юнитов
def UnitsOverlayTest(sizeNewObj, listObjectsOnMap):
    flag = True
    while(flag):
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
    UnitInit(20, 8, 30)
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