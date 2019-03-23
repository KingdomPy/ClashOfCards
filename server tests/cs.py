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
        self.roomsData = []
        for i in range(12):
            self.addRoom({"HOST": "killerjack1234", "MAP": "Deep Space", "PLAYERS": [["killerjack1234",1]]},
                         {"HOST":("192.168.0.7", 8080), "PLAYERS": [("192.168.0.7", 8080)]}
                         )
        
        #Data on addresses connected
        self.clientsData = []
        
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.bind((ip,port))
        self.tcpSocket.listen(1)

        print("TCP server on {}:{}".format(ip, port))
        
        _thread.start_new_thread(self.tcp_thread, ())

    def addRoom(self, publicData, privateData):
        #publicData is data that the client will see when room data is requested
        #privateData is data about the room that only the server can access
        ID = len(self.rooms) + 1
        publicData["ID"] = ID
        privateData["ID"] = ID
        self.rooms.append(publicData)
        self.roomsData.append(privateData)
        print(publicData["HOST"], privateData["HOST"], "created room with ID:", ID)

    def findRoom(self, ID):
        #Find room by ID
        for i in range(len(self.rooms)):
            if self.rooms[i]["ID"] == ID:
                return i
        return -1

    def tcp_thread(self):
        while True:
            #client, address
            client = self.tcpSocket.accept()
            if not(client[1] in self.clients):
                self.clients.append(client[1])
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
                    dataLocation = self.clients.index(client[1])
                    if data[0] == "SETNAME":
                        self.clientsData[dataLocation]["NAME"] = data[1]
                        report = "SETNAME: {}".format(data[1])

                    elif data[0] == "JOINROOM":
                        #If not in a room
                        if self.clientsData[dataLocation]["ROOM"] == "null":
                            #Search for the room, -1 = False (or else it will clash with 0)
                            found = self.findRoom(data[1])
                            if found != -1:
                                if len(self.rooms[found]["PLAYERS"]) < 4:
                                    self.clientsData[dataLocation]["ROOM"] = data[1]
                                    self.rooms[found]["PLAYERS"].append([self.clientsData[dataLocation]["NAME"],0])
                                    self.roomsData[found]["PLAYERS"].append(client[1])
                                    print(self.clientsData[dataLocation]["NAME"], client[1], "has joined the host:", self.rooms[found]["HOST"], self.roomsData[found]["HOST"])
                                    report = "JOINROOM: {}".format(data[1])
                                else:
                                    report = "ROOM FULL"
                            else:
                                report == "JOINROOM: {} not found.".format(data[1])
                        else:
                            report == "JOINROOM: {} failed, already in a room.".format(data[1])

                    elif data[0] == "TOGGLEREADY":
                        if self.clientsData[dataLocation]["ROOM"] == "null":
                            report = "NOT IN A ROOM"
                        else:
                            roomSlot = self.findRoom(self.clientsData[dataLocation]["ROOM"])
                            index = self.roomsData[roomSlot]["PLAYERS"].index(client[1])
                            #Toggle 1 to 0 and 0 to 1
                            self.rooms[roomSlot]["PLAYERS"][index][1] = 1 - self.rooms[roomSlot]["PLAYERS"][index][1]
                            report = "TOGGLED"

                    elif data[0] == "ADDROOM":
                        if self.clientsData[dataLocation]["ROOM"] == "null":
                            host = self.clientsData[dataLocation]["NAME"]
                            publicData = {"HOST": host, "MAP": data[1], "PLAYERS": [[host,0]]}
                            privateData = {"HOST": client[1], "PLAYERS": [client[1]]}
                            self.addRoom(publicData, privateData)
                            self.clientsData[dataLocation]["ROOM"] = self.rooms[len(self.rooms)-1]["ID"]
                        
                    #Get requests
                    elif data[0] == "GETNAME":
                        request = self.clientsData[dataLocation]["NAME"]
                        report = request

                    elif data[0] == "GETROOMS":
                        report = []
                        #Don't show full rooms
                        for i in range(len(self.rooms)):
                            if len(self.rooms[i]["PLAYERS"]) < 4:
                                report.append(self.rooms[i])
                        report = json.dumps(report)

                    elif data[0] == "GETSTATUS":
                        ID = self.clientsData[dataLocation]["ROOM"]
                        request = "NULL"
                        #Search for the room
                        if not(ID  == "null"):
                            found = self.findRoom(ID)
                            if found > -1:
                                request = json.dumps(self.rooms[found])
                        report = request

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
        dataLocation = self.clients.index(client[1])
        roomSlot = self.clientsData[dataLocation]["ROOM"]
        #Leave room if in a room
        if roomSlot != "null":
            name = self.clientsData[dataLocation]["NAME"]
            try: #Allows player to be fully removed even if they have been kicked from the room
                room = self.findRoom(roomSlot)
                for i in range(4):
                    if self.rooms[room]["PLAYERS"][i][0] == name:
                        self.rooms[room]["PLAYERS"].pop(i)
                        self.roomsData[room]["PLAYERS"].remove(client[1])
            except:
                pass
        self.clients.pop(dataLocation)
        self.clientsData.pop(dataLocation)
        print(client[1], "has disconnected")
        client[0].close()
                    
test = server(SERVER_IP, SERVER_PORT)
