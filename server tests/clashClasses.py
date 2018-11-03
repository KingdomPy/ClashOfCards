import math
import pygame.draw

class player:

    def __init__(self, surface):
        self.surface = surface
        self.scale = 30
    
    def render(self, position, angle, colours):
        x,y = position
        point1 = [self.scale*math.cos(angle) + x, self.scale*math.sin(angle) + y]
        point2 = [self.scale*math.cos(angle+(7*math.pi)/9) + x, self.scale*math.sin(angle+(7*math.pi)/9) + y]
        point3 = [self.scale*math.cos(angle-(7*math.pi)/9) + x, self.scale*math.sin(angle-(7*math.pi)/9) + y]

        points = (point1, point2, point3)

        pygame.draw.aalines(self.surface, colours, True, (points)) 

class server_player:

    def __init__(self, x, y, angle, name, colours):
        self.name = name
        self.x = x
        self.y = y
        self.velocity = 10
        self.angle = angle
        self.colours = colours

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 2*math.pi

    def moveForward(self):
        self.x += self.velocity * math.cos(self.angle)
        self.y += self.velocity * math.sin(self.angle)

    def getData(self):
        return [[self.x, self.y], self.angle, self.colours]
