import pygame
import random
import math

class Unit:
    def __init__(self, position = (50, 50), hp = 1000, speed = [5, 5], overviewRadius = 0, damage = 5, color = (0,0,0), size = 10):
        self.position = position
        self.hp = hp
        self.hpMax = hp
        self.speed = speed
        self.damage = damage
        self.color = color
        self.size = size
        self.overviewRadius = self.size + overviewRadius
        self.blockMove = False

    def move(self):
        if self.hp > 0:
            if random.random() < 0.05 and not self.blockMove:
                # self.speed = ((random.randint(-1,1)*4), (random.randint(-1,1)*4))
                self.speed = [(random.randint(-4,4)), (random.randint(-4,4))]
        self.position = (self.position[0] + self.speed[0], self.position[1] + self.speed[1])
            # if random.random() < 0.05 and not self.blockMove:
            #     self.speed = MoveRelativeTarget(random.randint(0, 1366), random.randint(0, 768), self.position[0], self.position[1], 4)
            # self.position = (int(self.position[0] + self.speed[0]), int(self.position[1] + self.speed[1]))
    
    def DetectedTarget(self):
        pass

class Altruist(Unit):
    def Heal(self):
        for hero in listHero:
            len = ((self.position[0] - hero.position[0]) ** 2 + (self.position[1] - hero.position[1]) ** 2) ** (1/2)
            # Лечение
            if len <= self.size + hero.size + 10 and self != hero and hero.hp > 0 and self.hp > 0 and hero.hp < hero.hpMax and type(hero) is not Aggressor :
                if (hero.hp < hero.hpMax and hero.hp > 0) or (self.hp > hero.hp):
                    
                    hero.color = (hero.color[0] + (hero.color[0] * self.damage)/hero.hp, 
                                   hero.color[1] + (hero.color[1] * self.damage)/hero.hp, 
                                    hero.color[2] + (hero.color[2] * self.damage)/hero.hp)
                    self.color = (self.color[0] - (self.color[0] * self.damage)/self.hp, 
                                   self.color[1] - (self.color[1] * self.damage)/self.hp, 
                                    self.color[2] - (self.color[2] * self.damage)/self.hp)
                    self.hp -= self.damage
                    hero.hp += self.damage
            # Бежать к больному или от агрессора
            if len <= self.overviewRadius + hero.size + 10 and self != hero and self.hp > 0 and hero.hp > 0 and hero.hp < hero.hpMax:
                if type(hero) is Aggressor:
                    self.blockMove = True
                    vectorMove = MoveRelativeTarget(hero.position[0], hero.position[1], self.position[0], self.position[1], 4)
                    self.position = (int(self.position[0] - vectorMove[0]), int(self.position[1] - vectorMove[1]))
                elif self.hp > hero.hp:
                    self.blockMove = True
                    vectorMove = MoveRelativeTarget(hero.position[0], hero.position[1], self.position[0], self.position[1], 5)
                    self.position = (int(self.position[0] + vectorMove[0]), int(self.position[1] + vectorMove[1]))
            else:
                self.blockMove = False
    
class Egoist(Unit):
     def Protection(self, hero):
        # for hero in listHero:
            len = ((self.position[0] - hero.position[0]) ** 2 + (self.position[1] - hero.position[1]) ** 2) ** (1/2)
            # Защита
            if len <= self.size + hero.size + 10 and self != hero and hero.hp > 0 and self.hp > 0:
                if hero.hp > 0 and self.hp > 0:
                    hero.color = (hero.color[0] - (hero.color[0] * self.damage)/hero.hp, 
                                   hero.color[1] - (hero.color[1] * self.damage)/hero.hp, 
                                    hero.color[2] - (hero.color[2] * self.damage)/hero.hp)
                    hero.hp -= self.damage
            if len <= self.overviewRadius + hero.size + 10 and self != hero and hero.hp > 0 and self.hp > 0:
                self.blockMove = True
                vectorMove = MoveRelativeTarget(hero.position[0], hero.position[1], self.position[0], self.position[1], 5)
                self.position = (int(self.position[0] + vectorMove[0]), int(self.position[1] +  vectorMove[1]))
            else:
                self.blockMove = False
