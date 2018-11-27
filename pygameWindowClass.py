import sys
import pygame
import classdir

class clashOfCards():

    def __init__ (self, name ="Clash of Cards", width = 800, height = 600):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.running = True

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

        #Player objects
        self.projectiles = []
        #0 = right, 1 = left
        self.player1StatsBar = classdir.statsBar(self.window, self.testPlayer.maxHp, self.testPlayer.maxMp, 250, 10 , 0)
        self.player2StatsBar = classdir.statsBar(self.window, self.testPlayer2.maxHp, self.testPlayer.maxMp, 250, 10 , 1)

        #Interactive objects
        "Text loader"
        self.menuFont = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.optionsFont =  pygame.font.Font(pygame.font.get_default_font(), 14)

        "Main Menu"
        self.adventureOption = classdir.mainButton(255, 255, 255, 220, 170, 340, 50, "ADVENTURE", (0,0,0), self.menuFont)
        self.versusOption = classdir.mainButton(255, 255, 255, 220, 230, 340, 50, "VERSUS", (0,0,0), self.menuFont)
        self.optionsOption = classdir.mainButton(255, 255, 255, 220, 290, 340, 50, "OPTIONS", (0,0,0), self.menuFont)
        self.extrasOption = classdir.mainButton(255, 255, 255, 220, 350, 340, 50, "EXTRAS", (0,0,0), self.menuFont)

        "Colour Menu player 1"
        self.slider1 = classdir.slider(255, 100, 100, 350, 75, 400, 30)
        self.slider2 = classdir.slider(255, 100, 100, 350, 125, 400, 30)
        self.slider3 = classdir.slider(255, 100, 100, 350, 175, 400, 30)
        self.p1Asettings = classdir.mainButton(255, 255, 255, 350, 225, 80, 30, "Attack", (0,0,0), self.optionsFont)
        self.p1Bsettings = classdir.mainButton(255, 255, 255, 450, 225, 80, 30, "Back", (0,0,0), self.optionsFont)
        self.p1Psettings = classdir.mainButton(255, 255, 255, 550, 225, 80, 30, "Primary", (0,0,0), self.optionsFont)

        "Colour Menu player 2"
        self.slider4 = classdir.slider(255, 100, 100, 350, 375, 400, 30)
        self.slider5 = classdir.slider(255, 100, 100, 350, 425, 400, 30)
        self.slider6 = classdir.slider(255, 100, 100, 350, 475, 400, 30)
        self.p2Asettings = classdir.mainButton(255, 255, 255, 350, 525, 80, 30, "Attack", (0,0,0), self.optionsFont)
        self.p2Bsettings = classdir.mainButton(255, 255, 255, 450, 525, 80, 30, "Back", (0,0,0), self.optionsFont)
        self.p2Psettings = classdir.mainButton(255, 255, 255, 550, 525, 80, 30, "Primary", (0,0,0), self.optionsFont)

        #Image loading
        self.backgroundAnimation = []
        imgPath = self.getPath()+"/assets/background/frame_"
        endPath = "_delay-0.03s.jpg"
        for i in range (0, 164):
            file = str(i)
            if len(str(i)) < 2:
                file = "00"+str(i)
            elif len(str(i)) < 3:
                file = "0"+str(i)
            image = pygame.image.load(imgPath+file+endPath).convert()
            self.backgroundAnimation.append(image)
        self.cycle = 0

        print("<instance>Main menu has been launched.")
        self.runMainMenu()

    #Cross platform get path method
    def getPath(self):
        path = __file__
        #Remove the file name
        path = path.split('\\')
        path.pop()
        path = '\\'.join(path)
        return path

    #Procedure to end the application
    def closeGame(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def runMainMenu(self):
        #Run instance
        while self.running:
            pygame.time.delay(33)

            x, y = pygame.mouse.get_pos()
            self.adventureOption.collision(x, y)
            self.versusOption.collision(x, y)
            self.optionsOption.collision(x, y)
            self.extrasOption.collision(x, y)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closeGame()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.versusOption.selected == True:
                        print("<select>Playground has been launched.")
                        self.runSimulation()

                    elif self.optionsOption.selected == True:
                        self.runOptions()

            #Load background animation
            self.window.blit(self.backgroundAnimation[self.cycle], (0,0))
            self.cycle +=1
            self.cycle %= 164

            #Display text
            self.adventureOption.update(self.window)
            self.versusOption.update(self.window)
            self.optionsOption.update(self.window)
            self.extrasOption.update(self.window)
            
            pygame.display.update()

    def runOptions(self):
        #Store players old position
        prev_x, prev_y, prev_angle = self.testPlayer.x, self.testPlayer.y, self.testPlayer.angle
        prev_x2, prev_y2, prev_angle2 = self.testPlayer2.x, self.testPlayer2.y, self.testPlayer2.angle

        #Sender player to new location to display colours
        self.testPlayer.teleport(200,140)
        self.testPlayer2.teleport(200,440)

        #Init slider
        red, green, blue = self.testPlayer.originalColours
        self.slider1.initColours(red)
        self.slider2.initColours(green)
        self.slider3.initColours(blue)

        red, green, blue = self.testPlayer2.originalColours
        self.slider4.initColours(red)
        self.slider5.initColours(green)
        self.slider6.initColours(blue)
            
        while self.running:
            pygame.time.delay(33)

            #Fetch player colours
            self.slider1.setColours(self.testPlayer.originalColours)
            self.slider2.setColours(self.testPlayer.originalColours)
            self.slider3.setColours(self.testPlayer.originalColours)
            
            self.slider4.setColours(self.testPlayer2.originalColours)
            self.slider5.setColours(self.testPlayer2.originalColours)
            self.slider6.setColours(self.testPlayer2.originalColours)

            #Mouse collision detection
            x, y = pygame.mouse.get_pos()

            self.p1Asettings.collision(x, y)
            self.p1Bsettings.collision(x, y)
            self.p1Psettings.collision(x, y)

            self.p2Asettings.collision(x, y)
            self.p2Bsettings.collision(x, y)
            self.p2Psettings.collision(x, y)

            self.slider1.collision(x, y)
            self.slider2.collision(x, y)
            self.slider3.collision(x, y)
            
            self.slider4.collision(x, y)
            self.slider5.collision(x, y)
            self.slider6.collision(x, y)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closeGame()

            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()

            #Mouse clicked
            if mouse[0]:
                if self.slider1.selected == True:
                    self.slider1.setBar(x)

                elif self.slider2.selected == True:
                    self.slider2.setBar(x)

                elif self.slider3.selected == True:
                    self.slider3.setBar(x)

                if self.slider4.selected == True:
                    self.slider4.setBar(x)

                elif self.slider5.selected == True:
                    self.slider5.setBar(x)

                elif self.slider6.selected == True:
                    self.slider6.setBar(x)

            if keys[pygame.K_ESCAPE]:
                #Fetch and load old player's coordinates
                self.testPlayer.teleport(prev_x, prev_y, prev_angle)
                self.testPlayer2.teleport(prev_x2, prev_y2, prev_angle2, True)
                
                print("<key>Main menu has been launched.")
                self.runMainMenu()

            #Load background animation
            self.window.fill((0,0,0))
            #self.window.blit(self.backgroundAnimation[self.cycle], (0,0))
            #self.cycle +=1
            #self.cycle %= 164

            #Fetch slider and update them
            
            red = self.slider1.update(self.window, "red")
            green = self.slider2.update(self.window, "green")
            blue = self.slider3.update(self.window, "blue")

            red2 = self.slider4.update(self.window, "red")
            green2 = self.slider5.update(self.window, "green")
            blue2 = self.slider6.update(self.window, "blue")

            #Update settings
            self.p1Asettings.update(self.window)
            self.p1Bsettings.update(self.window)
            self.p1Psettings.update(self.window)

            self.p2Asettings.update(self.window)
            self.p2Bsettings.update(self.window)
            self.p2Psettings.update(self.window)

            #Update slider colours
            
            self.slider1.setColours((red, green, blue))
            self.slider2.setColours((red, green, blue))
            self.slider3.setColours((red, green, blue))

            self.slider4.setColours((red2, green2, blue2))
            self.slider5.setColours((red2, green2, blue2))
            self.slider6.setColours((red2, green2, blue2))

            #Render player
            self.testPlayer.setColours(red, green, blue)
            self.testPlayer2.setColours(red2, green2, blue2)
            
            self.testPlayer.rotate(0.06)
            self.testPlayer2.rotate(0.06)
            
            self.testPlayer.update()
            self.testPlayer2.update()

            pygame.display.update()

    def runSimulation(self):
        #Run instance
        while self.running:
            pygame.time.delay(33)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closeGame()

            keys = pygame.key.get_pressed()

            #Command controls
            if keys[pygame.K_p]:
                print("<key>Main menu has been launched.")
                self.runMainMenu()

            # Player 1 controls
            if keys[pygame.K_w]:
                self.testPlayer.moveForward()

            if keys[pygame.K_d]:
                self.testPlayer.rotate(0.15)

            if keys[pygame.K_a]:
                self.testPlayer.rotate(-0.15)

            if keys[pygame.K_x]:
                self.testPlayer.commandBack()

            if keys[pygame.K_t]:
                skill = self.testPlayer.commandPrimary()
                if skill != 0:
                    if skill[0] == "Aura":
                        angle = 0
                        for i in range (0, 6):
                            self.projectiles.append(classdir.aura(self.window, skill[1], skill[2], angle ,skill[4], skill[5], 2, self.testPlayer))
                            angle += (1)

            if keys[pygame.K_r]:
                bullet = self.testPlayer.shootBullet()
                #Checks if the ability is available 
                if bullet != 0:
                    if bullet[0] == "Surge":
                        self.projectiles.append(classdir.projectile(self.window, bullet[1], bullet[2], bullet[3], bullet[4], bullet[5], 2))
                    elif bullet[0] == "Shotgun":
                        angle = bullet[3]
                        self.projectiles.append(classdir.projectile(self.window, bullet[1], bullet[2], angle, bullet[4], bullet[5], 2))
                        angle += 0.12
                        self.projectiles.append(classdir.projectile(self.window, bullet[1], bullet[2], angle, bullet[4], bullet[5], 2))
                        angle -= 0.24
                        self.projectiles.append(classdir.projectile(self.window, bullet[1], bullet[2], angle, bullet[4], bullet[5], 2))

            # Player 2 controls
            if keys[pygame.K_UP]:
                self.testPlayer2.moveForward()

            if keys[pygame.K_RIGHT]:
                self.testPlayer2.rotate(0.15)

            if keys[pygame.K_LEFT]:
                self.testPlayer2.rotate(-0.15)

            if keys[pygame.K_DOWN]:
                self.testPlayer2.commandBack()

            if keys[pygame.K_KP2]:
                skill = self.testPlayer2.commandPrimary()
                if skill != 0:
                    if skill[0] == "Aura":
                        angle = 0
                        for i in range (0, 6):
                            self.projectiles.append(classdir.aura(self.window, skill[1], skill[2], angle ,skill[4], skill[5], 1, self.testPlayer2))
                            angle += (1)

            if keys[pygame.K_KP1]:
                bullet = self.testPlayer2.shootBullet()
                #Checks if the ability is available 
                if bullet != 0:
                    #0 = type, 1 = position, 2 = angle, 3 = colours end value is the player that is targeted
                    if bullet[0] == "Surge":
                        self.projectiles.append(classdir.projectile(self.window, bullet[1], bullet[2], bullet[3], bullet[4], bullet[5], 1))
                    elif bullet[0] == "Shotgun":
                        angle = bullet[3]
                        self.projectiles.append(classdir.projectile(self.window, bullet[1], bullet[2], angle, bullet[4], bullet[5], 1))
                        angle += 0.12
                        self.projectiles.append(classdir.projectile(self.window, bullet[1], bullet[2], angle, bullet[4], bullet[5], 1))
                        angle -= 0.24
                        self.projectiles.append(classdir.projectile(self.window, bullet[1], bullet[2], angle, bullet[4], bullet[5], 1))

            self.window.fill((0, 0, 0))

            #render players and health bars
            self.testPlayer.update()
            self.testPlayer2.update()
            self.player1StatsBar.update(self.testPlayer.hp, self.testPlayer.mana)
            self.player2StatsBar.update(self.testPlayer2.hp, self.testPlayer2.mana)

            #Check for bullet collisions
            for i in range (0, len(self.projectiles)):
                x,y = self.projectiles[i].getPosition()
                if self.projectiles[i].target == 1:
                    if self.testPlayer.collision(x, y, self.projectiles[i].damage, 5):
                        self.projectiles[i].hit()
                        
                if self.projectiles[i].target == 2:
                    if self.testPlayer2.collision(x, y, self.projectiles[i].damage, 5):
                        self.projectiles[i].hit()
            
            #Check if any objects need to be deleted
            pointer = 0
            while pointer < len(self.projectiles):
                if self.projectiles[pointer].delete == True:
                    del self.projectiles[pointer]
                    pointer -= 1
                pointer +=1
                
            #render bullets
            for i in range (0, len(self.projectiles)):
                self.projectiles[i].move()
                self.projectiles[i].update()

            pygame.display.update()

gameLaunch = clashOfCards("Clash of Cards Developer Build")

