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
        self.room = "null"
        
        clock = 0
        while True:
            self.surface.fill((80,100,120))
            self.drawHud()

            #Every half second reload room data
            if clock == 496:
                request = '["GETSTATUS"]'
                self.tcpSocket.send(request.encode())
                response = (self.tcpSocket.recv(2048)).decode()

                if response == '"null"': #Checks if in a room
                    self.room = "null"
                    request = '["GETROOMS"]'
                    self.tcpSocket.send(request.encode())
                    rooms = (self.tcpSocket.recv(2048)).decode()
                    rooms = json.loads(rooms)

                else:
                    self.room = response
                    rooms = [{"ID":9999, "HOST":"JOINED SUCCESSFULLY", "MAP":"9999", "PLAYERS":[1]}]
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.tcpSocket.close()
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.room == "null":
                            request = '["JOINROOM", 1]'
                            self.tcpSocket.send(request.encode())
                            data = self.tcpSocket.recv(2048).decode()
                            if data[0] == "J":
                                print(data)
                            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                if self.scrolly < 0:
                    self.scrolly += 10

            if keys[pygame.K_s]:
                if self.scrolly > self.limit:
                    self.scrolly -= 10
            
            box.render(self.surface)
            self.drawRooms(rooms)
            #Frame
            pygame.draw.rect(self.surface, (9,24,102), (70,100,660,460), 7)
            pygame.display.update()
            pygame.time.delay(16)
            clock += 16
            clock %= 992
            
    def drawHud(self):
        #(46,102,193) light  blue, (9,24,102) dark blue colour codes
        path = self.getPath()
        labelFont = pygame.font.Font(path+r"\assets\fonts\Kh2_Menu_Font.ttf", 16)
        textBoxFont = pygame.font.Font(path+r"\assets\fonts\OpenSans-Bold.ttf", 16)
        
        "Field box"
        pygame.draw.rect(self.surface, (46,102,193), (70,100,660,80))
        
        "Field text"
        #ID | Host | Map | Players
        text1 = labelFont.render("Id", True, (235,235,235))
        text2 = labelFont.render("Host", True, (235,235,235))
        text3 = labelFont.render("Map", True, (235,235,235))
        text4 = labelFont.render("Players", True, (235,235,235))

        box1 = text1.get_rect()
        box1.center = pygame.Rect(10,113,220,50).center
        box2 = text2.get_rect()
        box2.center = pygame.Rect(175,113,220,50).center
        box3 = text2.get_rect()
        box3.center = pygame.Rect(340,113,220,50).center
        box4 = text3.get_rect()
        box4.center = pygame.Rect(505,113,220,50).center
            
        self.surface.blit(text1, box1)
        self.surface.blit(text2, box2)
        self.surface.blit(text3, box3)
        self.surface.blit(text4, box4)
        
        pygame.draw.line(self.surface, (9,24,102), (70,180), (730,180), 4)

    def drawRooms(self, rooms):
        length = len(rooms)
        for i in range(length):
            gui.roomEntry(self.surface, rooms[i], 180+i*50, self.scrolly)
        self.limit = 50 + -50 * length
    
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
