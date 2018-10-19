import pygame
import math
        
class player:

    def __init__ (self, surface, red=255, green=255, blue=255):
        self.surface = surface
        self.x = 400
        self.y = 300
        self.velocity = 7
        self.size = 30
        self.angle = 0
        self.red = red
        self.green = green
        self.blue = blue
        self.originalColours = (red, green, blue)
        
    def teleport(self, x, y, angle=0, radians=False):
        self.x = x
        self.y = y
        self.angle = angle
        if not radians:
            self.angle = (angle/180)*math.pi
    
    def setColours(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        self.originalColours = (red, green, blue)

    def getColours(self):
        return (self.red, self.green, self.blue)

    def rotate(self, angle):
        self.angle += angle

    def getRotationPoints(self):
        #Reset angle
        self.angle %= 2*math.pi
        
        #Set points and rotate on the unit circle
        point1 = [self.size*math.cos(self.angle), self.size*math.sin(self.angle)]
        point2 = [self.size*math.cos(self.angle+(7*math.pi)/9), self.size*math.sin(self.angle+(7*math.pi)/9)]
        point3 = [self.size*math.cos(self.angle-(7*math.pi)/9), self.size*math.sin(self.angle-(7*math.pi)/9)]

        #Translate points to the screen
        point1[0] += self.x
        point1[1] += self.y
        point2[0] += self.x
        point2[1] += self.y
        point3[0] += self.x
        point3[1] += self.y

        return (point1, point2, point3)

    def update(self):
        points = self.getRotationPoints()
        
        #Draw the points on the screen
        pygame.draw.aalines(self.surface, (self.red, self.green, self.blue), True, (points))        


        
