import socket, _thread, json
import sys, pygame, classdir

class Application:

    def __init__ (self, name ="Clash of Cards", mode="dev", width = 800, height = 600):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.running = True
        self.mode = mode

        if self.mode == "dev":
            #Load test players
            self.testPlayer = classdir.player(self.window, 255 ,100, 100)
            self.testPlayer2 = classdir.player(self.window, 100, 100, 255)
            "set coordinates and direction"
            self.testPlayer.teleport(50, 300, 0)
            self.testPlayer2.teleport(750, 300, 180)
            "set stats"
            self.testPlayer.setStats(99, 0, 100, 100, 20, 20)
            self.p1Commands = {"Str":"10", "Speed":8, "Attack": "Shotgun", "Back": "Dodge", "Primary": "Aura"}
            self.testPlayer.setCommands(self.p1Commands)
            self.testPlayer2.setStats(99, 0, 100, 100, 20, 20)
            self.p2Commands = {"Str":"10", "Speed":8, "Attack": "Shotgun", "Back": "Dodge", "Primary": "Aura"}
            self.testPlayer2.setCommands(self.p2Commands)

        self.projectiles = []
        #Pre-iage loading
        percentage = 0
        loadingFont = pygame.font.Font(pygame.font.get_default_font(), 28)
        loadingText = loadingFont.render("Loading: "+str(percentage)+"%", True, (255,255,255))
        self.backgroundAnimation = []
        imgPath = self.getPath()+"/assets/background/frame_"
        endPath = "_delay-0.03s.jpg"
        for i in range (0, 164):
            pygame.display.update()
            file = str(i)
            if len(str(i)) < 2:
                file = "00"+str(i)
            elif len(str(i)) < 3:
                file = "0"+str(i)
            image = pygame.image.load(imgPath+file+endPath).convert()
            #loading
            percentage = (100/163 * i)
            percentage = round(percentage,1)
            loadingText = loadingFont.render("Loading: "+str(percentage)+"%", True, (255,255,255))
            self.window.fill((0,0,0))
            frame = loadingText.get_rect()
            frame.bottomright = self.window.get_rect().bottomright
            self.window.blit(loadingText, frame)
            #loading
            self.backgroundAnimation.append(image)
        pygame.display.update()
        self.cycle = 0

        if self.mode != "pi":
            print("<instance>Main menu has been launched.")
        self.runMainMenu()

    def getPath(self):
        path = __file__
        #Remove the file name
        path = path.split('\\')
        path.pop()
        path = '\\'.join(path)
        return path
    
    def closeGame(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def runMainMenu(self):
        #Instantiate objects
        "Text loader"
        menuFont = pygame.font.Font(pygame.font.get_default_font(), 20)

        "Main Menu"
        adventureOption = classdir.mainButton(255, 255, 255, 220, 170, 340, 50, "ADVENTURE", (0,0,0), menuFont)
        versusOption = classdir.mainButton(255, 255, 255, 220, 230, 340, 50, "VERSUS", (0,0,0), menuFont)
        optionsOption = classdir.mainButton(255, 255, 255, 220, 290, 340, 50, "OPTIONS", (0,0,0), menuFont)
        extrasOption = classdir.mainButton(255, 255, 255, 220, 350, 340, 50, "EXTRAS", (0,0,0), menuFont)

        #Run instance
        while self.running:
            pygame.time.delay(16)

            x, y = pygame.mouse.get_pos()
            adventureOption.collision(x, y)
            versusOption.collision(x, y)
            optionsOption.collision(x, y)
            extrasOption.collision(x, y)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closeGame()

            if self.mode == "dev":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if versusOption.selected == True:
                        print("<select>Playground has been launched.")
                        self.runSimulation()

                    elif optionsOption.selected == True:
                        self.runOptions()

            #Load background animation
            if self.cycle%2 == 0:
                self.window.blit(self.backgroundAnimation[self.cycle//2], (0,0))
            self.cycle +=1
            self.cycle %= 328

            #Display text
            adventureOption.update(self.window)
            versusOption.update(self.window)
            optionsOption.update(self.window)
            extrasOption.update(self.window)
            
            pygame.display.update()
        
Application("Clash of Cards Developer Build", "dev")   
