
import random
import math
from operator import itemgetter
import operator


class Unit:
    def __init__(self, position = {'x': 50, 'y': 50}, color = (0, 0, 0), size = 10):
        self.position = position
        self.color = color
        self.size = size

class Hero(Unit):

    def __init__(self, position = {'x': 50, 'y': 50}, hp = 1000, speed = 4, overviewRadius = 30, damage = 5, color = (0,0,0), size = 10, angle = 0):
        super().__init__(position, color, size)
        self.hp = hp
        self.hpMax = hp
        self.speed = speed
        self.angle = angle
        self.damage = damage
        self.overviewRadius = self.size + overviewRadius
        self.colorMax = color
        self.blockMove = False
        self.visibleUnits = set()
        
    def Move(self, chunks, sizeChunks, sizeMap, pygame, screen):
        pass
        # canMove = True
        if not self.blockMove:

            if random.random() < 0.5:
                self.angle += random.uniform(-30, 30)
            # Корректировка движения в зависимости от окружения
            self.MovementByEvent(chunks, sizeChunks, pygame, screen)
       
            # if not self.blockMove:
            self.TestBordersMap(self, sizeMap, chunks, sizeChunks)
            dx = math.sin(self.angle * (math.pi / 180)) * self.speed
            dy = math.cos(self.angle * (math.pi / 180)) * self.speed 
            # Переместим объект на карте, а также из чанка в чанк + можно включать отображение чанков героеев до после
            # pygame.draw.rect(screen, (255, 255, 255), (self.position['x'] // sizeChunks * sizeChunks, self.position['y'] // sizeChunks * sizeChunks, 40, 40), 2)
            chunks[self.position['x'] // sizeChunks][self.position['y'] // sizeChunks].remove(self)
            self.position['x'] += int(dx)
            self.position['y'] += int(dy)
            chunks[self.position['x'] // sizeChunks][self.position['y'] // sizeChunks].append(self)
            # pygame.draw.rect(screen, (255, 50, 50), (self.position['x'] // sizeChunks * sizeChunks, self.position['y'] // sizeChunks * sizeChunks, 40, 40), 2)
            # pygame.draw.aaline(screen, (250,250,250), [self.position['x'], self.position['y']], [self.position['x'] + dx *8, self.position['y'] + dy *8])

    def TestBordersMap(self, unit, sizeMap, chunks, sizeChunks):
        # if unit.position['x']  + unit.size < 20 or unit.position['x']  + unit.size > sizeMap['x'] - 20 or unit.position['y']  + unit.size < 20 or unit.position['y']  + unit.size > sizeMap['y'] - 20:
        #     unit.angle -= 180
        #     # dx = math.sin(unit.angle * (math.pi / 180)) * unit.speed
        #     # dy = math.cos(unit.angle * (math.pi / 180)) * unit.speed 
        #     # chunks[unit.position['x'] // sizeChunks][unit.position['y'] // sizeChunks].remove(unit)
        #     # unit.position['x'] += int(dx)
        #     # unit.position['y'] += int(dy)
        #     # chunks[unit.position['x'] // sizeChunks][unit.position['y'] // sizeChunks].append(unit)
        #     return True;
        if unit.position['x']  + unit.size < 20:
            unit.angle = 90
            return True
        if unit.position['x']  + unit.size > sizeMap['x'] - 20:
            unit.angle = -90
            return True
        if unit.position['y']  + unit.size < 20:
            unit.angle = 0
            return True
        if unit.position['y']  + unit.size > sizeMap['y'] - 20:
            unit.angle = 180
            return True


        # if unit.position['x']  + unit.size < 20 or unit.position['x']  + unit.size > sizeMap['x'] - 20:
        #     unit.angle -= 180
        # if unit.position['y']  + unit.size < 20 or unit.position['y']  + unit.size > sizeMap['y'] - 20:
        #     unit.angle -= 180
        return False

    def MovementByEvent(self, chunks, sizeChunks, pygame, screen):
         for i in range(len(chunks)):
                for j in range(len(chunks[0])): 
                    for unit in chunks[i][j]:

                        # Встреча героя с другими персонажами или едой
                        if type(unit).__bases__[0] is Hero and unit.hp > 0:
                            listTargets = list()

                            viewCells = 2 *unit.overviewRadius // sizeChunks
                            minX = 0 if (i - viewCells + 1 ) <= 0 else i - viewCells  + 1
                            maxX = len(chunks) if (i + viewCells ) >= len(chunks) else i + viewCells 
                            minY = 0 if (j - viewCells  + 1) <= 0 else j - viewCells + 1
                            maxY = len(chunks[0]) if (j + viewCells ) >= len(chunks[0]) else j + viewCells 
                            # pygame.draw.rect(screen, unit.color, (minX * sizeChunks, minY * sizeChunks, (maxX - minX) * sizeChunks, (maxY - minY) * sizeChunks), 2)
                            for col in range(minX, maxX):
                                for row in range(minY, maxY):
                                    for objcecVisible in chunks[col][row]:
                                        dist = ((unit.position['x'] - objcecVisible.position['x']) ** 2 + (unit.position['y'] - objcecVisible.position['y']) ** 2) ** (1/2)
                                        # Если герой видит другого героя
                                        if type(objcecVisible).__bases__[0] is Hero and objcecVisible != unit and objcecVisible.hp > 0 and unit.hp > 0:
                                            if dist <= unit.overviewRadius + objcecVisible.size:
                                                pass
                                                listTargets.append((objcecVisible, dist))
                                        if len(listTargets) > 0: 
                                            # В зависимости от вида героя выполняем взаимодейтсвие с остальными
                                            self.HeroDecisionMaking(unit, listTargets)
                                        
                                        # Если герой видит еду
                                        if type(objcecVisible) is Food:
                                            if dist <= unit.overviewRadius + objcecVisible.size:
                                                pass
                                                # В зависимости от вида героя полполняем Hp за счет еды
                                                if (type(unit) is Altruist or type(unit) is Egoist) and unit.hp < unit.hpMax and objcecVisible.hp > 0:
                                                    unit.Eat(objcecVisible)

                        # Если сталкиваемся со стеной
                        if type(unit) is Wall:
                            viewCells = 2 *unit.size // sizeChunks
                            minX = 0 if (i - viewCells - 1) <= 0 else i - viewCells - 1
                            maxX = len(chunks) if (i + viewCells + 2) >= len(chunks) else i + viewCells + 2
                            minY = 0 if (j - viewCells - 1) <= 0 else j - viewCells - 1
                            maxY = len(chunks[0]) if (j + viewCells + 2) >= len(chunks[0]) else j + viewCells + 2
                            # pygame.draw.rect(screen, (255, 255, 255), (minX * sizeChunks, minY * sizeChunks, (maxX - minX) * sizeChunks, (maxY - minY) * sizeChunks), 2)
                            # print(str(minX) + " " + str(maxX) + " " + str(minY) + " " + str(maxY))
                            for col in range(minX, maxX):
                                for row in range(minY, maxY):
                                    for hero in chunks[col][row]:
                                        if type(hero).__bases__[0] is Hero:
                                            dist = ((unit.position['x'] - hero.position['x']) ** 2 + (unit.position['y'] - hero.position['y']) ** 2) ** (1/2)
                                            if dist <= unit.size + hero.size + 1:
                                                pass
                                                # print(str(hero.angle) + " DO")
                                                hero.angle -= 180
                                                # hero.angle = math.degrees(math.atan2(hero.position['y']  - unit.position['y'], hero.position['x']  - unit.position['x']))
                                                dxT = math.sin(hero.angle * (math.pi / 180)) * hero.speed
                                                dyT = math.cos(hero.angle * (math.pi / 180)) * hero.speed  
                                                chunks[hero.position['x'] // sizeChunks][hero.position['y'] // sizeChunks].remove(hero)
                                                hero.position['x'] += int(dxT)
                                                hero.position['y'] += int(dyT)
                                                chunks[hero.position['x'] // sizeChunks][hero.position['y'] // sizeChunks].append(hero)

    # Соверешние героем выбора в зависимости от параметров соседей  
    def HeroDecisionMaking(self, unit, listObjectVisible):
        listTargetForAltruist, listTargetForEgoist, listTargetForAggressor = self.UnitsActionLogic(listObjectVisible)
        if type(unit) is Altruist:
            target = listTargetForAltruist[0]
            if (type(target) is Egoist or type(target) is Altruist) and target.hp < unit.hp and target.hp < target.hpMax and abs(unit.hp - target.hp) > unit.damage:
                unit.Heal(target)
            if type(target) is Aggressor:
                unit.Save(target)
        if type(unit) is Egoist:
            target = listTargetForEgoist[0]
            unit.Protection()
        if type(unit) is Aggressor:
            target = listTargetForAggressor[0]
            unit.Attack(target)

    # Разбитие списка целей на группы и выделение их основных параметров
    def UnitsActionLogic(self, listObjectVisible):

        sortedTatgets = dict()
        dictMinMaxParametersTargets = dict()

        sortedTatgets['Altruist']  = [x for x in listObjectVisible if type(x[0]) is Altruist]
        sortedTatgets['Egoist']  = [x for x in listObjectVisible if type(x[0]) is Egoist]
        sortedTatgets['Aggressor']  = [x for x in listObjectVisible if type(x[0]) is Aggressor]

        for typeHero in sortedTatgets:
            if len(sortedTatgets[typeHero]) > 0:
                listHero = [x[0] for x in sortedTatgets[typeHero]]
                dictMinMaxParametersTargets["dist"] = {'min': min(sortedTatgets[typeHero], key=itemgetter(1))[0], 'max': max(sortedTatgets[typeHero], key=itemgetter(1))[0] }
                dictMinMaxParametersTargets["hp"] = {'min': min(listHero, key=operator.attrgetter('hp')), 'max': max(listHero, key=operator.attrgetter('hp'))}
                dictMinMaxParametersTargets["speed"] = {'min': min(listHero, key=operator.attrgetter('speed')), 'max': max(listHero, key=operator.attrgetter('speed'))}
                dictMinMaxParametersTargets["damage"] = {'min': min(listHero, key=operator.attrgetter('damage')), 'max': max(listHero, key=operator.attrgetter('damage'))}
                sortedTatgets[typeHero] = dictMinMaxParametersTargets
            else:
                sortedTatgets[typeHero] = None 
        sortedTatgets['All'] = [x[0] for x in listObjectVisible]
        return self.СreatingQueuesTargets(sortedTatgets)

    def СreatingQueuesTargets(self, sortedTatgets):
        listTargetForAltruist = list()
        listTargetForEgoist = list()
        listTargetForAggressor = list()

        if sortedTatgets['Aggressor'] != None: listTargetForAltruist.append(sortedTatgets['Aggressor']['dist']['min']) 
        if sortedTatgets['Egoist'] != None: listTargetForAltruist.append(sortedTatgets['Egoist']['dist']['min'])
        if sortedTatgets['Egoist'] != None: listTargetForAltruist.append(sortedTatgets['Egoist']['hp']['min'])
        if sortedTatgets['Altruist'] != None: listTargetForAltruist.append(sortedTatgets['Altruist']['dist']['min'])
        if sortedTatgets['Altruist'] != None: listTargetForAltruist.append(sortedTatgets['Altruist']['hp']['min'])
        listTargetForAltruist.extend(sortedTatgets['All'])

        if sortedTatgets['Aggressor'] != None: listTargetForEgoist.append(sortedTatgets['Aggressor']['dist']['min'])
        if sortedTatgets['Altruist'] != None: listTargetForEgoist.append(sortedTatgets['Altruist']['dist']['min'])
        listTargetForEgoist.extend(sortedTatgets['All'])
        
        if sortedTatgets['Altruist'] != None: listTargetForAggressor.append(sortedTatgets['Altruist']['dist']['min'])
        if sortedTatgets['Altruist'] != None: listTargetForAggressor.append(sortedTatgets['Altruist']['hp']['min'])
        if sortedTatgets['Egoist'] != None: listTargetForAggressor.append(sortedTatgets['Egoist']['dist']['min'])
        if sortedTatgets['Egoist'] != None: listTargetForAggressor.append(sortedTatgets['Egoist']['hp']['min'])
        if sortedTatgets['Aggressor'] != None: listTargetForAggressor.append(sortedTatgets['Aggressor']['dist']['min'])
        listTargetForAggressor.extend(sortedTatgets['All'])

        return list(set(listTargetForAltruist)), list(set(listTargetForEgoist)), list(set(listTargetForAggressor))
        # dictMinMaxParametersTargets = dict()
        # listHeros = [x[0] for x in listObjectVisible] if type(x[0]) is Altruist

        # dictMinMaxParametersTargets["dist"] = {'min': min(listObjectVisible, key=itemgetter(1)), 'max': max(listObjectVisible, key=itemgetter(1)) }
        # dictMinMaxParametersTargets["hp"] = {'min': min(listHeros, key=operator.attrgetter('hp')), 'max': max(listHeros, key=operator.attrgetter('hp'))}
        # dictMinMaxParametersTargets["speed"] = {'min': min(listHeros, key=operator.attrgetter('speed')), 'max': max(listHeros, key=operator.attrgetter('speed'))}
        # dictMinMaxParametersTargets["damage"] = {'min': min(listHeros, key=operator.attrgetter('damage')), 'max': max(listHeros, key=operator.attrgetter('damage'))}
        # return dictMinMaxParametersTargets


       


    # Отрисовка здоровья персонажей или другой дополнительной инфы (операция требовательна к ресурсам)
    def DrawHp(self, pygame = None, screen = None):
        fontObj = pygame.font.Font('freesansbold.ttf', 8)
        textSurfaceObj = fontObj.render(str(self.hp), True, (255,255,255))
        # textSurfaceObj = fontObj.render(str(self.position['x']) + "  " + str(self.position['y']), True, (255,255,255))
        if type(self) is Egoist:
            textSurfaceObj = fontObj.render(str(self.defenseTarget), True, (255,255,255))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (self.position['x'], self.position['y'])
        screen.blit(textSurfaceObj, textRectObj)

    # Проверка состояния героя и его перекрас под соответствующий уровень Hp
    def TestLife(self):
        if self.hp <= 0:
            self.blockMove = True
            self.hp = 0
            self.speed = 0
        else:
            self.color = (int(self.hp * self.colorMax[0] / self.hpMax), 
                        int(self.hp  * self.colorMax[1] / self.hpMax), 
                        int(self.hp  * self.colorMax[2] / self.hpMax))
    


class Altruist(Hero):
    def Heal(self, target):
        pass
        self.angle = math.degrees(math.atan2(self.position['x'] - target.position['x'], self.position['y'] - target.position['y'])) - 180 + random.randint(-30, 30)
        dist = ((self.position['x'] - target.position['x']) ** 2 + (self.position['y'] - target.position['y']) ** 2) ** (1/2)
        if dist <= self.size + target.size: 
            target.hp += self.damage
            self.hp -= self.damage
    def Save(self, target):
        self.angle = math.degrees(math.atan2(self.position['y'] - target.position['y'], self.position['x'] - target.position['x'])) + random.randint(-30, 30)
    def Eat(self, target):
        pass
        self.angle = math.degrees(math.atan2(self.position['x'] - target.position['x'], self.position['y'] - target.position['y'])) - 180 + random.randint(-30, 30)
        dist = ((self.position['x'] - target.position['x']) ** 2 + (self.position['y'] - target.position['y']) ** 2) ** (1/2)
        if dist <= self.size + target.size: 
            target.hp -= target.damage
            self.hp += target.damage
    
class Egoist(Hero):
    defenseTarget = None
    def Protection(self):
        pass
        if type(self.defenseTarget) is Aggressor:
            self.angle = math.degrees(math.atan2(self.position['x'] - self.defenseTarget.position['x'], self.position['y'] - self.defenseTarget.position['y'])) - 180 + random.randint(-30, 30)
            dist = ((self.position['x'] - self.defenseTarget.position['x']) ** 2 + (self.position['y'] - self.defenseTarget.position['y']) ** 2) ** (1/2)
            if dist <= self.size + self.defenseTarget.size: 
                self.defenseTarget.hp -= self.damage
                # Если в результате обороны цель уничтожена, то снять метку обороны 
                if self.defenseTarget.hp <= 0:
                    self.defenseTarget = None
    def Eat(self, target):
        pass
        self.angle = math.degrees(math.atan2(self.position['x'] - target.position['x'], self.position['y'] - target.position['y'])) - 180 + random.randint(-30, 30)
        dist = ((self.position['x'] - target.position['x']) ** 2 + (self.position['y'] - target.position['y']) ** 2) ** (1/2)
        if dist <= self.size + target.size: 
            target.hp -= target.damage
            self.hp += target.damage

class Aggressor(Hero):
    def Attack(self,target):
        pass
        self.angle = math.degrees(math.atan2(self.position['x'] - target.position['x'], self.position['y'] - target.position['y'])) - 180 + random.randint(-30, 30)
        dist = ((self.position['x'] - target.position['x']) ** 2 + (self.position['y'] - target.position['y']) ** 2) ** (1/2)
        if dist <= self.size + target.size: 
            target.hp -= self.damage
            if type(target) is Egoist:
                target.defenseTarget = self
                target.Protection()

class Food(Unit):
    def __init__(self, position = (None, None), color = (0, 0, 0), size = None, hp = 500, damage = 20):
        super().__init__(position, color, size)
        self.hp = hp
        self.hpMax = hp
        self.colorMax = color
        self.damage = damage

    def DrawHp(self, pygame = None, screen = None):
        fontObj = pygame.font.Font('freesansbold.ttf', 8)
        textSurfaceObj = fontObj.render(str(self.hp), True, (255,255,255))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (self.position['x'], self.position['y'])
        screen.blit(textSurfaceObj, textRectObj)

    def TestLife(self):
        if self.hp <= 0:
            self.hp = 0
        else:
            self.color = (int(self.hp * self.colorMax[0] / self.hpMax), 
                        int(self.hp  * self.colorMax[1] / self.hpMax), 
                        int(self.hp  * self.colorMax[2] / self.hpMax))

class Wall(Unit):
    def __init__(self, position = (None, None), color = (0, 0, 0), size = None):
        super().__init__(position, color, size)