import pygame
import math

#Menu objects
class menuWidget:

    def __init__ (self, red, green, blue, x, y, width, length):
        self.red = red
        self.green = green
        self.blue = blue
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.selected = False

    def teleport(self, x, y):
        pass

    def setColours(self, colours):
        self.red, self.green, self.blue = colours
        
    def getColours(self):
        return (self.red, self.green, self.blue)

    def getDimensions(self):
        return (self.x, self.y, self.width, self.length)

    def collision(self, mouseX, mouseY):
        if (mouseX >= self.x and mouseX <= self.x + self.width) and (mouseY >= self.y and mouseY <= self.y + self.length):
            self.selected = True
        else:
            self.selected = False

class mainButton(menuWidget):
    
    def __init__(self, red, green, blue, x, y, width, length, text, colours, font):
        super().__init__(red, green, blue, x, y, width, length)
        self.originalColours = (red, green, blue)
        self.font = font
        #bText is back up text
        self.bText = text
        self.textColours = colours
        self.text = self.font.render(text, True, colours)

    def collision(self, mouseX, mouseY):
        if (mouseX >= self.x and mouseX <= self.x + self.width) and (mouseY >= self.y and mouseY <= self.y + self.length):
            self.selected = True
            self.red = 2
            self.green = 180
            self.blue = 245
            self.text = self.font.render(self.bText, True, (255, 255, 255))
        else:
            self.selected = False
            self.red, self.green, self.blue = self.originalColours
            self.text = self.font.render(self.bText, True, self.textColours)

    def update(self, surface):
        widget = pygame.draw.rect(surface, (self.red, self.green, self.blue), (self.x, self.y, self.width, self.length))
        if self.selected:
            pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), (self.x, self.y+self.length), 6)
            pygame.draw.line(surface, (255, 255, 255), (self.x+self.width, self.y), (self.x+self.width, self.y+self.length), 6)
        textHolder = self.text.get_rect()
        textHolder.center = widget.center
        surface.blit(self.text, textHolder)

class settingsButton(mainButton):
    pass

class slider(menuWidget):

    def __init__(self, red, green, blue, x, y, width, length):
        super().__init__(red, green, blue, x, y, width, length)
        self.barX = x

    def setBar(self, mouseX):
        self.barX = mouseX

    def initColours(self, colour):
        self.barX = math.ceil(self.x + (colour/255)*self.width)
            
    def update(self, surface, colour):

        #Set colour to position
        if colour == "red":
            self.red = math.ceil(255*((self.barX - self.x) / self.width))
        elif colour == "green":
            self.green = math.ceil(255 * ((self.barX - self.x) / self.width))
        elif colour == "blue":
            self.blue = math.ceil(255 * ((self.barX - self.x) / self.width))

        
        #Draw slider rectangle frame
        pygame.draw.rect(surface, (self.red, self.green ,self.blue), (self.x, self.y, self.width, self.length))
        
        #Draw Bar
        pygame.draw.rect(surface, (255, 255, 255), (self.barX-2, self.y-2, 4, self.length+4))
        
        #Draw curved tops
        pygame.draw.circle(surface, (255, 255, 255), (self.barX, self.y), 4, 4)
        pygame.draw.circle(surface, (255, 255, 255), (self.barX, self.y + self.length), 4, 4)

        #Return new colour
        if colour == "red":
            return self.red
        elif colour == "green":
            return self.green
        elif colour == "blue":
            return self.blue

