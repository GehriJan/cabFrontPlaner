import plotly.graph_objects as go
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
    def __init__(self, posX, posY, height, bulbiness) -> None:
        self.posX = posX
        self.posY = posY
        self.height = height
        self.bulbiness = bulbiness/np.power(10,5)
    def function(self, x, y):
        return self.height*np.sin(self.bulbiness*np.sqrt(((np.square(x-self.posX)+np.square(y-self.posY)))))


class graph():
    
    def __init__(self, lengthX, lengthY, stepSize) -> None:
        self.lengthX = lengthX
        self.lengthY = lengthY
        self.stepSize = stepSize
        self.textures = set()
        

    
    def plot(self):
        
        x = np.linspace(0, self.lengthX, int(np.floor(self.lengthX/self.stepSize)))
        y = np.linspace(0, self.lengthY, int(np.floor(self.lengthY/self.stepSize)))
        X, Y = np.meshgrid(x, y)
        
        first = True
        for characteristic in self.textures:
            if first == True:
                Z = characteristic.function(X, Y)
                first = False
            else:
                Z += characteristic.function(X, Y)
        
        scene = dict(
            xaxis = dict(title='Breite (x)', range = [0,max({self.lengthX, self.lengthY})]),
            yaxis = dict(title='Länge (y)', range = [0,max({self.lengthX, self.lengthY})]),
            zaxis = dict(title='Tiefe (z)', range = [-50,max({self.lengthX, self.lengthY})]))
        
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])
        
        fig.update_layout(title='Schrankfront Modell', scene=scene)
        
        fig.show()
        

        
if __name__ == "__main__":
    front = graph(654, 780, 1)
    front.textures.add(bump(0.61*front.lengthX, 0.61*front.lengthY, 30, 20000))
    front.textures.add(bump(0.61*0.39*front.lengthX, 0.61*0.39*front.lengthY, 15, 20000))
    front.textures.add(bump(0.61*0.7*front.lengthX, 0.61*0.7*front.lengthY, -25, 15000))
    
    front.textures.add(rings(-1.5*front.lengthX, 0.5*front.lengthY, 5, 5000))
    front.textures.add(rings(-1.5*front.lengthX, 1.5*front.lengthY, 15, 9000))
    #front.textures.add(rings(-15*front.lengthX, 15*front.lengthY, 15, 9000))
    front.textures.add(rings(2*front.lengthX, 2*front.lengthY, 10, 1000))
    front.textures.add(bumpGrid(0.5*front.lengthX, 0.5*front.lengthY, 10, 700))
    #front.textures.add(bumpGrid(0.6*front.lengthX, 0.3*front.lengthY, 3, 1000))
    #front.textures.add(bumpGrid(0.9*front.lengthX, 0.1*front.lengthY, 12, 200))
    #front.textures.add(bumpGrid(0.2*front.lengthX, 0.3*front.lengthY, 8, 700))
    #front.textures.add(bumpGrid(-0.5*front.lengthX, 0.4*front.lengthY, 6, 700))
    front.plot()