class Aggressor(Unit):
     def Atack(self):
        for hero in listHero:
            len = ((self.position[0] - hero.position[0]) ** 2 + (self.position[1] - hero.position[1]) ** 2) ** (1/2)
            # Атака
            if len <= self.size + hero.size + 10 and self != hero:
                if hero.hp > 0 and self.hp > 0:
                    hero.color = (hero.color[0] - (hero.color[0] * self.damage)/hero.hp, 
                                   hero.color[1] - (hero.color[1] * self.damage)/hero.hp, 
                                    hero.color[2] - (hero.color[2] * self.damage)/hero.hp)
                    hero.hp -= self.damage
                    if type(hero) is Egoist:
                        hero.Protection(self)
           
            # Бежать к жертве
            if len <= self.overviewRadius + hero.size + 10 and self != hero and hero.hp > 0 and self.hp > 0:
                self.blockMove = True
                vectorMove = MoveRelativeTarget(hero.position[0], hero.position[1], self.position[0], self.position[1], 5)
                self.position = (int(self.position[0] + vectorMove[0]), int(self.position[1] +  vectorMove[1]))
            else:
                self.blockMove = False

class World:
    positionWall = (None, None)
    positionEat = (None, None)
    color = None
    size = None

    def __init__(self, positionWall = (None, None), color = (0, 0, 0), size = None):
        self.positionWall = positionWall
        self.color = color
        self.size = size

def MoveRelativeTarget(t0,t1,psx,psy,speed):    
    distance = [t0 - psx, t1 - psy]
    norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    if norm != 0:
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]
    else:
        bullet_vector = [0,0]
    return bullet_vector



listHero = []
listWall = []
listEat = []

listAltruists = []
listEgoist = []
listAggressor = []

def TestLife():
    for hero in listHero:
        hero.color = (hero.color[0], hero.color[1], hero.color[2])
        if hero.hp <= 0:
            hero.blockMove = True
            hero.hp = 0
            hero.speed = [0,0]


def WorldInit(numberHero, numberWall):
    while numberWall > 0:
        wall = World((random.randint(10,1256), random.randint(10,768)), (50,50,50), random.randint(5,80))
        listWall.append(wall)
        numberWall -= 1
    while numberHero > 0:
        flag = True
        size = 10
        # Генерировать героев не в камнях
        while(flag):
            x = random.randint(100,1266)
            y = random.randint(100,668)
            for wall in listWall:
                len = (((wall.positionWall[0] - x) ** 2) + ((wall.positionWall[1] - y) ** 2)) ** (1/2)
                if len <= (wall.size + size):
                    flag = True
                    break
                else:
                    flag = False
                    continue
                    
        speedX = 0
        speedY = 0
        typeHero = random.randint(0,2)
        # typeHero = 0
        hero = None
        if typeHero == 0:
            color = (94, 180, 35)
            hero = Altruist((x,y), 6000, [speedX, speedY], 50, 20, color, size)
        elif typeHero == 1: 
            color = (35, 94, 180)
            hero = Egoist((x,y), 5000, [speedX, speedY], 80, 15, color, size)
        elif typeHero == 2 or typeHero == 1: 
            color = (180, 94, 35)
            hero = Aggressor((x,y), 5000, [speedX, speedY], 120, 20, color, size)
        listHero.append(hero)
        numberHero -= 1
 


def RedrawingWorld(screen = None, surface = None):
    for wall in listWall:
        pygame.draw.circle(screen, wall.color, wall.positionWall, wall.size)
    for unit in listHero:
        unit.move()
        if type(unit) is Altruist:
            unit.Heal()
        # if type(unit) is Egoist:
        #     unit.Protection()
        if type(unit) is Aggressor:
            unit.Atack()
        if unit.hp > 0:
            pygame.draw.circle(screen, (0,100,160), unit.position, unit.overviewRadius, 2)
        pygame.draw.circle(screen, unit.color, unit.position, unit.size)
    DrawHp(screen)
    TestLife()
    CheckCollision()

def DrawHp(screen = None):
    for unit in listHero:
        # if unit.hp > 0:
        #     damage = 1
        #     unit.color = (unit.color[0] - (unit.color[0] * damage)/unit.hp, 
        #                            unit.color[1] - (unit.color[1] * damage)/unit.hp, 
        #                             unit.color[2] - (unit.color[2] * damage)/unit.hp)
        #     unit.hp -= damage
        fontObj = pygame.font.Font('freesansbold.ttf', 8)
        textSurfaceObj = fontObj.render(str(unit.hp), True, (255,255,255))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (unit.position[0], unit.position[1])
        screen.blit(textSurfaceObj, textRectObj)