#Player objects
class player:

    def __init__ (self, surface, red=255, green=255, blue=255):
        self.surface = surface
        self.x = 400
        self.y = 300
        self.velocity = 7
        self.turnSpeed = self.velocity/50
        self.size = 30
        self.angle = 0
        self.red = red
        self.green = green
        self.blue = blue
        self.originalColours = (red, green, blue)

    def setStats(self, level, exp, maxHp ,hp, maxMp, mana):
        #Load attributes
        self.level = level
        self.exp = exp
        self.maxHp = maxHp
        self.hp = hp
        self.maxMp = maxMp
        self.mana = float(mana)

    def setCommands(self, commandData):
        self.commandData = commandData
        self.velocity = commandData["Speed"]
        self.turnSpeed = self.velocity/50
        self.damage = float(commandData["Str"])

        # Load abilitity cooldowns
        self.cooldowns = {}
        self.primaryCost = 0

        #Set attack mode
        if commandData["Attack"] == "Surge":
            self.cooldowns["bAtk"] = 693

        elif commandData["Attack"] == "Shotgun":
            self.cooldowns["bAtk"] = 594

        #Set back command
        if commandData["Back"] == "Dodge":
            self.cooldowns["bCom"] = 990

        #Set primary command
        if commandData["Primary"] == "Aura":
            self.cooldowns["pCom"] = 7920 #240 frames
            self.primaryCost = 8

        self.basicAttack = self.cooldowns["bAtk"]
        self.backCommand = self.cooldowns["bCom"]
        self.primaryCommand = self.cooldowns["pCom"]

        "hit animation"
        self.hit = 198

    def cycleCooldowns(self):
        #Abilities
        if self.basicAttack != self.cooldowns["bAtk"]:
            self.basicAttack += 33

        if self.backCommand != self.cooldowns["bCom"]:
            self.backCommand += 33
            if self.dash != 5:
                self.dash += 1
                self.moveForward()

        if self.primaryCommand != self.cooldowns["pCom"]:
            self.primaryCommand += 33

        #Animations
        if self.mana < 1:
            if self.mana != -1*self.maxMp:
                self.mana -= self.maxMp/300
                if self.mana <= -1*self.maxMp:
                    self.mana = self.maxMp

        if self.hit != 198:
            self.hit +=33
            if self.hit == 198:
                self.red, self.green, self.blue = self.originalColours
        
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

    def moveForward(self):
        self.x += self.velocity * math.cos(self.angle)
        self.y += self.velocity * math.sin(self.angle)

    def rotate(self, angle):
        self.angle += angle

    def shootBullet(self):
        if self.basicAttack == self.cooldowns["bAtk"]:
            self.basicAttack = 0
            position = (self.size*math.cos(self.angle) + self.x, self.size*math.sin(self.angle) + self.y)
            if self.commandData["Attack"] == "Surge":
                damage = self.damage*0.8
                speed = 14
            elif self.commandData["Attack"] == "Shotgun":
                damage = self.damage*0.3
                speed = 9
            return(self.commandData["Attack"], speed, position, self.angle, self.originalColours, damage)
        else:
            return 0

    def commandBack(self):
        if self.backCommand == self.cooldowns["bCom"]:
            self.backCommand = 0
            if self.commandData["Back"] == "Dodge":
                self.dash = 0

    def commandPrimary(self):
        if self.mana > 0:
            if self.primaryCommand == self.cooldowns["pCom"]:
                self.primaryCommand = 0
                if self.commandData["Primary"] == "Aura":
                    self.mana -= self.primaryCost
                    if self.mana < 0:
                        self.mana = 0
                    position = (self.x, self.y)
                    distance = 45
                    damage = self.damage*0.15
                    return(self.commandData["Primary"], distance, position, self.angle, self.originalColours, damage)

            #Ability is on cooldown
            else:
                return 0
        #Not enough energy
        else:
            return 0

    def collision(self, bulletX, bulletY, damage, variance):
        corners = self.getRotationPoints()
        for i in range(0, 3):
            l1 = corners[i]
            l2 = corners[(i + 1) % 3]
            x = bulletX
            y = bulletY
            x_diff = l2[0] - l1[0]
            y_diff = l2[1] - l1[1]
            numerator = abs(y_diff * x - x_diff * y + l2[0] * l1[1] - l2[1] * l1[0])
            denom = math.sqrt(y_diff ** 2 + x_diff ** 2)
            distance = numerator / denom

            # Fix for horizontal and vertical
            if y_diff == 0:
                if (x > max(l2[0], l1[0]) or x < min(l2[0], l1[0])) and y == l2[1]:
                    distance = min(abs(x - l2[0]), abs(x - l1[0]))

            elif x_diff == 0:
                if (y > max(l2[1], l1[1]) or y < min(l2[1], l1[1])) and x == l2[0]:
                    distance = min(abs(y - l2[1]), abs(y - l1[1]))

            # Fix for infinite line length
            # check the boundaries
            x_failed = (x > max(l2[0], l1[0]) or x < min(l2[0], l1[0]))
            y_failed = (y > max(l2[1], l1[1]) or y < min(l2[1], l1[1]))
            if x_failed or y_failed:
                # Sets the distance as too far
                distance = variance + 1

            if variance >= distance:
                hit = True
                self.hit = 0
                self.hp -= damage
                return True

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

        if self.hit != 198:
            self.red, self.green, self.blue = 255, 255, 255

        if self.x < -10 or self.x > 810 or self.y < -10 or self.y > 610:
            if self.x < -10 or self.x > 810:
                self.x = abs(810 - abs(self.x))
            else:
                self.y = abs(610 - abs(self.y))
        
        #Draw the points on the screen
        pygame.draw.aalines(self.surface, (self.red, self.green, self.blue), True, (points))        

        #Calculate cooldowns
        self.cycleCooldowns()
        

