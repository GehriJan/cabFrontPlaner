import numpy as np


class texture():
    def __init__(self, posX, posY, factorX, factorY, height, cover = None) -> None: 
        accuracy = 2
        self.posX = np.round(posX, accuracy)
        self.posY = np.round(posY, accuracy)
        self.height = np.round(height, accuracy)
        self.factorX = np.round(factorX, accuracy)
        self.factorY = np.round(factorY, accuracy)
        self.cover =  cover

class bump(texture):
    def function(self, x, y):
        
        factorX = np.log(2)/np.square(self.factorX)
        factorY = np.log(2)/np.square(self.factorY)
        
        return self.height*np.exp(-1*(factorX*np.square(x-self.posX)+factorY*np.square(y-self.posY)))
    
    def exportAutodesk(self) -> str:
        
        xPart = f"(log(2)/(factorX^2))*(x-posX)"
        yPart = f"(log(2)/(factorY^2))*(y-posY)"
        
        return f"height*exp(-1*({xPart}+{yPart}))"
    
class bumpGrid(texture):
    def function(self, x, y):
        factorX = (2*np.pi)/self.factorX
        factorY = (2*np.pi)/self.factorY
        return self.height*np.cos(factorX*(x-self.posX))*np.cos(factorY*(y-self.posY))

    def exportAutodesk(self) -> str:
        return f"height*cos(factorX*(x-posX))*cos(factorY*(y-posY))"

class rings(texture):
    def function(self, x, y):
        factorX = np.square((2*np.pi)/self.factorX)
        factorY = np.square((2*np.pi)/self.factorY)
        return self.height*np.cos(np.sqrt(((factorX*np.square(x-self.posX)+factorY*np.square(y-self.posY)))))

    def exportAutodesk(self) -> str:

        return f"height*cos(sqrt(factorX*pow((x-posX), 2)+factorY*pow((y-posY), 2)))"



class smoothEdges():
    def __init__(self, direction, distanceFromEdge, steepness, numStages, graphLengthX, graphLengthY) -> None:
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
        
        return otherVariable*0+1/(1+np.exp(directionFactor*self.steepness*(argument+shift))) #hier wurde mal round auf 8 nks entferns
    
    def exportAutodesk(self) -> str: # not finished
        
        if self.direction[0] == "-":
            sign = "-"
            shiftX = -self.distanceFromEdge
            shiftY = -self.distanceFromEdge
        else:
            sign = ""
            shiftX = -self.graphLengthX+self.distanceFromEdge
            shiftY = -self.graphLengthY+self.distanceFromEdge
        
        if self.direction[-1] == "x":
            argument = "x"
            shift = shiftX
            otherVariable = "y"
        else:
            argument = "y"
            shift = shiftY
            otherVariable = "x"
        
        
        return f"1/(1+pow(e,{sign}{self.steepness}*({argument}+({shift}))))"
        