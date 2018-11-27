import pygame, pygame.gfxdraw, math

def getPath():
    path = __file__
    path = path.split('\\')
    #Go to root folder
    path.pop()
    path.pop()
    path = '\\'.join(path)
    return path

class display:
    def __init__(self, surface, dimensions, debug=False):
        self.debug = debug
        self.surface = surface
        self.width = dimensions[0]
        self.length = dimensions[1]
        path = getPath()
        frame = path+"/assets/player/command_menu/frame.png"
        frame_selected = path+"/assets/player/command_menu/frame_selected.png"
        frame_shoot = path+"/assets/player/command_menu/frame_shoot.png"
        self.frame = pygame.image.load(frame)
        self.frame_selected = pygame.image.load(frame_selected)
        self.frame_shoot = pygame.image.load(frame_shoot)
        if self.debug == True:
            self.colour = (0,0,0)
        else:
            self.colour = (0,0,0)

    def renderCMenu(self, commands=[], cooldowns=[], selected=1):
        x = 30
        y = self.length - 180
        #Load sprites
        for i in range (0, 4):
            if i != selected:
                self.surface.blit(self.frame, (x, y+36*i))
        if selected == 0:
            image = self.frame_shoot
        else:
            image = self.frame_selected
        self.surface.blit(image, (x+12, y+36*selected))
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        #Load text
        for i in range(len(commands)):
            if i != selected:
                text = font.render(commands[i], True, (255,255,255))
                sprite = pygame.Rect(x+25, y+36*i+13, 119, 29)
                location = text.get_rect()
                location.topleft = sprite.topleft
                self.surface.blit(text, location)
            else:
                text = font.render(commands[i], True, (255,255,255))
                sprite = pygame.Rect(x+37, y+36*i+13, 119, 29)
                location = text.get_rect()
                location.topleft = sprite.topleft
                self.surface.blit(text, location)
                
    def renderHud(self, miniMapData):
        #Mana bar
        points = [(self.width-220,self.length-43), (self.width-200,self.length-83), (self.width-20,self.length-83), (self.width-20,self.length-73), (self.width-190,self.length-73)]
        pygame.draw.polygon(self.surface, (66,167,244), points)
        if self.debug == True:
            pygame.draw.lines(self.surface,  self.colour, True, points, 2)
                             
        #Health bar
        points = [(self.width-190,self.length-68), (self.width-20,self.length-68), (self.width-20,self.length-38), (self.width-220,self.length-38)]
        pygame.draw.polygon(self.surface, (63,237,47), points)
        pygame.draw.lines(self.surface,  self.colour, True, points, 2)

        #Minimap Rect
        #miniMapRect = (30,260,144,144)
        miniMapRect = (self.width-174,30,144,144)
        borderWidth = 3
        clipRect = (miniMapRect[0]+borderWidth, miniMapRect[1]+borderWidth, miniMapRect[2]-borderWidth*2, miniMapRect[3]-borderWidth*2)
        xConstant = (miniMapRect[0]*2 + miniMapRect[2])/2
        yConstant = (miniMapRect[1]*2 + miniMapRect[3])/2
        #Mini Map
        pygame.draw.rect(self.surface,  self.colour, miniMapRect, borderWidth)
        self.surface.set_clip(clipRect)
        #Dimensions of the map
        mapScale = 72/1500
        #Size of icons on the map
        sizeScale = 72/600
        enemies = ("triangle", "square")
        allies = ("ally", "location")
        for i in range(len(miniMapData)):
            size = miniMapData[i][2]*sizeScale
            x = (-1*miniMapData[i][1][0]) * mapScale + xConstant - size/2
            y = (-1*miniMapData[i][1][1]) * mapScale + yConstant - size/2
            if miniMapData[i][0] in enemies:
                colour = (250,50,50)
                pygame.draw.rect(self.surface, colour, (x, y, size, size))
                
            elif miniMapData[i][0] in allies:
                colour = miniMapData[i][3]
                pygame.draw.rect(self.surface, colour, (x, y, size, size), 2)
                #Draw zone range
                if miniMapData[i][0] == "location":
                    x += size/2
                    y += size/2
                    radius = round(miniMapData[i][2] * 5 * mapScale)
                    pygame.gfxdraw.aacircle(self.surface, round(x), round(y), radius-1, colour)
                    pygame.gfxdraw.aacircle(self.surface, round(x), round(y), radius, colour)

        #The player
        pygame.draw.rect(self.surface,  self.colour, (xConstant-2.5, yConstant-2.5, 5,5))
        self.surface.set_clip()
        

    def update(self, commands=[], cooldowns=[], selected=1, miniMapData=[]):
        self.renderCMenu(commands, cooldowns, selected)
        self.renderHud(miniMapData)
        pygame.display.update()
        

    
