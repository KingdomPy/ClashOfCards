#Online menu interface design
import pygame
import socket,json
import guiClasses as gui

#Networking config
SERVER_IP = "192.168.0.7"
SERVER_PORT = 8080

class multiplayerMenu:

    def __init__(self, surface, server):

        #Networking socket
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.connect(server)
        request = '["SETNAME", "Nathan"]'
        self.tcpSocket.send(request.encode())
        self.tcpSocket.recv(128)
        
        self.surface = surface
        self.main()

    def main(self):
        path = self.getPath()
        labelFont = pygame.font.Font(path+r"\assets\fonts\Kh2_Menu_Font.ttf", 22)
        textBoxFont = pygame.font.Font(path+r"\assets\fonts\OpenSans-Bold.ttf", 16)
        request = '["GETNAME"]'
        self.tcpSocket.send(request.encode())
        username = self.tcpSocket.recv(128).decode()
        box = gui.textBox(username, (46,102,193), textBoxFont, (140,50), (190,25))
        rooms = [{"ID":0, "HOST":"Fetching...", "MAP":"Loading...", "PLAYERS":[]}]

        self.scrolly = 0
        self.limit = 0
        self.target = -1 #The selected room
        self.joinedRoom = -1
        self.joinedRoomData = None
        
        clock = 0
        while True:
            clicked = False
            self.surface.fill((80,100,120))
            self.drawHud(self.joinedRoom)

            #Every half second reload room data
            if clock == 496:
                request = '["GETSTATUS"]'
                self.tcpSocket.send(request.encode())
                response = (self.tcpSocket.recv(2048)).decode()

                if response == '"null"': #Checks if in a room
                    request = '["GETROOMS"]'
                    self.tcpSocket.send(request.encode())
                    rooms = (self.tcpSocket.recv(2048)).decode()
                    rooms = json.loads(rooms)

                else:
                    self.joinedRoomData = json.loads(response)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.tcpSocket.close()
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    clicked = True

                '''elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.room == "null":
                            request = '["JOINROOM", 1]'
                            self.tcpSocket.send(request.encode())
                            data = self.tcpSocket.recv(2048).decode()
                            if data[0] == "J":
                                print(data)'''
                            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                if self.scrolly < 0:
                    self.scrolly += 10

            if keys[pygame.K_s]:
                if self.scrolly > self.limit:
                    self.scrolly -= 10
            
            box.render(self.surface)
            if self.joinedRoom == -1:
                self.drawRooms(rooms)
                if clicked == True:
                    if not(self.target == -1):
                        ID = self.rooms[self.target].ID
                        request = json.dumps(["JOINROOM", ID])
                        self.tcpSocket.send(request.encode())
                        data = self.tcpSocket.recv(2048).decode()
                        if data[0] == "J":
                            self.joinedRoom = ID
        
            #Frame
            pygame.draw.rect(self.surface, (9,24,102), (70,100,660,460), 7)
            pygame.display.update()
            pygame.time.delay(16)
            clock += 16
            clock %= 992
            
    def drawHud(self, room):
        "colour codes"
        #(46,102,193) - light blue
        #(35,77,145) - light blue 75% (blue)
        #(23,51,97)  - light blue 50% (blue)
        #(9,24,102) - dark blue
        
        path = self.getPath()
        labelFont = pygame.font.Font(path+r"\assets\fonts\Kh2_Menu_Font.ttf", 16)
        textBoxFont = pygame.font.Font(path+r"\assets\fonts\OpenSans-Bold.ttf", 16)
        
        "Field box"
        pygame.draw.rect(self.surface, (46,102,193), (70,100,660,80))
        
        "Field text"
        if room == -1:
            #ID | Host | Map | Players
            text1 = labelFont.render("Id", True, (235,235,235))
            text2 = labelFont.render("Host", True, (235,235,235))
            text3 = labelFont.render("Map", True, (235,235,235))
            text4 = labelFont.render("Players", True, (235,235,235))

            box1 = text1.get_rect()
            box1.center = pygame.Rect(10,113,200,50).center
            box2 = text2.get_rect()
            box2.center = pygame.Rect(175,113,200,50).center
            box3 = text2.get_rect()
            box3.center = pygame.Rect(340,113,200,50).center
            box4 = text3.get_rect()
            box4.center = pygame.Rect(505,113,200,50).center
                
            self.surface.blit(text1, box1)
            self.surface.blit(text2, box2)
            self.surface.blit(text3, box3)
            self.surface.blit(text4, box4)
            
        else:
            if not(self.joinedRoomData):
                clock = 496 #Skip to loading data
                hostText = labelFont.render("LOADING", True, (235,235,235))
            else:
                hostText = labelFont.render(self.joinedRoomData["HOST"]+'S LOBBY', True, (235,235,235))
                "#Box divider lines"
                
                #Information boxes
                pygame.draw.rect(self.surface, (35,77,145), (70,440,660,120))
                pygame.draw.rect(self.surface, (23,51,97), (70,410,660,30))

                #Information dividor lines
                pygame.draw.line(self.surface, (9,24,102), (70,440), (730,440), 4)
                pygame.draw.line(self.surface, (9,24,102), (70,410), (730,410), 4)
                
                #Player dividor lines
                pygame.draw.line(self.surface, (9,24,102), (235,180), (235,560), 4)
                pygame.draw.line(self.surface, (9,24,102), (400,180), (400,560), 4)
                pygame.draw.line(self.surface, (9,24,102), (565,180), (565,560), 4)

                
                
                
            hostBox = hostText.get_rect()
            hostBox.center = pygame.Rect(360,113,80,50).center
            self.surface.blit(hostText, hostBox)
        
        pygame.draw.line(self.surface, (9,24,102), (70,180), (730,180), 4)

    def drawRooms(self, rooms):
        self.rooms = [] #clear the memory
        length = len(rooms)
        x, y = pygame.mouse.get_pos()
        self.target = -1

        #Set clip boundary
        surface.set_clip((70,183,660,377))
        for i in range(length):
            if x >= 70 and x <=730 and y >= 180+i*50+self.scrolly and y <= 230+i*50+self.scrolly:
                touching = True
                self.target = i
                #top yellow line
                pygame.draw.line(surface, (220,220,0), (70,183+i*50+self.scrolly), (730,183+i*50+self.scrolly), 1)
            else:
                touching = False  
            self.rooms.append(gui.roomEntry(self.surface, rooms[i], 183+i*50+self.scrolly, touching)) #store room in the memory
        surface.set_clip()
        
        self.limit = 50 + -50 * length
        if self.scrolly < self.limit:
            self.scrolly = self.limit
    
    def getPath(self):
        path = __file__
        path = path.split('\\')
        #Go to root folder
        path.pop()
        path.pop()
        path = '\\'.join(path)
        return path
                
#Test the menu
if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("multiplayer client test")
    multiplayerMenu(surface, (SERVER_IP, SERVER_PORT))