def CheckCollision():
    for hero in listHero:
        for wall in listWall:
            len = ((wall.positionWall[0] - (hero.position[0] + hero.speed[0]-2)) ** 2 + (wall.positionWall[1] - (hero.position[1] + hero.speed[1]-2)) ** 2) ** (1/2) 
            if (wall.size + hero.size) - len > 0:
                vectorMove = MoveRelativeTarget(wall.positionWall[0], wall.positionWall[1], hero.position[0], hero.position[1], 2)
                hero.position = (int(hero.position[0] - vectorMove[0]*3), int(hero.position[1] -  vectorMove[1]*3))


            # len = ((wall.positionWall[0] - (hero.position[0] + hero.speed[0]-2)) ** 2 + (wall.positionWall[1] - (hero.position[1] + hero.speed[1]-2)) ** 2) ** (1/2) 
            # if (wall.size + hero.size) - len > 0:
            #     # hero.color = (255,255,255)
            #     # hero.speed = ((random.randint(0, int(wall.positionWall[0]/250))), (random.randint(0, int(wall.positionWall[1]/250))))
            #     hero.speed = (int(-hero.speed[0]/(3/2)), int(-hero.speed[1]/(3/2)))
            # else:
            #     pass

                # hero.color = (240, 94, 35)
    # for hero1 in listHero:
    #     for hero2 in listHero:
    #         if hero1.hp > 0 or hero2.hp > 0:
    #             len = (((hero1.position[0] - hero2.position[0]) ** 2) + ((hero1.position[1] - hero2.position[1]) ** 2)) ** (1/2)
    #             if len <= (hero1.size + hero2.size) and hero1 != hero2 :
    #                 # hero1
    #                 # print(str(len) + " " + str(hero1.size + hero2.size))
                    
    #                 # deltaHp1 = hero1.hp - hero2.damage
    #                 # deltaHp2 = hero2.hp - hero1.damage
    #                 # if deltaHp1 <= 0:
    #                 #     hero1.hp = 0
    #                 #     break
    #                 # if deltaHp2 <= 0:
    #                 #     hero2.hp = 0
    #                 #     break
    #                 # hero1.color = ((hero1.color[0] * deltaHp1)/hero1.hp, 
    #                 #                 (hero1.color[1] * deltaHp1)/hero1.hp, 
    #                 #                 (hero1.color[2] * deltaHp1)/hero1.hp)
    #                 # hero2.color = ((hero1.color[0] * deltaHp2)/hero2.hp,
    #                 #                 (hero1.color[1] * deltaHp2)/hero2.hp, 
    #                 #                 (hero1.color[2] * deltaHp2)/hero2.hp)

    #                 # hero1.hp = deltaHp1
    #                 # hero2.hp = deltaHp2
    #                 pass
    #             else:
    #                 pass
    for hero in listHero:
        if hero.position[0] + hero.size < 30:
            hero.speed = [(random.randint(5,5)*2)-5, (random.randint(0,5)*2)-5]
        elif hero.position[0] + hero.size > size[0]:
            hero.speed = [(random.randint(0,0)*2)-5, (random.randint(0,5)*2)-5]
        elif hero.position[1] + hero.size < 30:
            hero.speed = [(random.randint(0,5)*2)-5, (random.randint(5,5)*2)-5]
        elif hero.position[1] + hero.size > size[1]:
            hero.speed = [(random.randint(0,5)*2)-5, (random.randint(0,0)*2)-5]
    # for hero in listHero:
    #     if hero.position[0] + hero.size < 30:
    #         hero.speed = MoveRelativeTarget(0, hero.position[1], hero.position[0], hero.position[1], 4)
    #         hero.position = (int(hero.position[0] - hero.speed[0]), int(hero.position[1] - hero.speed[1]))
    #     elif hero.position[0] + hero.size > size[0]:
    #         hero.speed = MoveRelativeTarget(size[0], hero.position[1], hero.position[0], hero.position[1], 4)
    #         hero.position = (int(hero.position[0] - hero.speed[0]), int(hero.position[1] - hero.speed[1]))
    #     elif hero.position[1] + hero.size < 30:
    #         hero.speed = MoveRelativeTarget(hero.position[0], 0, hero.position[0], hero.position[1], 4)
    #         hero.position = (int(hero.position[0] - hero.speed[0]), int(hero.position[1] - hero.speed[1]))
    #     elif hero.position[1] + hero.size > size[1]:
    #         hero.speed = MoveRelativeTarget(hero.position[0], size[1], hero.position[0], hero.position[1], 4)
    #         hero.position = (int(hero.position[0] - hero.speed[0]), int(hero.position[1] - hero.speed[1]))
    


pygame.init()
size = [1366, 768]
screen = pygame.display.set_mode(size)
surface = pygame.Surface(size, pygame.SRCALPHA)

clock = pygame.time.Clock()


def main():
    running = True
    WorldInit(15, 50)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                    # пишем свой код
        # обновляем значения
        screen.fill((10, 130, 80))
        
        RedrawingWorld(screen, surface)

        # рисуем
        pygame.display.flip()
      
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main() 