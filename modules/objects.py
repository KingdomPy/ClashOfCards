import pygame
import math

def distanceLinePoint(line, point, size):
    x0 = point[0]
    y0 = point[1]
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    #Check if point is within rectangle surrounding bordering the line
    if x0 >= min(x1,x2) and x0 <= max(x1,x2) and y0 >= min(y1,y2) and y0 <= max(y1,y2):
        distance = abs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/math.sqrt((y2-y1)**2+(x2-x1)**2)
        return distance <= 1+size

class entity:
    def __init__(self, tag, stats, position=(0,0,0), size=30):
        self.tag = tag
        self.stats = stats
        self.x = position[0]
        self.y = position[1]
        self.angle = position[2]
        self.visualAngle = self.angle
        self.size = size
        self.speed = 3
        self.clock = 0
        self.animation = False
        #Collision complexity
        self.complexity = 10
        #Conditions (e.g. hp, mana, cooldowns, is alive?)
        self.loadConditions()
        
    def loadConditions(self):
        try:
            self.name = self.stats["name"]
        except:
            self.name = self.tag+":nameNotSet"
        try:
            self.hp = self.stats["hp"]
        except:
            self.hp = 10
        try:
            self.maxHp = self.stats["maxHp"]
        except:
            self.maxHp = self.hp
        try:
            self.colour = self.stats["colour"]
        except:
            self.colour = (0,0,0)

    def moveForward(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)

    def rotate(self, strength):
        if strength == 1:
            self.angle += self.speed/80
        elif strength == -1:
            self.angle -= self.speed/80        
        else:
            self.angle += strength
        self.angle %= 2*math.pi

    def getImage(self):
        point1 = [self.x+self.size*math.cos(self.visualAngle), self.y+self.size*math.sin(self.visualAngle)]
        point2 = [self.x+self.size*math.cos(self.visualAngle+math.pi/2), self.y+self.size*math.sin(self.visualAngle+math.pi/2)]
        point3 = [self.x+self.size*math.cos(self.visualAngle+math.pi), self.y+self.size*math.sin(self.visualAngle+math.pi)]
        point4 = [self.x+self.size*math.cos(self.visualAngle+(3*math.pi/2)), self.y+self.size*math.sin(self.visualAngle+(3*math.pi/2))]
        return point1,point2,point3,point4

    def collision(self, bullet, size):
        return False

    def renderData(self):
        return (self.x,self.y),self.getImage(), self.colour

    def hitProcedure(self, damage):
        pass
        
    def update(self, externalData = []):
        self.visualAngle += math.pi/800
        self.visualAngle %= 2*math.pi  

        self.clock += 16
        self.clock %= 960

class location(entity):
    def __init__(self, tag, stats, position=(0,0,0), size=60):
        super().__init__(tag, stats, position, size)
        self.name = self.stats["name"]
        self.colour = self.stats["colour"]
        self.speed = 1

    def getImage(self):
        point1 = [self.x+self.size*math.cos(self.visualAngle), self.y+self.size*math.sin(self.visualAngle)]
        point2 = [self.x+self.size*math.cos(self.visualAngle+math.pi/2), self.y+self.size*math.sin(self.visualAngle+math.pi/2)]
        point3 = [self.x+self.size*math.cos(self.visualAngle+math.pi), self.y+self.size*math.sin(self.visualAngle+math.pi)]
        point4 = [self.x+self.size*math.cos(self.visualAngle+(3*math.pi/2)), self.y+self.size*math.sin(self.visualAngle+(3*math.pi/2))]
        return point1,point2,point3,point4

    def update(self, externalData=[]):
        returns = []
        if externalData != []:
            playerx, playery = externalData[0]
            distance = math.sqrt((self.y-playery)**2 + (self.x-playerx)**2)
            if distance <= self.size*5:
                returns = (distance, self.name, self.colour)
            
        #AI
        self.visualAngle += math.pi/800
        self.visualAngle %= 2*math.pi  

        self.clock += 16
        self.clock %= 960
        self.clock %= 2880

        if returns != []:
            return returns

class triangle(entity):
    def __init__(self, tag, stats, position=(0,0,0), size=30):
        super().__init__(tag, stats, position, size)
        self.speed = 2

    def getImage(self):
        point1 = [self.x+self.size*math.cos(self.angle), self.y+self.size*math.sin(self.angle)]
        point2 = [self.x+self.size*math.cos(self.angle+(7*math.pi)/9), self.y+self.size*math.sin(self.angle+(7*math.pi)/9)]
        point3 = [self.x+self.size*math.cos(self.angle-(7*math.pi)/9), self.y+self.size*math.sin(self.angle-(7*math.pi)/9)]
        return point1,point2,point3

    def collision(self, bullet, size):
        size = self.size
        #List of lines to check
        checks = []
        for i in range(self.complexity):
            size -= self.size/self.complexity
            point1 = [size*math.cos(self.angle)+self.x, size*math.sin(self.angle)+self.y]
            point2 = [size*math.cos(self.angle+(7*math.pi)/9)+self.x, size*math.sin(self.angle+(7*math.pi)/9)+self.y]
            point3 = [size*math.cos(self.angle-(7*math.pi)/9)+self.x, size*math.sin(self.angle-(7*math.pi)/9)+self.y]
            checks.append(point1)
            checks.append(point2)
            checks.append(point3)
        for i in range(len(checks)):
            touching = distanceLinePoint((checks[i],checks[(i+1)%len(checks)]), bullet, size)
            if touching:
                self.hp -= 2
                self.hitProcedure(2)
                return True
    
    def update(self, externalData=[]):
        if self.hp > 0:
            #AI
            if self.clock < 960:
                self.moveForward()
                self.moveForward()
                self.rotate(-1)
            elif self.clock < 1920:
                self.rotate(1)
                self.rotate(1)
            elif self.clock < 2880:
                self.moveForward()
                self.moveForward()
                self.rotate(1)
                
            self.clock += 16
            self.clock %= 2880
        else:
            return 0

