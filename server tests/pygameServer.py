import socket, _thread
import json
import pygame

UDP_IP = "127.0.0.1"
UDP_PORT = 8080

class server:

    def __init__(self, ip, port):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind((ip,port))

        print("UDP server on {}:{}".format(ip, port))
        
        #Addresses connected
        self.clients = []
        #Data on addresses connected
        self.clientsData = []
        #Address of those who have sent data
        self.recvPackets = []
        #Data to send to all the connected addresses
        self.sendPackets = []

        _thread.start_new_thread(self.update_thread, ())
        
        while True:
            try:
                data, address = self.serverSocket.recvfrom(24)
                
                #Create a player
                if not(address in self.clients):
                    self.clients.append(address)
                    self.clientsData.append([200,200])
                    
                #See if the server has caught their input
                if not(address in self.recvPackets):
                    self.recvPackets.append(address)
                    #Compute data
                    data = self.handleInput(data.decode(), self.clientsData[self.clients.index(address)])
                    self.sendPackets.append(data)

            except:
                continue

        self.serverSocket.close()
            

    def update_thread(self):
        while True:
            pygame.time.delay(33)
            pointer = 0
            while pointer < len(self.clients):
                try:
                    self.serverSocket.sendto(str(self.sendPackets).encode(), self.clients[pointer])
                    pointer += 1
                except:
                    print(self.clients[pointer], "has disconnected")
                    self.clientsData.pop(self.clients.index(self.clients[pointer]))
                    self.clients.remove(self.clients[pointer])
                    continue
            
            self.recvPackets = []
            self.sendPackets = []
        
    def handleInput(self, data, position):
        data = json.loads(data)

        if data[0]:
            position[0] -= 5
        if data[1]:
            position[0] += 5
        if data[2]:
            position[1] -= 5
        if data[3]:
            position[1] += 5

        return position
        
#serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#serverSocket.bind((UDP_IP, UDP_PORT))

#clients = []
#clientsData = []

#def movePlayer(data, position):
#    data = json.loads(data)

#    if data[0]:
#        position[0] -= 5
#    if data[1]:
#        position[0] += 5
#    if data[2]:
#        position[1] -= 5
#    if data[3]:
#        position[1] += 5
#
#    return position

#print("UDP server on {}:{}".format(UDP_IP,UDP_PORT))

#while True:
#    data, address = serverSocket.recvfrom(24)
#    if not(address in clients):
#        clients.append(address)
#        clientsData.append([200,200])
#    pointer = 0
#    data = movePlayer(data.decode(), clientsData[clients.index(address)])
#    clientsData[clients.index(address)] = data
#    data = str(data).encode()
#    while pointer < len(clients):
#        print(clients)
#        try:
#            serverSocket.sendto(data, clients[pointer])
#            pointer += 1
#        except:
#            print(clients[pointer], "has disconnected")
#            clientsData.pop(clients.index(clients[pointer]))
#            clients.remove(clients[pointer])
#            continue

test = server(UDP_IP, UDP_PORT)
