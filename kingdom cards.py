import pygame, math
from modules import cursor, interface, gameEngine

class application:

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Esl Pi: Kingdom Cards Test Build")
        icon = pygame.image.load(self.getPath()+r"\assets\icon.png")
        pygame.display.set_icon(icon)
        self.debug = False
        self.controls = {"up":pygame.K_w, "left":pygame.K_a, "right":pygame.K_d, "down":pygame.K_s, "A":pygame.K_j, "B":pygame.K_k, "next":pygame.K_i, "previous":pygame.K_o, "pause":pygame.K_p}

        #Animated background test
        path = self.getPath()
        logo = pygame.image.load(path+r"\assets\logo.png").convert()
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
        self.surface.blit(logo, (200,75))
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

    def miniMenu(self, size):
        #size should end at 24
        i = size
        width, length = (i+1)*26, (i+1)*18
        tRect = pygame.Surface((width,length), pygame.SRCALPHA)
        tRect.fill((0,0,0,110))
        x, y = 400-width/2, 260-length/2
        self.surface.blit(tRect, (x,y))

        pygame.draw.rect(self.surface, (0,0,40), (x, y, width, length), round(10*(i/24)))
        
        pygame.display.update()

    def mainMenu(self, cursorRow=-1):
        DPAD = cursor.cursor()
        DPAD.setTrack((["ADVENTURE", "VERSUS", "SETTINGS"],[" "]))
        #Transparent rectangle
        tRect = pygame.Surface((190, 280), pygame.SRCALPHA)
        tRect.fill((0,0,0,40))
        tTextRect = pygame.Surface((600, 100), pygame.SRCALPHA)
        tTextRect.fill((0,0,240,70))
        #Font
        fontPath = self.getPath()+r"\assets\fonts\Kh2_Menu_Font.ttf"
        font = pygame.font.Font(fontPath, 18)
        text = font.render("Please move the DPAD to select", True, (9,24,102))
        text2 = font.render("a mode.", True, (9,24,102))
        #Selected mode
        DPAD.setCursor(cursorRow, 0)
        location = DPAD.getCursor()

        #Animated background test
        cycle = 0
        miniMenu = 24

        #0 = selection, 1 = mini menu
        instance = 0
        
        while True:
            self.surface.fill((255,255,255))
            pygame.time.delay(16)

            #Animated background test
            self.surface.blit(self.bgAnimation[cycle], (0,0))
            cycle += 1
            cycle %= 164

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
                             return self.adventureMode(self.debug)
                            
                         elif mode == "SETTINGS":
                             instance = 1
                             miniMenu = 0
                             text = font.render("Configure your options here", True, (9,24,102))
                             DPAD.setCursor(-1, 0)
                             DPAD.setTrack((["DEBUG"],["MUSIC"],["SFX"]))

                    if event.key == self.controls["B"]:
                        if instance == 1:
                            instance = 0
                            DPAD.setTrack((["ADVENTURE", "VERSUS", "SETTINGS"],[" "]))
                            DPAD.setCursor(2, 0)
                             
                    if event.key == self.controls["right"]:
                        DPAD.moveRight()

                    if event.key == self.controls["left"]:
                         DPAD.moveLeft()

                    if instance != 0:
                        if event.key == self.controls["up"]:
                            DPAD.moveUp()

                        if event.key == self.controls["down"]:
                             DPAD.moveDown()
                    
                    location = DPAD.getCursor()
                    cursorRow = location[0]
                    mode = location[2]
                    
            #Draw screen
            if instance == 0:
                for i in range(3):
                    if i != cursorRow:
                        self.surface.blit(tRect, (60+240*i,90))
                        
                    else:
                        text = font.render(str(location[2]), True, (9,24,102))
                        pygame.draw.rect(self.surface, (0,0,0), (60+240*i, 90, 190, 280))
                        pygame.draw.rect(self.surface, (107,182,239), (60+240*i, 90, 190, 280), 10)
                        #DPAD
                        pygame.draw.rect(self.surface, (0,0,0), (130+240*i, 390, 50, 50))
                        pygame.draw.rect(self.surface, (46,102,193), (135+240*i, 395, 40, 40))
                        pygame.draw.rect(self.surface, (107,182,239), (142.5+240*i, 402.5, 27.5, 27.5))

            #Text box
            self.surface.blit(tTextRect, (100,500))
            textEntry = text.get_rect()
            textEntry.topleft = (pygame.Rect(120, 520, 600, 100)).topleft
            self.surface.blit(text, textEntry)
            "Print second line of instructions"
            if location[0] == -1:
                textEntry = text2.get_rect()
                textEntry.topleft = (pygame.Rect(120, 540, 600, 100)).topleft
                self.surface.blit(text2, textEntry)
            pygame.draw.rect(self.surface, (46,102,193), (100, 500, 600, 100), 7)

            #Render a mini menu if needed
            if instance == 1:
                self.miniMenu(miniMenu)
            
            pygame.display.update()

    def adventureMode(self, debug=False):
        engine = gameEngine.engine(self.surface, (800,600), debug)
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
            pygame.time.delay(16)
            arguments = engine.update()
            if arguments == 0:
                return self.mainMenu(0)
            hud.update(arguments[0], [], arguments[1], arguments[2])
    
    def getPath(self):
        path = __file__
        #Remove the file name
        path = path.split('\\')
        path.pop()
        path = '\\'.join(path)
        return path

"""pygame.draw.rect(surface, (0,0,0), (100, 80, 300, 400))
pygame.draw.rect(surface, (0,0,0), (450, 80, 250, 190))
pygame.draw.rect(surface, (0,0,0), (450, 280, 250, 100))
pygame.draw.rect(surface, (0,0,0), (450, 390, 250, 100))"""

"""pygame.draw.rect(surface, (0,0,0), (100, 80, 600, 190))
pygame.draw.rect(surface, (0,0,0), (100, 280, 310, 210))
pygame.draw.rect(surface, (0,0,0), (440, 280, 260, 100))
pygame.draw.rect(surface, (0,0,0), (440, 390, 260, 100))"""

"""pygame.draw.rect(surface, (0,0,0), (0, 120, 280, 70))
pygame.draw.rect(surface, (0,0,0), (0, 210, 280, 70))
pygame.draw.rect(surface, (0,0,0), (0, 300, 280, 70))
pygame.draw.rect(surface, (0,0,0), (0, 390, 280, 70))
pygame.draw.rect(surface, (0,0,0), (460, 120, 340, 350))"""


game = application()
    