class projectile:

    def __init__ (self, surface, speed, position, angle, colour, damage, target):
        self.surface = surface
        self.x, self.y = position
        self.angle = angle
        self.colour = colour
        self.velocity = speed
        self.damage = damage
        self.target = target
        self.delete = False

    def getPosition(self):
        return self.x, self.y

    def move(self):
        self.x += self.velocity * math.cos(self.angle)
        self.y += self.velocity * math.sin(self.angle)

    def hit(self):
        #Hit code / animations
        self.delete = True
    
    def update(self):
        #Destroy projectile if out of bounds
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
            self.delete = True

        else:
            pygame.draw.rect(self.surface, (self.colour), (self.x-5, self.y-5, 5, 5))

class aura(projectile):
    def __init__ (self, surface, distance, position, angle, colour, damage, target, player):
        super().__init__(surface, distance, position, angle, colour, damage, target)
        self.player = player #player the aura orbits
        self.timer = 0

    def move(self):
        self.x = self.player.x
        self.y = self.player.y
        self.angle += 0.15
        #self.velocity is the distance
        self.x += self.velocity * math.cos(self.angle)
        self.y += self.velocity * math.sin(self.angle)
        if self.timer != 2970: #90 frames
            self.timer += 33
            if self.timer == 2970:
                self.delete = True

    def update(self):
        pygame.draw.rect(self.surface, (self.colour), (self.x - 5, self.y - 5, 5, 5))

class statsBar:

    def __init__(self, surface, maxHp, maxMp, width, length ,direction):
        self.surface = surface
        self.maxHp = maxHp
        self.maxMp = maxMp
        self.width = width
        self.length = length
        self.direction = direction

    def update(self, hp, mp):
        if hp > 0:
            scale = hp / self.maxHp
            if self.direction == 0:
                pygame.draw.rect(self.surface, (41, 43, 41),  (0, 0, self.width+15, self.length+10))
                pygame.draw.rect(self.surface, (63, 237, 47), (5, 5, 5+scale*self.width, self.length))

            elif self.direction == 1:
                pygame.draw.rect(self.surface, (41, 43, 41),  (800, 0, -1*(self.width+15), self.length+10))
                pygame.draw.rect(self.surface, (63, 237, 47), (795, 5 , -1*(5+scale*self.width), self.length))

        scale = mp / self.maxMp
        if mp > 0:
            if self.direction == 0:
                pygame.draw.rect(self.surface, (41, 43, 41), (0, self.length+10, self.width*(2/3)+15, (3/5)*self.length+5))
                pygame.draw.rect(self.surface, (66, 134, 244), (5, self.length+12, 5+scale*self.width*(2/3), self.length*(3/5)))

            elif self.direction == 1:
                pygame.draw.rect(self.surface, (41, 43, 41), (800, self.length+10, -1*(self.width*(2/3)+15), (3/5)*self.length+5))
                pygame.draw.rect(self.surface, (66, 134, 244), (795, self.length+12, -1*(5+scale*self.width*(2/3)), self.length*(3/5)))

        else:
            scale *= -1
            if self.direction == 0:
                pass
                pygame.draw.rect(self.surface, (41, 43, 41), (0, self.length+10, self.width*(2/3)+15, (3/5)*self.length+5))
                pygame.draw.rect(self.surface, (242, 87, 162), (5, self.length+12, 5+scale*self.width*(2/3), self.length*(3/5)))

            elif self.direction == 1:
                pass
                pygame.draw.rect(self.surface, (41, 43, 41), (800, self.length+10, -1*(self.width*(2/3)+15), (3/5)*self.length+5))
                pygame.draw.rect(self.surface, (242, 87, 162), (795, self.length+12, -1*(5+scale*self.width*(2/3)), self.length*(3/5)))

