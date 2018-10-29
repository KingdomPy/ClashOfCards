import socket, _thread
import json
import pygame

UDP_IP = "127.0.0.1"
UDP_PORT = 8080
Message = "hello".encode()

class client:

    def __init__ (self, ip, port):
        pygame.init()
        self.surface = pygame.display.set_mode((400,400))
        pygame.display.set_caption("client test")

        self.server = (ip,port)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.connect((ip, port))

        _thread.start_new_thread(self.network_thread, ())

        while True:
            pygame.time.delay(33)
            self.pygameInputs()
            
        self.clientSocket.close()
        
    def network_thread(self):
        while True:
            data = self.clientSocket.recvfrom(48)
            packets = data[0].decode()
            packets = json.loads(packets)
            self.surface.fill((0,0,0))
            for i in range(0, len(packets)):
                self.render(packets[i])
            pygame.display.update()
    
    
    def pygameInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        presses = []

        presses.append(keys[pygame.K_a])
        presses.append(keys[pygame.K_d])
        presses.append(keys[pygame.K_w])
        presses.append(keys[pygame.K_s])
        
        presses = str(presses)
        
        self.clientSocket.sendto(presses.encode(), self.server)

    def render(self, data):
        pygame.draw.rect(self.surface, (100,50,50), (data[0], data[1], 20,20))


#while True:
    #keyboard(clientSocket, (UDP_IP, UDP_PORT), surface)
    #pygame.display.update()

test = client(UDP_IP, UDP_PORT)


