import socket, _thread, json
import pygame.time, time
from math import pi
import clashClasses

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 8080

class server:

    def __init__(self, ip, port):
        #Addresses connected
        self.clients = []
        self.authenticating = []
        self.authData = []
        
        #Data on addresses connected
        self.clientsData = []
        
        #Address of those who have sent data
        self.recvPackets = []
        
        #Data to send to all the connected addresses
        self.sendPackets = []
        
        #Track inactive users
        self.inactive = []
        self.clock = []
            
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSocket.bind((ip,port))
        
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.bind((ip,port))
        self.tcpSocket.listen(1)

        print("UDP & TCP server on {}:{}".format(ip, port))

        _thread.start_new_thread(self.udp_thread, ())
        _thread.start_new_thread(self.tcp_thread, ())



    def udp_thread(self):
        _thread.start_new_thread(self.udp_network_thread, ())
        while True:
            try:
                data, address = self.udpSocket.recvfrom(24)
                if address in self.clients:
                    #See if the server has caught their input
                    if not(address in self.recvPackets):
                        self.recvPackets.append(address)
                        #Compute data
                        data = self.returnInput(data, address)
                        self.sendPackets.append(data)
     
                    #Check if player was inactive
                    if address in self.inactive:
                        self.clock.pop(self.inactive.index(address))
                        self.inactive.remove(address)

                if data.decode() in self.authenticating:
                    location = self.authenticating.index(data.decode())
                    self.clients.append(address)
                    self.clientsData.append(self.authData[location])
                    self.authenticating.pop(location)
                    self.authData.pop(location)
                    
            except:
                continue

    def tcp_thread(self):
        while True:
            client, address = self.tcpSocket.accept()
            if not(address in self.clients or address in self.authenticating):
                _thread.start_new_thread(self.tcp_client_thread, (client, address))
            else:
                client.close()
        self.tcpSocket.close()

    def udp_network_thread(self):
        while True:
            pygame.time.delay(16)
            pointer = 0
            #check for data not sent by players
            self.orderPackets()
            #check for inactive players
            for i in range (0, len(self.clients)):
                try:
                    if not(self.clients[i] in self.recvPackets):
                        if not(self.clients[i] in self.inactive):
                            self.inactive.append(self.clients[i])
                            self.clock.append(0)
                        clock = self.inactive.index(self.clients[i])
                        self.clock[clock] += 1
                        if self.clock[clock] > 32:
                            self.removeClient(self.clients[i])
                except:
                    continue

            while pointer < len(self.clients) and not(self.sendPackets == []):
                try:
                    #update the players
                    self.udpSocket.sendto(str(self.sendPackets).encode(), self.clients[pointer])
                    pointer += 1
      
                except:
                    continue
            
            self.recvPackets = []
            self.sendPackets = []

    def tcp_client_thread(self, client, address):
        client.settimeout(2)
        data = client.recv(128)
        try:
            self.createPlayer(data)
            client.send(str(address).encode())
            print(address, "has connected")
            self.authenticating.append(str(address))
        except:
            client.send("0".encode())
            
    def createPlayer(self, data):
        data = json.loads(data.decode())
        self.authData.append(clashClasses.server_player(200, 200, pi/2, data[0], data[1]))     
        
    def removeClient(self, address):
        print(address, "has disconnected")
        self.clientsData.pop(self.clients.index(address))
        self.clients.remove(address)
        self.clock.pop(self.inactive.index(address))
        self.inactive.remove(address)
        
    def returnInput(self, data, address):
        data = json.loads(data.decode())
        player = self.clients.index(address)
        try:
            #a[0]/d[1]/w[2]/s[3]
            if data[0]:
                self.clientsData[player].rotate(-0.12)
            if data[1]:
                self.clientsData[player].rotate(+0.12)
            if data[2]:
                self.clientsData[player].moveForward()

            return self.clientsData[player].getData()
 
        except:
            pass

    def orderPackets(self):
        if len(self.clients) > len(self.recvPackets):
            for i in range(0, len(self.clients)):
                if not(self.clients[i] in self.recvPackets):
                    self.sendPackets.append(self.clientsData[i].getData())
                    
test = server(SERVER_IP, SERVER_PORT)