class square(entity):
    def __init__(self, tag, stats, position=(0,0,0), size=30):
        super().__init__(tag, stats, position, size)
        self.speed = 2
        self.visualAngle = self.angle

    def getImage(self):
        point1 = [self.x+self.size*math.cos(self.visualAngle), self.y+self.size*math.sin(self.visualAngle)]
        point2 = [self.x+self.size*math.cos(self.visualAngle+math.pi/2), self.y+self.size*math.sin(self.visualAngle+math.pi/2)]
        point3 = [self.x+self.size*math.cos(self.visualAngle+math.pi), self.y+self.size*math.sin(self.visualAngle+math.pi)]
        point4 = [self.x+self.size*math.cos(self.visualAngle+(3*math.pi/2)), self.y+self.size*math.sin(self.visualAngle+(3*math.pi/2))]
        return point1,point2,point3,point4

    def collision(self, bullet, size):
        size = self.size
        #List of lines to check
        checks = []
        for i in range(self.complexity):
            size -= self.size/self.complexity
            point1 = [self.x+size*math.cos(self.visualAngle), self.y+size*math.sin(self.visualAngle)]
            point2 = [self.x+size*math.cos(self.visualAngle+math.pi/2), self.y+size*math.sin(self.visualAngle+math.pi/2)]
            point3 = [self.x+size*math.cos(self.visualAngle+math.pi), self.y+size*math.sin(self.visualAngle+math.pi)]
            point4 = [self.x+size*math.cos(self.visualAngle+(3*math.pi/2)), self.y+size*math.sin(self.visualAngle+(3*math.pi/2))]
            checks.append(point1)
            checks.append(point2)
            checks.append(point3)
            checks.append(point4)
        for i in range(len(checks)):
            touching = distanceLinePoint((checks[i],checks[(i+1)%len(checks)]), bullet, size)
            if touching:
                self.hp -=2
                self.hitProcedure(2)
                return True

    def update(self, externalData=[]):
        if self.hp > 0:
            #AI
            if self.clock < 960:
                self.moveForward()
                self.moveForward()
            elif self.clock < 1920:
                self.rotate(math.pi/60)
            elif self.clock < 2880:
                self.moveForward()
                self.moveForward()
                self.moveForward()
                self.moveForward()
            elif self.clock < 3840:
                self.rotate(math.pi/60)
            elif self.clock < 4800:
                self.moveForward()
                self.moveForward()
            self.visualAngle += math.pi/50
            self.visualAngle %= 2*math.pi

            self.clock += 16
            self.clock %= 4800
        else:
            return 0
                                                       
class player(entity):
    def __init__(self, tag, stats, position=(0,0,0), size=30):
        super().__init__(tag, stats, position, size)
        self.speed = 6

    def getImage(self):
        point1 = [self.size*math.cos(self.angle), self.size*math.sin(self.angle)]
        point2 = [self.size*math.cos(self.angle+(7*math.pi)/9), self.size*math.sin(self.angle+(7*math.pi)/9)]
        point3 = [self.size*math.cos(self.angle-(7*math.pi)/9), self.size*math.sin(self.angle-(7*math.pi)/9)]
        return point1,point2,point3

    def update(self, externalData=[]):
        pass
        
class bullet(entity):
    def __init__(self, tag, stats, position=(0,0,0), size=30):
        super().__init__(tag, stats, position, size)
        self.speed = 10
        self.size = 5

    def getImage(self):
        point1 = [self.x+self.size*math.cos(self.visualAngle), self.y+self.size*math.sin(self.visualAngle)]
        point2 = [self.x+self.size*math.cos(self.visualAngle+math.pi/2), self.y+self.size*math.sin(self.visualAngle+math.pi/2)]
        point3 = [self.x+self.size*math.cos(self.visualAngle+math.pi), self.y+self.size*math.sin(self.visualAngle+math.pi)]
        point4 = [self.x+self.size*math.cos(self.visualAngle+(3*math.pi/2)), self.y+self.size*math.sin(self.visualAngle+(3*math.pi/2))]
        return point1,point2,point3,point4

    def hasHit(self):
        #Any code to be run
        pass
    
    def update(self, externalData=[]):
        if self.clock < 1920:
            self.moveForward()
        else:
            return 0

        self.visualAngle += math.pi/20
        self.visualAngle %= 2*math.pi
        
        self.clock += 16
        
