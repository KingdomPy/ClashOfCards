#cOnline gui classes
import pygame

def getPath():
        path = __file__
        path = path.split('\\')
        #Go to root folder
        path.pop()
        path.pop()
        path = '\\'.join(path)
        return path

class textBox:

    def __init__(self, defaultText, colour, font, position, dimensions):
        self.x = position[0]
        self.y = position[1]
        self.dimensions = dimensions
        self.colour = colour
        self.font = font
        self.defaultText = defaultText
        self.text = ""
        self.circle = pygame.image.load(getPath()+r"\assets\background\circle.png")
        self.circle = pygame.transform.scale(self.circle, (dimensions[1]*4,dimensions[1]*4))

    def update(self, keypress):
        if len(keypress) == 1:
            if len(self.text) < 16:
                self.text += keypress
        else:
            if keypress == "backspace":
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            elif keypress == "space":
                self.text += " "

    def render(self, surface):
        #Draw frame
        rectx = self.x - self.dimensions[0]/2
        recty = self.y - self.dimensions[1]/2
        surface.blit(self.circle, (rectx-self.dimensions[1]*2+12, recty-self.dimensions[1]*4/3-3))
        box = pygame.draw.rect(surface, (255,255,255), (rectx+3, recty+3, self.dimensions[0]-3, self.dimensions[1]-3))
        pygame.draw.rect(surface, self.colour, (rectx, recty, self.dimensions[0], self.dimensions[1]), 4)
        if self.text != "":
            display = self.font.render(self.text, True, (0,0,0))
        else:
           display = self.font.render(self.defaultText, True, (0,0,0))
        textBox = display.get_rect()
        textBox.topleft = box.topleft
        surface.blit(display, textBox)

class roomEntry:
        
    def __init__(self, surface, room, y, scrolly = 0):

        y += scrolly
        
        #Only render if within dimenions
        if y >= 100 and y < 560:
                
                #Set clip boundary
                surface.set_clip((70,184,660,376))
                    
                #Parse room
                ID = str(room["ID"])
                HOST = room["HOST"]
                MAPS = room["MAP"]
                PLAYERS = str(len(room["PLAYERS"]))

                font = pygame.font.Font(getPath()+r"\assets\fonts\OpenSans-Regular.ttf", 12)

                idText = font.render(ID, True, (220,220,220))
                hostText = font.render(HOST, True, (220,220,220))
                mapText = font.render(MAPS, True, (220,220,220))
                playersText = font.render(PLAYERS+"/4", True, (220,220,220))
                self.y = y
                
                #boxes = [(70,100,220,80), (290,100,220,80), (510,100,220,80)]

                #field box
                tRect = pygame.Surface((660,49), pygame.SRCALPHA)
                tRect.fill((0,0,0,50))

                box1 = idText.get_rect()
                box1.center = pygame.Rect(10,y,220,50).center
                
                box2 = hostText.get_rect()
                box2.center = pygame.Rect(175,y,220,50).center
                
                box3 = mapText.get_rect()
                box3.center = pygame.Rect(340,y,220,50).center
                
                box4 = playersText.get_rect()
                box4.center = pygame.Rect(505,y,220,50).center

                #Order of record blit
                surface.blit(tRect, (70,y+1))
                surface.blit(idText, box1)
                surface.blit(hostText, box2)
                surface.blit(mapText, box3)
                surface.blit(playersText, box4)
                
                pygame.draw.line(surface, (220,220,220), (70,y+50), (730,y+50), 1)

                surface.set_clip()
        
        
            
