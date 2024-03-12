import numpy as np

class bump():
    def __init__(self, posX, posY, height, bulbiness) -> None:
        self.posX = posX
        self.posY = posY
        self.height = height
        self.bulbiness = bulbiness
    def function(self, x, y):
        return self.height*np.exp((-1/self.bulbiness)*(np.square(x-self.posX)+np.square(y-self.posY)))
    
class bumpGrid():
    def __init__(self, posX, posY, height, density) -> None:
        self.posX = posX
        self.posY = posY
        self.height = height
        self.density = density*np.pi/100
    def function(self, x, y):
        return self.height*np.cos(self.density*(x-self.posX))*np.cos(self.density*(y-self.posY))
     
class rings():
    def __init__(self, posX, posY, height, density) -> None:
        self.posX = posX
        self.posY = posY
        self.height = height
        self.density = density/np.power(10,5)
    def function(self, x, y):
        return self.height*np.sin(self.density*np.sqrt(((np.square(x-self.posX)+np.square(y-self.posY)))))
