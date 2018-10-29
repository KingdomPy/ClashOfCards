#pygame server

import math, time
import socket, sys, _thread

global CONNECTED_CLIENTS
global LOBBIES

class server:

    def __init__(self, bind_ip, bind_port):
                        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((bind_ip, bind_port))
        self.server.listen(10)

        print("[*] Listening on {}:{}".format(bind_ip, bind_port))

        for i in range(0, len(LOBBIES)):
            _thread.start_new_thread(self.threaded_lobby, (LOBBIES[i],))
        
        while True:
            if len(CONNECTED_CLIENTS) < 10:
                
                client, address = self.server.accept()
                print("[+] {} is attempting to connect.".format(address))
                
                self.joinRoom(client,address)
                CONNECTED_CLIENTS.append(address)
                print("[+] {} has connected.".format(address))

    def threaded_lobby(self, lobby):
        while True:
            time.sleep(0.033)
            lobby.update()


    def joinRoom(self, client, address):
        for i in range (0, len(LOBBIES)):
            if LOBBIES[i].join(client, address):
                return i
            
class lobby:
    
    def __init__(self, size):
        self.size = size
        self.CLIENTS = []

    def join(self, client, address):
        if len(self.CLIENTS) < self.size:
            self.CLIENTS.append(client)
            _thread.start_new_thread(self.threaded_client, (client,address,))
            return 1
        else:
            return 0

    def threaded_client(self, client, address):
        client.send(str.encode("Connection successful."))
        while True:
            try:
                active = client.recv(1024)
                if not active:
                    break
                client.sendall(str.encode("\n"))
            except:
                break
        CONNECTED_CLIENTS.remove(address)
        self.leave(client)
        print("[-] {} has disconnected.".format(address))
        client.close()
    
    def leave(self, client):
        self.CLIENTS.remove(client)

    def update(self):
        inputs = []
        for i in range (0, self.size):
            try:
                inputs.append((self.CLIENTS[i].recv(1024)).decode())
                
            except:
                inputs.append("")
                continue
                
        for i in range(0, len(self.CLIENTS)):
            try:
                self.CLIENTS[i].sendall(str(inputs).encode())
            except:
                continue
        
CONNECTED_CLIENTS = []
LOBBIES = [lobby(2)] * 3

runServer = server("",8888)
