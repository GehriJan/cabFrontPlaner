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
        
    
    def plot(self):
        
        x = np.linspace(0, self.lengthX, int(np.floor(self.lengthX/self.stepSize)))
        y = np.linspace(0, self.lengthY, int(np.floor(self.lengthY/self.stepSize)))
        X, Y = np.meshgrid(x, y)
        
        first = True
        for texture in self.textures:            
            if first == True:
                Z = texture.function(X, Y)
                first = False
            else:
                Z += texture.function(X, Y)
        
        for border in self.borders:
            Z *= border.function(X, Y)
        
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
    
    # factor = {
    #    bump: 1,
    #    rings: np.power(10,5),
    #    bumpGrid: (100/np.pi)
    #}
    
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
    front = graph(654, 780, 1)
    front.textures.add(bump(0.61*front.lengthX, 0.61*front.lengthY, 30, 20000))
    #front.textures.add(bump(0.61*0.39*front.lengthX, 0.61*0.39*front.lengthY, 15, 20000))
    front.textures.add(bump(0.61*0.7*front.lengthX, 0.61*0.7*front.lengthY, -25, 15000))
    
    #front.textures.add(rings(-1.5*front.lengthX, 0.5*front.lengthY, 5, 5000))
    #front.textures.add(rings(-1.5*front.lengthX, 1.5*front.lengthY, 15, 9000))
    front.textures.add(rings(-15*front.lengthX, 15*front.lengthY, 15, 9000))
    #front.textures.add(rings(2*front.lengthX, 2*front.lengthY, 10, 1000))
    #front.textures.add(bumpGrid(0.5*front.lengthX, 0.5*front.lengthY, 10, 700))
    #front.textures.add(bumpGrid(0.6*front.lengthX, 0.3*front.lengthY, 3, 1000))
    #front.textures.add(bumpGrid(0.9*front.lengthX, 0.1*front.lengthY, 12, 200))
    front.textures.add(bumpGrid(0.2*front.lengthX, 0.3*front.lengthY, 8, 700))
    #front.textures.add(bumpGrid(-0.5*front.lengthX, 0.4*front.lengthY, 6, 700))
    front.borders.add(smoothEdges("+x", 20, 0.5, front.lengthX, front.lengthY))
    # front = importGraph("export.json")
    #exportGraph(front)
    front.plot()
    