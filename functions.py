import numpy as np

class bump():
    def __init__(self, posX, posY, height, specialParam) -> None: # specialParam is bulbiness
        self.posX = posX
        self.posY = posY
        self.height = height
        self.specialParam = specialParam
    def function(self, x, y):
        return self.height*np.exp((-1/self.specialParam)*(np.square(x-self.posX)+np.square(y-self.posY)))
    
class bumpGrid():
    def __init__(self, posX, posY, height, specialParam) -> None: # specialParam is density
        self.posX = posX
        self.posY = posY
        self.height = height
        self.specialParam = specialParam
    def function(self, x, y):
        return self.height*np.cos((self.specialParam*np.pi/100)*(x-self.posX))*np.cos((self.specialParam*np.pi/100)*(y-self.posY))
     
class rings():
    def __init__(self, posX, posY, height, specialParam) -> None: # specialParam is density 
        self.posX = posX
        self.posY = posY
        self.height = height
        self.specialParam = specialParam
    def function(self, x, y):
        return self.height*np.sin((self.specialParam/np.power(10,5))*np.sqrt(((np.square(x-self.posX)+np.square(y-self.posY)))))
