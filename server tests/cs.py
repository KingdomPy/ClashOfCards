import socket, _thread, json
import pygame.time, time
from math import pi

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 8080

class server:

    def __init__(self, ip, port):
        #Addresses connected
        self.clients = []
        self.rooms = []
        testRoom = {"HOST":"killerjack1234", "MAP":"Deep Space", "PLAYERS":["killerjack1234"]}
        self.rooms.append(testRoom)
        
        #Data on addresses connected
        self.clientsData = []
        
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.bind((ip,port))
        self.tcpSocket.listen(1)

        print("TCP server on {}:{}".format(ip, port))
        
        _thread.start_new_thread(self.tcp_thread, ())

    def tcp_thread(self):
        while True:
            #client, address
            client = self.tcpSocket.accept()
            if not(client in self.clients):
                self.clients.append(client)
                data = {"NAME":"null", "ROOM":"null"}
                self.clientsData.append(data)
                _thread.start_new_thread(self.tcp_client_thread, (client,))
                print(client[1], "has connected")
            else:
                client.close()
        self.tcpSocket.close()

    def tcp_client_thread(self, client):
        while True:
            try:
                data = client[0].recv(128).decode()
                try:
                    data = json.loads(data)
                    #Set requests
                    if data[0] == "SETNAME":
                        dataLocation = self.clients.index(client)
                        self.clientsData[dataLocation]["NAME"] = data[1]
                        report = "SETNAME: {}".format(data[1])

                    elif data[0] == "JOINROOM":
                        dataLocation = self.clients.index(client)
                        #If not in a room
                        if self.clientsData[dataLocation]["ROOM"] == "null":
                            #Search for the room, -1 = False (or else it will clash with 0)
                            found = -1
                            for i in range(len(self.rooms)):
                                #Room found
                                if self.rooms[i]["HOST"] == data[1]:
                                    found = i
                                    break
                                
                            if found != -1:
                                self.clientsData[dataLocation]["ROOM"] = found
                                self.rooms[found]["PLAYERS"].append(self.clientsData[dataLocation]["NAME"])
                                print(self.clientsData[dataLocation]["NAME"], "has joined the host:", self.rooms[found]["HOST"])
                                report = "JOINROOM: {}".format(data[1])
                            else:
                                report == "JOINROOM: {} not found.".format(data[1])
                        else:
                            report == "JOINROOM: {} failed, already in a room.".format(data[1])
                        
                    #Get requests
                    elif data[0] == "GETNAME":
                        dataLocation = self.clients.index(client)
                        request = self.clientsData[dataLocation]["NAME"]
                        report = request

                    elif data[0] == "GETROOMS":
                        report = json.dumps(self.rooms)

                    #Request not found   
                    else:
                        report = "Command {} not found.".format(data[0])

                    client[0].send(report.encode())
                    
                except:
                    report = "Interpretation failed: {}".format(data)
                    client[0].send(report.encode())
            except:
                break
        #Player has disconnected
        #Check if in a room
        dataLocation = self.clients.index(client)
        name = self.clientsData[dataLocation]["NAME"]
        roomSlot = self.clientsData[dataLocation]["ROOM"]
        #Leave room ifin a room
        if roomSlot != "null":
            self.rooms[roomSlot]["PLAYERS"].remove(name)
        self.clients.remove(client)
        print(client[1], "has disconnected")
        client[0].close()
                    
test = server(SERVER_IP, SERVER_PORT)
