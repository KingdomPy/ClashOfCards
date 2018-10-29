#Tutorial https://www.youtube.com/watch?v=SepyXsvWVfo

import socket, pygame

pygame.init()
pygame.display.set_mode((400,400))
pygame.display.set_caption("pygame client test")

ip = "192.168.0.7"
port = 8888

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip,port))

data = client.recv(1024)
print(data.decode())
while True:
    pygame.time.delay(33)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_t]:
        array = (keys[pygame.K_w], keys[pygame.K_d], keys[pygame.K_a], keys[pygame.K_t])
        keysPressed = str(array)
        client.send(keysPressed.encode())
    else:
        client.send(str.encode("None"))
    data = client.recv(1024)
    print(data.decode())

client.close()
