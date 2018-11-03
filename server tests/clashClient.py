import socket, _thread, json
import pygame
import clashClasses

#SERVER_IP = input("Enter the servers ip: ")
SERVER_IP = "192.168.0.7"
SERVER_PORT = 8080
LOGIN = '["Nathan",[50,50,200]]'.encode()

class client:

    def __init__(self, ip, port, login):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("client test")

        self.server = (ip,port)
        self.loginSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.loginSocket.connect((ip,port))
        self.gameSocket.connect((ip, port))
        self.loginSocket.send(login)
        validation = self.loginSocket.recv(64)

        if not(validation.decode() == "0"):
            print("Login successful")
            self.loginSocket.close()
            pygame.time.delay(500)
            self.gameSocket.sendto(validation, self.server)
            self.main()
        else:
            print("Login failed")

    def main(self):
        _thread.start_new_thread(self.udp_network_thread, ())
        while True:
            pygame.time.delay(8)
            self.getInputs()
        self.gameSocket.close()    

    def udp_network_thread(self):
        while True:
            data = self.gameSocket.recvfrom(1024)
            packets = data[0].decode()
            packets = json.loads(packets)
            self.surface.fill((0,0,0))
            for i in range(0, len(packets)):
                self.render(packets[i])
            pygame.display.update()
            
    def getInputs(self):
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
        
        self.gameSocket.sendto(presses.encode(), self.server)

    def render(self, packet):
        player = clashClasses.player(self.surface)
        player.render(packet[0], packet[1], packet[2])
        del player
        

test = client(SERVER_IP, SERVER_PORT, LOGIN)
