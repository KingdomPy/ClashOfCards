import math

def collision(point, lineStart, lineEnd, variance):
    lineEnd[1] = 600 - lineEnd[1]
    lineStart[1] = 600 - lineStart[1]
    point[1] = 600 - point[1]
    
    print(lineStart, lineEnd)
    print(point)
    
    gradient = (lineEnd[1]-lineStart[1])/(lineEnd[0]-lineStart[0])
    constant = lineEnd[1]-(lineEnd[0]*gradient)
    normal = (-1)/gradient
    
    bisectedX = (point[0]+ point[1]*gradient -constant*gradient)/(gradient**2 + 1)
    bisectedY = bisectedX*gradient + constant

    print(bisectedX)
    print(math.sqrt((point[1]-bisectedY)**2 + (point[0]-bisectedX)**2))
    
    #Clip the line if it is too long
    if bisectedX >= lineEnd[0]:
        distance = math.sqrt((point[1]-lineEnd[1])**2 + (point[0]-lineEnd[0])**2)
        
    elif bisectedX <= lineStart[0]:
        distance = math.sqrt((point[1]-lineStart[1])**2 + (point[0]-lineStart[0])**2)
    
    else:
        distance = math.sqrt((point[1]-bisectedY)**2 + (point[0]-bisectedX)**2)
        
    if distance <= variance:
        print(distance)
        return True
    else:
        return False

def coll(point, lineStart, lineEnd, variance):
    gradient = (lineEnd[1]-lineStart[1])/(lineEnd[0]-lineStart[0])
    constant = lineEnd[1]-(lineEnd[0]*gradient)

    poa = point[0]*gradient+constant
    print(poa)
    if abs(point[1]-poa) <= variance:
        print(point[1]-poa)
        return True
    else:
        return False


def lineCollision(point, line, variance):
    #Get line and the points
    lineStart = line[0]
    lineEnd = line[1]
    x = point[0]
    y = point[1]

    #change in y
    deltaY = lineStart[1] - lineEnd[1]

    #change in x
    deltaX = lineStart[0] - lineEnd[0]

    if deltaY == 0:
        gradient = 0
        
    elif deltaX == 0:
        gradient = 0
        
    else:
        gradient = deltaY/deltaX

    #Check if its a vertical line
    if deltaX == 0:
        distance = abs(lineEnd[0] - x)
        maxY = max(lineEnd[1], lineStart[1])
        minY = min(lineEnd[1], lineStart[1])
        if y <= maxY and y >= minY:
            return(distance <= variance)

    else:
        constant = lineStart[1]-(lineStart[0]*gradient)

        shortestX = (x + y*gradient - constant*gradient)/(gradient**2 + 1)
        shortestY = shortestX*gradient + constant
        
        #Distance from perpendicular point
        distanceY = (shortestY - y)**2
        distanceX = (shortestX - x)**2
        distance = math.sqrt(distanceY+distanceX)

        #Clip the lines
        "Check which side of the line is the end"
        maxX = max(lineEnd[0], lineStart[0])
        minX = min(lineEnd[0], lineStart[0])
        
        maxY = max(lineEnd[1], lineStart[1])
        minY = min(lineEnd[1], lineStart[1])
        
        if shortestX <= maxX and shortestX >= minX and shortestY <= maxY and shortestY >= minY:
            return(distance <= variance)
        

points1 = [100, 100]
points2 = [101, 110]
x = 100
y = 104

#print(coll([x,y], points1, points2, 5))
print(lineCollision((x,y), (points1, points2), 0.5))
