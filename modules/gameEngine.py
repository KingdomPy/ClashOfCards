import pygame
import math
from modules import objects

def getPath():
    path = __file__
    path = path.split('\\')
    #Go to root folder
    path.pop()
    path.pop()
    path = '\\'.join(path)
    return path

class engine:
    def __init__(self, surface, dimensions, debug=False):
        self.debug = debug
        self.surface = surface
        self.width = dimensions[0]
        self.length = dimensions[1]
        self.player = ""
        self.entities = []
        self.projectiles = []
        self.instance = "map"
        self.controls = {"up":pygame.K_w, "left":pygame.K_a, "right":pygame.K_d, "down":pygame.K_s, "A":pygame.K_j, "next":pygame.K_i, "previous":pygame.K_o, "pause":pygame.K_p}
        self.selectedMove = 0
        self.camera = camera(self.surface, dimensions, debug)
        
    def setControls(self, controls):
        self.controls = controls
        
    def addEntity(self, tag, stats={}, position=(0,0,0), size=30):
        if tag == "player":
            entity = objects.player(tag, stats, position, size)
            self.player = entity
        elif tag == "triangle":
            entity = objects.triangle(tag, stats, position, size)
        elif tag == "square":
            entity = objects.square(tag, stats, position, size)
        elif tag == "location":
            entity = objects.location(tag, stats, position, size)
        self.entities.append(entity)
        

    def update(self):
        returnToMenu = False
        #Get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if self.instance == "map":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        returnToMenu = True
                    
                    if event.key == self.controls["next"]:
                        self.selectedMove = (self.selectedMove-1)%4

                    if event.key == self.controls["previous"]:
                        self.selectedMove = (self.selectedMove+1)%4

                    if event.key == self.controls["A"]:
                        if self.selectedMove == 0:
                            angle = self.player.angle + 0.12
                            for i in range(3):
                                bullet = objects.bullet("shotgun", {}, (self.player.x,self.player.y,angle-i*0.12))
                                self.projectiles.append(bullet)
                        
        if not returnToMenu:
            if self.player != "":
                keys = pygame.key.get_pressed()

                if keys[self.controls["up"]]:
                    self.player.moveForward()

                if keys[self.controls["left"]]:
                    self.player.rotate(-1)

                if keys[self.controls["right"]]:
                    self.player.rotate(1)

            #Call object clock cycles and capture data
            cameraData = []
            i = 0
            #coordinates, name
            nearest_location = [-1, ""]
            while i < len(self.entities):
                #Collision checker script
                if not(self.entities[i].tag == "player"):
                    j = 0
                    while j < len(self.projectiles):
                        x,y = self.projectiles[j].x,self.projectiles[j].y
                        distance = math.sqrt((y-self.entities[i].y)**2+(x-self.entities[i].x)**2)
                        #Will check if bullet is in the entity's sphere
                        if distance <= self.entities[i].size:
                            bullet = ((x,y),self.projectiles[j].size)
                            hasBeenHit = self.entities[i].collision(bullet[0],bullet[1])
                            if not(hasBeenHit):
                                j += 1
                            else:
                                self.projectiles[j].hasHit()
                                self.projectiles.pop(j)
                        else:
                            j += 1
                update = self.entities[i].update(((self.player.x,self.player.y),))
                #0 = signal to delete the object
                if update != 0:
                    if update != None:
                        #check for nearby locations
                        if nearest_location[0] == -1:
                            nearest_location = update
                        elif nearest_location[0] > update[0]:
                            nearest_location = update
                    cameraData.append((self.entities[i].tag,self.entities[i].renderData(),self.entities[i].size))
                    i += 1
                else:
                    self.entities.pop(i)
                    
            #Add projectiles to camera data
            i = 0
            while i < len(self.projectiles):
                update = self.projectiles[i].update(((self.player.x,self.player.y),))
                #0 = signal to delete the object
                if update != 0:
                    cameraData.append((self.projectiles[i].tag,self.projectiles[i].renderData(),self.projectiles[i].size))
                    i += 1
                else:
                    self.projectiles.pop(i)
        
            #Add location name to camera data
            cameraData.append(nearest_location)
            #Pass data to camera
            miniMapData = self.camera.render(cameraData)
            #Pass hud data to hud
            arguments = (self.selectedMove, miniMapData)
            return arguments
        else:
            return 0
            
