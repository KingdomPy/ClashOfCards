class character:

    def __init__ (self, data, x, y):
        self.data = data
        self.name = data['name']
        self.moveSpeed = data['moveSpeed']
        self.x = x
        self.y = y

    def moveUp(self):
        self.y-=self.moveSpeed

    def moveDown(self):
        self.y+=self.moveSpeed

    def moveRight(self):
        self.x+=self.moveSpeed

    def moveLeft(self):
        self.x-=self.moveSpeed

    def getColours(self):
        return {'red':self.data['red'], 'green':self.data['green'], 'blue':self.data['blue']}

    def getPosition(self):
        return {'x': self.x, 'y': self.y}

#{'name': 'Dragos', 'red': 255, 'green': 100, 'blue': 100, 'moveSpeed':3}
