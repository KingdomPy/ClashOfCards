#Tutorial https://www.youtube.com/watch?v=ZwxTGGEx-1w
#https://www.youtube.com/watch?v=WrtebUkUssc

import socket
import sys
import _thread

bind_ip = ""
bind_port = 8888

global CONNECTED_PLAYERS
global LOBBIES

CONNECTED_PLAYERS = []
LOBBIES = [([],[]),([],[]),([],[])]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(10)

print("[+] Listening on {}:{}".format(bind_ip, bind_port))

def threaded_client(client, address):
    client.send(str.encode("Successfully connected."))

    while True:
        try:
            data = client.recv(1024)
            reply = "Received: " + data.decode()
            if not data:
                break
            client.sendall(reply.encode())
        except:
            break
    CONNECTED_PLAYERS.remove(address)
    print(CONNECTED_PLAYERS)
    client.close()


while True:
    client, address = server.accept()
    print("[+] Client request from: {}".format(address))
    _thread.start_new_thread(threaded_client, (client,address,))
    CONNECTED_PLAYERS.append(address)
    print(CONNECTED_PLAYERS)
    
server.close()