class camera:
    def __init__(self, surface,dimensions, debug):
        self.debug = debug
        self.surface = surface
        self.width = dimensions[0]
        self.length = dimensions[1]
        self.x = 0
        self.y = 0
        if self.debug == True:
            self.colour = (0,0,0)
        else:
            self.colour = (0,0,0)
        path = getPath()+"/assets/fonts/Kingdom_Hearts_Font.ttf"
        self.locationFont = pygame.font.Font(path, 50)

    def distance(self, point1, point2):
        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]
        return x2-x1, y2-y1
        

    def render(self, data):
        font = pygame.font.Font(pygame.font.get_default_font(), 10)
        if self.debug == True:
            self.surface.fill((255,255,255))
        else:
            self.surface.fill((255,255,255))
        boundary = [self.width/2, self.length/2]
        centerx = (self.width)/2
        centery = (self.length)/2
        playerx = centerx
        playery = centery
        player = ([0,0],[0,0])
        miniMapData = []
        #Find the player
        for i in range(len(data)-1):
            if data[i][0] == "player":
                self.x, self.y = data[i][1][0]
                player = data[i][1][1]
                playerColour = data[i][1][2]
                data.pop(i)
                playerx = centerx - self.x
                playery = centery - self.y
                break
        #See if monsters are close enough to be rendered
        #data format:
        "i = monster"
        "[i][0] = tag"
        "[i][1][0] = coordinates"
        "[i][1][1] = points to draw"
        "[i][1][2] = colour"
        "[i][2] = size"
        for i in range(len(data)-1):
            distance = self.distance(data[i][1][0], (self.x,self.y))
            colour = data[i][1][2]
            if abs(distance[0]) <= boundary[0]+data[i][2] and abs(distance[1]) <= boundary[1]+data[i][2]:
                for j in range(len(data[i][1][1])):
                    data[i][1][1][j][0] += playerx
                    data[i][1][1][j][1] += playery
                entity = data[i][1][1]
                if self.debug == True:
                    x = round(data[i][1][0][0])
                    y = round(data[i][1][0][1])
                    position = font.render(str((x,y)), True, self.colour)
                    location = position.get_rect()
                    location.center = (data[i][1][0][0]+playerx, data[i][1][0][1]+playery)
                    self.surface.blit(position, location)
                pygame.draw.aalines(self.surface, colour, True, entity)
            #Get minimap data
            "tag, (minimapX, minimapY), size, colour"
            if data[i][0] != "location":
                if abs(distance[0]) <= 1500 and abs(distance[1]) <= 1500:
                    #Tag, position, size
                    miniMapData.append((data[i][0],(distance[0], distance[1]), data[i][2], colour))
            else:
                #Allows location area to be radius
                if abs(distance[0]) <= 1500+data[i][2]*10 and abs(distance[1]) <= 1500+data[i][2]*5:
                    #Tag, position, size
                    miniMapData.append((data[i][0],(distance[0], distance[1]), data[i][2], colour))
        #Render player at the center
        for i in range(len(player)):
            player[i][0] += centerx
            player[i][1] += centery
        if self.debug == True:
            x = round(self.x)
            y = round(self.y)
            position = font.render(str((x,y)), True, self.colour)
            location = position.get_rect()
            location.center = (centerx, centery)
            self.surface.blit(position, location)
        pygame.draw.aalines(self.surface, playerColour, True, player)
        #Render nearest location
        end = len(data)-1
        text = data[end][1]
        if text != "":
            text = self.locationFont.render(text, True, data[end][2])
            location = text.get_rect()
            location.center = (400, 50)
            self.surface.blit(text, location)
        return miniMapData
