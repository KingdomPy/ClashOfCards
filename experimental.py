import pygame, math, json
from lib import cursor, interface, gameEngine
#Experimental
from lib import onlineClient

def loadConfig():
    try:
        config = open('config.txt').readlines()
        config = [x.strip() for x in config]
        dicte = "{"
        for i in range(len(config)):
            dicte += config[i]+','
        dicte = dicte[:-1]
        dicte += "}"
        config = json.loads(dicte)
        return config
    except:
        return 0 #loading error

class application:

    def __init__(self, debug=False):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Esl Pi: Kingdom Cards Test Build")
        icon = pygame.image.load(self.getPath()+r"\assets\title screen\icon.png")
        pygame.display.set_icon(icon)
        self.debug = debug
        self.controls = {"up":pygame.K_w, "left":pygame.K_a, "right":pygame.K_d, "down":pygame.K_s, "A":pygame.K_j, "B":pygame.K_k, "next":pygame.K_i, "previous":pygame.K_o, "pause":pygame.K_p}

        #Animated background test
        path = self.getPath()
        logo = pygame.image.load(path+r"\assets\title screen\logo.png").convert()
        font = pygame.font.Font(path+r"\assets\fonts\Kh2_Menu_Font.ttf", 24)
        self.bgAnimation = []
        imgPath = path+r"\assets\background\frame_"
        fileEnd = "_delay-0.03s.jpg"
        for i in range(164):
            self.surface.fill((0,0,0))
            file = str(i)
            #convert i to 3 digit string
            for j in range(3-len(file)):
                file = "0"+file
            image = pygame.image.load(imgPath+file+fileEnd).convert()
            self.bgAnimation.append(image)
            text = font.render(str(round(i*100/164, 1))+"%", True, (240,240,240))
            entry = text.get_rect()
            entry.bottomright= pygame.Rect(0,0,800,600).bottomright
            self.surface.blit(text, entry)
            self.surface.blit(logo, (200,75))
            pygame.display.update()

        #Loading finished animation
        self.surface.fill((0,0,0))
        text = font.render("100%", True, (240,240,240))
        entry = text.get_rect()
        entry.bottomright= pygame.Rect(0,0,800,600).bottomright
        self.surface.blit(text, entry)
        'self.surface.blit(logo, (200,75))'
        pygame.display.update()
        pygame.time.delay(16)
        self.mainMenu()

    def transition(self):
        tRect = pygame.Surface((800,600), pygame.SRCALPHA)
        for i in range(75):
            tRect.fill((0,0,0,i+1))
            self.surface.blit(tRect, (0,0))
            pygame.display.update()
            pygame.time.delay(16)

    def displayInfo(self, text, colour=(9,24,102), location=0):
        #location = 0 default, 1 top right
        if location == 0:
            locationRect = (100, 500, 600, 100)
            fontSize = 18
            
        elif location == 1:
            locationRect = (300, 10, 480, 75)
            fontSize = 13
            
        font = pygame.font.Font(self.fontPath, fontSize)
        tTextRect = pygame.Surface((locationRect[2], locationRect[3]), pygame.SRCALPHA)
        tTextRect.fill((0,0,240,70))
        self.surface.blit(tTextRect, (locationRect[0],locationRect[1]))
        renderText = [font.render(text, True, colour)]

        #Splice text
        splice = ""
        #While the last spliced text width is too large keep looping and adding spliced text
        while renderText[len(renderText)-1].get_rect()[2] >= locationRect[2]-40:
            i = len(renderText)-1 # current text, using i allows me to reset the splice
            while renderText[i].get_rect()[2] >= locationRect[2]-40 or splice[0] == " ": #splice[0stops words from being seperated
                splice += text[-1:]
                text = text[:-1]
                renderText[i] = font.render(text, True, (9,24,102))
            text = splice[::-1] #flip splice
            renderText.append(font.render(text, True, (9,24,102)))        
            splice = "" 
        if renderText[ len(renderText)-1 ] == "":
            renderText.pop()

        textEntry = [i.get_rect() for i in renderText]

        for i in range(len(textEntry)):
            textEntry[i].topleft = (pygame.Rect(locationRect[0]+fontSize, locationRect[1]+fontSize+i*fontSize, locationRect[2]-fontSize*2, locationRect[3])).topleft

        for i in range(len(renderText)):
            self.surface.blit(renderText[i], textEntry[i])
            
        pygame.draw.rect(self.surface, (46,102,193), locationRect, 7)
        
    def mainMenu(self, cursorRow=-1):
        DPAD = cursor.cursor()
        DPAD.setTrack((["ADVENTURE", "VERSUS", "SETTINGS"],[" "]))
        #Transparent rectangle
        tRect = pygame.Surface((190, 280), pygame.SRCALPHA)
        tRect.fill((0,0,0,40))
        #Font
        self.fontPath = self.getPath()+r"\assets\fonts\Kh2_Menu_Font.ttf"
        font = pygame.font.Font(self.fontPath, 18)
        text = "Please move the DPAD to select a mode."
        #Selected mode
        DPAD.setCursor(cursorRow, 0)
        location = DPAD.getCursor()

        #Animated background test
        self.cycle = 0
        miniMenu = 24
        
        while True:
            self.surface.fill((255,255,255))
            pygame.time.delay(16)

            #Animated background test
            self.surface.blit(self.bgAnimation[self.cycle], (0,0))
            self.cycle += 1
            self.cycle %= 164

            if miniMenu != 24:
                miniMenu += 1
                
            #Get inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == self.controls["A"]:
                         if mode == "ADVENTURE":
                             self.transition()
                             self.adventureMode(self.debug)

                         elif mode == "VERSUS":
                             self.transition()
                             self.versusMode(self.debug)
                            
                         elif mode == "SETTINGS":
                             self.transition()
                            
                             
                    if event.key == self.controls["right"]:
                        DPAD.moveRight()

                    if event.key == self.controls["left"]:
                         DPAD.moveLeft()
                    
                    location = DPAD.getCursor()
                    cursorRow = location[0]
                    mode = location[2]
                    
            #Draw screen
            for i in range(3):
                if i != cursorRow:
                    self.surface.blit(tRect, (60+240*i,90))
                        
                else:
                    text = str(location[2])
                    pygame.draw.rect(self.surface, (0,0,0), (60+240*i, 90, 190, 280))
                    pygame.draw.rect(self.surface, (107,182,239), (60+240*i, 90, 190, 280), 10)
                    #DPAD
                    pygame.draw.rect(self.surface, (0,0,0), (130+240*i, 390, 50, 50))
                    pygame.draw.rect(self.surface, (46,102,193), (135+240*i, 395, 40, 40))
                    pygame.draw.rect(self.surface, (107,182,239), (142.5+240*i, 402.5, 27.5, 27.5))

            #Text box
            self.displayInfo(text)
            
            pygame.display.update()

    def adventureMode(self, debug=False):
        engine = gameEngine.engine(self.surface, (800,600), self.controls, debug)
        hud = interface.display(self.surface, (800,600), debug)

        #Entity parameters = tag, stats, position, size
        
        engine.addEntity("player", {"colour":(0,50,0), "commands":["Surge","Aura","Shield","Repair"]}, (0,0,math.pi/2))
        engine.addEntity("location", {"name":"Twilight Zone", "colour":(0,0,0)}, (0,0,0), 300)
        engine.addEntity("location", {"name":"Olympic City", "colour":(200,150,80)}, (0,-3000,0), 250)
        
        engine.addEntity("square", {"colour":(10,30,80)}, (0, -800, 0))
        engine.addEntity("square", {"colour":(20,30,80)}, (0, -600, math.pi))
        engine.addEntity("square", {"colour":(30,30,80)}, (0, -400, 0))
        engine.addEntity("square", {"colour":(40,30,80)}, (0, -200, math.pi))
        engine.addEntity("square", {"name":"Dummy-1","colour":(50,30,80)}, (0, 0, 0))
        engine.addEntity("square", {"colour":(60,30,80)}, (0, 200, math.pi))
        engine.addEntity("square", {"colour":(70,30,80)}, (0, 400, 0))
        engine.addEntity("square", {"colour":(80,30,80)}, (0, 600, math.pi))
        engine.addEntity("square", {"colour":(90,30,80)}, (0, 800, 0))
           
        engine.addEntity("triangle", {"name":"Dummy-2","colour":(100,30,80)}, (300,-300,math.pi/4)) 
        engine.addEntity("triangle", {"colour":(110,30,80)}, (-300,-300,3*math.pi/4))
        engine.addEntity("triangle", {"colour":(120,30,80)}, (-300,300,5*math.pi/4))
        engine.addEntity("triangle", {"colour":(130,30,80)}, (300,300,7*math.pi/4))
        
        while True:
            arguments = engine.update()
            if arguments == 0: #Exit adventure mode
                self.transition()
                break
            hud.update(arguments[0], [], arguments[1], arguments[2])
            pygame.time.delay(16)

    def versusMode(self, debug=False):
        onlineSession = onlineClient.multiplayerMenu(self.surface, (SERVER_IP, SERVER_PORT), self.controls, debug)

        if onlineSession.getStatus() == True:
            while True:
                self.surface.blit(self.bgAnimation[self.cycle], (0,0))
                pygame.draw.rect(self.surface, (80,100,140), (70,100,660,460))
                self.cycle += 1
                self.cycle %= 164
                arguments = onlineSession.update()
                self.displayInfo("Join up to 3 players in battle.", (220,220,220),1)
                pygame.display.update()
                if arguments == 0:
                    onlineSession.close()
                    self.transition()
                    break
                pygame.time.delay(16)
    
    def getPath(self):
        path = __file__
        #Remove the file name
        path = path.split('\\')
        path.pop()
        path = '\\'.join(path)
        return path

#Set constants
config = loadConfig()
SERVER_IP = config["SERVER_IP"]
SERVER_PORT = config["SERVER_PORT"]

game = application(False)
    
