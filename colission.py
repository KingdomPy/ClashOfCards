import pygame, math

size = 40
angle = 0

pygame.init()
surface = pygame.display.set_mode((800, 600))

x = 400
y = 300

def getHitBox(x,y,surface, bullet, debug=True):
    size = 40
    bulletx, bullety = bullet
    #List of lines to check
    checks = []
    for i in range (10):
        size -= 4
        point1 = [size*math.cos(angle)+x, size*math.sin(angle)+y]
        point2 = [size*math.cos(angle+(7*math.pi)/9)+x, size*math.sin(angle+(7*math.pi)/9)+y]
        point3 = [size*math.cos(angle-(7*math.pi)/9)+x, size*math.sin(angle-(7*math.pi)/9)+y]
        checks.append(point1)
        checks.append(point2)
        checks.append(point3)
        points = (point1, point2, point3)
        if debug == True:
            pygame.draw.aalines(surface, (0,0,0), True, points)
    for i in range(len(checks)):
        touching = distanceLinePoint((checks[i],checks[(i+1)%len(checks)]), (bullet))
        if touching:
            return True

    return False

def distanceLinePoint(line, point):
    x0 = point[0]
    y0 = point[1]
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    #Check if point is within rectangle surrounding bordering the line
    if x0 >= min(x1,x2) and x0 <= max(x1,x2) and y0 >= min(y1,y2) and y0 <= max(y1,y2):
        distance = abs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/math.sqrt((y2-y1)**2+(x2-x1)**2)
        return distance <= 1

colour = (0,0,0)
while True:
    pygame.time.delay(16)
    surface.fill((255,255,255))
    
    point1 = [size*math.cos(angle)+x, size*math.sin(angle)+y]
    point2 = [size*math.cos(angle+(7*math.pi)/9)+x, size*math.sin(angle+(7*math.pi)/9)+y]
    point3 = [size*math.cos(angle-(7*math.pi)/9)+x, size*math.sin(angle-(7*math.pi)/9)+y]
    
    points = (point1, point2, point3)

    hit = getHitBox(x,y,surface,(400,280))
    if hit:
        colour = (150,20,20)

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

    pygame.draw.aalines(surface, colour, True, points)
    colour = (0,0,0)
    pygame.draw.rect(surface, (0,0,0), (400,280,2,2))
    
    pygame.display.update()
