import pygame, math

size = 40
angle = 0

pygame.init()
surface = pygame.display.set_mode((800, 600))

x = 400
y = 300

def getHitBox(x,y,points, surface):
    for i in range(len(points)):
        #constMod is constant modifier, specifies if it should increase or decrease:
        constMod = 1
            
        #get line
        end = i+1
        end %= len(points)
        deltay = points[i][1] - points[end][1]
        deltax = points[i][0] - points[end][0]
        #0 = horizontal 1 = vertical 2 = normal
        if deltay == 0:
            line = 0
        elif deltax == 0:
            line = 1
        else:
            line = 2
            gradient = deltay/deltax
            constant = points[i][1] - points[i][0]*gradient
        for j in range(size):
            constant += constMod
            if line == 2:
                x1 = points[i][0]
                y1 = x1*gradient + constant
                x2 = points[end][0]
                y2 = x2*gradient + constant
                pygame.draw.aalines(surface, (50,0,0), False, ((x1,y1),(x2,y2)) )
        
while True:
    pygame.time.delay(16)
    surface.fill((255,255,255))
    
    point1 = [size*math.cos(angle)+x, size*math.sin(angle)+y]
    point2 = [size*math.cos(angle+(7*math.pi)/9)+x, size*math.sin(angle+(7*math.pi)/9)+y]
    point3 = [size*math.cos(angle-(7*math.pi)/9)+x, size*math.sin(angle-(7*math.pi)/9)+y]
    
    points = (point1, point2, point3)

    getHitBox(x,y,points, surface)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        angle -= 0.12
    if keys[pygame.K_d]:
        angle += 0.12
    if keys[pygame.K_w]:
        x += 4*math.cos(angle)
        y += 4*math.sin(angle)

    pygame.draw.aalines(surface, (0,0,0), True, points)
    pygame.draw.rect(surface, (0,0,0), (x,y,1,1))
    
    pygame.display.update()
