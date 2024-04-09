import plotly.graph_objects as go
import numpy as np
import json
from datetime import datetime
from functions import *




class graph():
    
    def __init__(self, lengthX, lengthY, stepSize) -> None:
        self.lengthX = lengthX
        self.lengthY = lengthY
        self.stepSize = stepSize
        self.textures = set()
        self.borders = set()
        
    
    def computeField(self):
        x = np.linspace(0, self.lengthX, int(np.floor(self.lengthX/self.stepSize)))
        y = np.linspace(0, self.lengthY, int(np.floor(self.lengthY/self.stepSize)))
        X, Y = np.meshgrid(x, y)
        
        Z = 0*X*Y
        for i in {-1, 0, 1}:
            for texture in self.textures:
                cover = texture.cover.function(X,Y+self.lengthY*i) if hasattr(texture, "cover") and texture.cover != None else np.power(X, 0)*np.power(Y, 0)
                Z += texture.function(X,Y+self.lengthY*i)*cover
            
        for border in self.borders:
            Z *= border.function(X, Y)

        return Z
    
    def plot(self):

        x = np.linspace(0, self.lengthX, int(np.floor(self.lengthX/self.stepSize)))
        y = np.linspace(0, self.lengthY, int(np.floor(self.lengthY/self.stepSize)))
        X, Y = np.meshgrid(x, y)
        Z = self.computeField()
        
        scene = dict(
            xaxis = dict(title='Breite (x)', range = [0,max({self.lengthX, self.lengthY})]),
            yaxis = dict(title='Länge (y)', range = [0,max({self.lengthX, self.lengthY})]),
            zaxis = dict(title='Tiefe (z)', range = [-50,max({self.lengthX, self.lengthY})]))
        
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])
        
        fig.update_layout(title='Schrankfront Modell', scene=scene)
        fig.show()

        
def importGraph(path: str) -> graph:
    
    # Read file
    f = open(path)
    data = json.load(f)
    p = data["parameters"]
    t = data["textures"]
    
    # Create graph
    types: dict = {
        "bump": bump,
        "rings": rings,
        "bumpGrid": bumpGrid
    }
    
    g = graph(p["lengthX"], p["lengthY"], p["stepSize"])
    for texture in t:
        
        # params
        type = texture["type"]
        posX = texture["posX"]
        posY = texture["posY"]
        height = texture["height"]
        specialParam = texture["specialParam"]
        
        function = types[type]
        
        function = function(posX, posY, height, specialParam)
        
        g.textures.add(function)
        
    return g
    
def exportGraph(g: graph):
    parameters = {
            "lengthX": g.lengthX,
            "lengthY": g.lengthY,
            "stepSize": g.stepSize
        }
    
    
    textures = list()
    for function in g.textures:
        
        texture = {
            "type": function.__class__.__name__,
            "posX": function.posX,
            "posY": function.posY,
            "height": function.height,
            #"specialParam": factor[function.__class__]*function.specialParam
            "specialParam": function.specialParam
        }
        textures.append(texture)
    
#    borders = list()
  #  for function in g.borders:
  #      border = {
  #          "direction": function.direction,
  #          "distanceFromEdge": function.distanceFromEdge,
  #          "steepness": function.steepness
  #      }
    
    
    
    # create final structure
    output = dict()
    output["parameters"] = parameters
    output["textures"] = textures
    
    # export
    exportTime = datetime.now()
    exporttime = exportTime.strftime("%Y_%m_%d_%H:%M:%S")
    fileName = f"graphExport_{exporttime}.json"
    
    
    
    with open(fileName, "a") as exportFile:
        json.dump(output, exportFile)
        exportFile.close()
    
    
    
    
    
    
    
        
if __name__ == "__main__":
    
    front = graph(lengthX=50, lengthY=50, stepSize=0.1)
    cover = bump(posX = 25, posY =  25, factorX = 400, factorY = 400, height = 1)
    front.textures.add(rings(posX = 25, posY =  25, factorX = 4, factorY = 8, height = 10, cover=cover))
    front.plot()
