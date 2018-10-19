import pygame
import math
import scrollingClassdir

class clashOfCards():

    def __init__ (self, name ="Map Test", width = 800, height = 600):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.mapData = [["tlc","h","h","h","tw","h","h","h","trc"],
                        ["v","2","3","4","v","6","7","8","v"],
                        ["v","2","3","4"," ","6","7","8","v"],
                        ["v","2","3","4","v","6","7","8","v"],
                        ["v","2","3","4"," ","6","7","8","v"],
                        ["v","2","3","4","v","6","7","8","v"],
                        ["v","2","3","4"," ","6","7","8","v"],
                        ["v","2","3","4","v","6","7","8","v"],
                        ["blc","h","h","h","bw","h","h","h","brc"]]

        #tlc, trc: top left/right corner
        #blc, brc: bottom left/right cornet
        #v vertical line
        #h horizontal line
        #bw/tw bottom/top wedge

        self.angle = 0
        self.x = 100
        self.y = 100
        self.velocity = 12
        self.test()

    def render(self, mapData, scale, cameraX, cameraY):
        for y in range (0, 9):
            for x in range (0, 9):
                if mapData[y][x] == "v":
                    pygame.draw.line(self.window, (255,255,255), (cameraX+scale +x*scale, cameraY+scale//2 +y*scale), (cameraX +scale+x*scale, cameraY+(scale*3)//2 +y*scale), 2)

                elif mapData[y][x] == "h":
                    pygame.draw.line(self.window, (255,255,255), (cameraX+scale//2 +x*scale, cameraY+scale +y*scale), (cameraX+(scale*3)//2 +x*scale, cameraY+scale +y*scale), 2)

                elif mapData[y][x] == "tlc":
                    pygame.draw.line(self.window, (255,255,255), (cameraX +scale+x*scale, cameraY+scale +y*scale), (cameraX +(scale*3)//2+x*scale, cameraY+scale +y*scale), 2) #h
                    pygame.draw.line(self.window, (255,255,255), (cameraX +scale+x*scale, cameraY+scale +y*scale), (cameraX +scale+x*scale, cameraY +(scale*3)//2+ y*scale), 2) #v

                elif mapData[y][x] == "trc":
                    pygame.draw.line(self.window, (255,255,255), (cameraX+scale//2 +x*scale, cameraY+scale +y*scale), (cameraX+scale+ x*scale, cameraY+scale +y*scale), 2) #h
                    pygame.draw.line(self.window, (255,255,255), (cameraX +scale+x*scale, cameraY+scale +y*scale), (cameraX +scale+x*scale, cameraY+(scale*3)//2 +y*scale), 2) #v

                elif mapData[y][x] == "blc":
                    pygame.draw.line(self.window, (255,255,255), (cameraX +scale+x*scale, cameraY+scale +y*scale), (cameraX+(scale*3)//2 +x*scale, cameraY+scale +y*scale), 2) #h
                    pygame.draw.line(self.window, (255,255,255), (cameraX +scale+x*scale, cameraY+scale +y*scale), (cameraX +scale+x*scale, cameraY +scale//2+y*scale), 2) #v

                elif mapData[y][x] == "brc":
                    pygame.draw.line(self.window, (255,255,255), (cameraX+scale//2 +x*scale, cameraY+scale +y*scale), (cameraX+scale +x*scale, cameraY+scale +y*scale), 2) #h
                    pygame.draw.line(self.window, (255,255,255), (cameraX+scale +x*scale, cameraY+scale +y*scale), (cameraX+scale +x*scale, cameraY +scale//2+y*scale), 2) #v

                elif mapData[y][x] == "bw":
                    pygame.draw.line(self.window, (255,255,255), (cameraX+scale//2 +x*scale, cameraY+scale +y*scale), (cameraX+(scale*3)//2 +x*scale, cameraY+scale +y*scale), 2) #h
                    pygame.draw.line(self.window, (255,255,255), (cameraX+scale +x*scale, cameraY+scale +y*scale), (cameraX+scale +x*scale, cameraY +scale//2+y*scale), 2) #v

                elif mapData[y][x] == "tw":
                    pygame.draw.line(self.window, (255,255,255), (cameraX+scale//2 +x*scale, cameraY+scale +y*scale), (cameraX+(scale*3)//2 +x*scale, cameraY+scale +y*scale), 2) #h
                    pygame.draw.line(self.window, (255,255,255), (cameraX +scale+x*scale, cameraY+scale +y*scale), (cameraX +scale+x*scale, cameraY+(scale*3)//2 +y*scale), 2) #v

    def moveForward(self):
        self.x -= self.velocity * math.cos(self.angle)
        self.y += self.velocity * math.sin(self.angle)

    def rotate(self, angle):
        self.angle -= angle

    def test(self):
        testPlayer = scrollingClassdir.player(self.window, 255, 0, 0)
        testPlayer.teleport(400, 300)
        while True:
            pygame.time.delay(33)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.moveForward()

            if keys[pygame.K_d]:
                testPlayer.rotate(0.12)
                self.rotate(0.12)

            if keys[pygame.K_a]:
                testPlayer.rotate(-0.12)
                self.rotate(-0.12)

            self.window.fill((0,0,0))
            self.render(self.mapData, 150, self.x, self.y)
            testPlayer.update()
            pygame.display.update()

gameLaunch = clashOfCards("Map Test")

