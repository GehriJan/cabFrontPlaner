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
        for bump in self.textures:
            if first == True:
                Z = bump.function(X, Y)
                first = False
            else:
                Z += bump.function(X, Y)
        
        
        scene = dict(
            xaxis = dict(title='Länge', range = [0,max({self.lengthX, self.lengthY})]),
            yaxis = dict(title='Breite', range = [0,max({self.lengthX, self.lengthY})]),
            zaxis = dict(title='Tiefe', range = [0,max({self.lengthX, self.lengthY})]))
        
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])
        
        fig.update_layout(title='Schrankfront Modell', scene=scene)
        
        
        fig.show()
        

        
if __name__ == "__main__":
    front = graph(654, 780, 2)
    front.textures.add(bump(0.61*front.lengthX, 0.61*front.lengthY, 30, 20000))
    front.textures.add(bump(0.61*0.39*front.lengthX, 0.61*0.39*front.lengthY, 15, 20000))
    front.textures.add(bump(0.4*front.lengthX, 0.8*front.lengthY, 25, 30000))
    front.plot()