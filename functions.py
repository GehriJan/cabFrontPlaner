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

class smoothEdges():
    def __init__(self, direction, distanceFromEdge, steepness, graphLengthX, graphLengthY) -> None: # specialParam is density 
        self.direction = direction
        self.distanceFromEdge = distanceFromEdge
        self.steepness = abs(steepness)
        self.graphLengthX = graphLengthX
        self.graphLengthY = graphLengthY
        
    def function(self, x, y):
        if self.direction[0] == "-":
            directionFactor = -1
            shiftX = -self.distanceFromEdge
            shiftY = -self.distanceFromEdge
        else:
            directionFactor = 1
            shiftX = -self.graphLengthX+self.distanceFromEdge
            shiftY = -self.graphLengthY+self.distanceFromEdge
        
        if self.direction[-1] == "x":
            argument = x
            shift = shiftX
            otherVariable = y
        else:
            argument = y
            shift = shiftY
            otherVariable = x
        
        
        
        return np.round(otherVariable*0+1/(1+np.exp(directionFactor*self.steepness*(argument+shift))), 8)
        