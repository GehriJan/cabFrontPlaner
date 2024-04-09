import numpy as np


class texture():
    def __init__(self, posX, posY, factorX, factorY, height, cover = None) -> None: 
        self.posX = posX
        self.posY = posY
        self.height = height
        self.factorX = factorX
        self.factorY = factorY
        self.cover = cover

class bump(texture):
    def function(self, x, y):
        return self.height*np.exp(-1*((1/self.factorX)*np.square(x-self.posX)+(1/self.factorY)*np.square(y-self.posY)))
    
class bumpGrid(texture):
    def function(self, x, y):
        factorX = self.factorX*np.pi/100
        factorY = self.factorY*np.pi/100
        return self.height*np.cos(factorX*(x-self.posX))*np.cos(factorY*(y-self.posY))

class rings(texture):
    def function(self, x, y):
        factorX = np.square((2*np.pi)/self.factorX)
        factorY = np.square((2*np.pi)/self.factorY)
        return self.height*np.cos(np.sqrt(((factorX*np.square(x-self.posX)+factorY*np.square(y-self.posY)))))



class smoothEdges():
    def __init__(self, direction, distanceFromEdge, steepness, numStages, graphLengthX, graphLengthY) -> None: # specialParam is density 
        self.direction = direction
        self.distanceFromEdge = distanceFromEdge
        self.steepness = abs(steepness)
        self.numStages = numStages
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
        
        #computation
        stairDeterminer = 2*self.numStages-1
        
        argument = np.power(argument, stairDeterminer)
        
        return np.round(otherVariable*0+1/(1+np.exp(directionFactor*self.steepness*(argument+shift))), 8)
        