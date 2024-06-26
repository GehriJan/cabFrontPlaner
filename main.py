import plotly.graph_objects as go
import numpy as np
import json
import random
import math
from datetime import datetime
from functions import *




class graph():
    
    def __init__(self, lengthX, lengthY, stepSize, niveaus: tuple) -> None:
        self.lengthX = lengthX
        self.lengthY = lengthY
        self.stepSize = stepSize
        
        self.minHeight = niveaus[0]-niveaus[1]
        self.normalNiveau = niveaus[1]
        self.maxHeight = niveaus[2]-niveaus[1]
        
        self.textures = set()
        self.borders = set()
        
        self.Z = None
        
    
    def computeBasicField(self):
        x = np.linspace(0, self.lengthX, int(np.floor(self.lengthX/self.stepSize)))
        y = np.linspace(0, self.lengthY, int(np.floor(self.lengthY/self.stepSize)))
        X, Y = np.meshgrid(x, y)
        Z = 0*X*Y
        
        # Sum up all the specified textures
        for i in {-1, 0, 1}:
            for texture in self.textures:
                cover = texture.cover.function(X,Y+self.lengthY*i) if hasattr(texture, "cover") and texture.cover != None else np.power(X, 0)*np.power(Y, 0)
                Z += texture.function(X,Y+self.lengthY*i)*cover
        
        # Flattening the borders           
        for border in self.borders:
            Z *= border.function(X, Y)
        
        self.Z = Z
    def compressAndRaise(self):
        Z = self.Z
        
        # Compress to min/max Height
        minO = np.min(Z)
        maxO = np.max(Z)
        minN = self.minHeight
        maxN = self.maxHeight
        
        a = (minN*maxO-maxN*minO)/(minO*minO*maxO-maxO*maxO*minO)
        b = (maxN*minO*minO-minN*maxO*maxO)/(maxO*minO*minO-minO*maxO*maxO)
        
        Z = a*np.square(Z)+b*Z
                
        # Raise to normalNiveau        
        Z += self.normalNiveau
        
        self.Z = Z
    
    
    def plot(self):

        x = np.linspace(0, self.lengthX, int(np.floor(self.lengthX/self.stepSize)))
        y = np.linspace(0, self.lengthY, int(np.floor(self.lengthY/self.stepSize)))
        X, Y = np.meshgrid(x, y)
        self.computeBasicField()
        self.compressAndRaise()
        Z = self.Z
        
        scene = dict(
            xaxis = dict(title='Breite (x)', range = [0,max({self.lengthX, self.lengthY})]),
            yaxis = dict(title='Länge (y)', range = [0,max({self.lengthX, self.lengthY})]),
            zaxis = dict(title='Tiefe (z)', range = [-50,max({self.lengthX, self.lengthY})]))
        
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])
        
        title = f"SideTableSurfaceModel\n\tMin:{np.min(Z).round(2)} Max:{np.max(Z).round(2)}\tStringlength: {len(self.exportAutodesk())}"
        fig.update_layout(title=title, scene=scene)
        fig.show()

    def exportAutodesk(self):
        output: str = ""
        
        # Texturen hinzufügen
        for i in {-1, 0, 1}:
            for texture in self.textures:
                output += f"+{texture.exportAutodesk()})"
                
                values = {
                    "height": f"{texture.height}",
                    "posX": f"{texture.posX}",
                    "posY": f"{texture.posY+i*self.lengthY}",
                    "factorX": f"{texture.factorX}",
                    "factorY": f"{texture.factorY}"
                }
                
                for text in values:
                    output = output.replace(text, values[text])
        
        # Flatten borders        
        for border in self.borders:
            output = f"{border.exportAutodesk()}*({output})"
        
        # compress
        self.computeBasicField()
        
        #minO = np.min(self.Z)
        
        
        #extrema = {
        #    "minO": str(np.round(np.min(self.Z),2)),
        #    "maxO": str(np.round(np.max(self.Z),2)),
        #    "minN": str(self.minHeight),
        #    "maxN": str(self.maxHeight),
        #}
        
        #output = f"(minN*maxO-maxN*minO)/(minO*minO*maxO-maxO*maxO*minO)*pow({output},2)+(maxN*minO*minO-minN*maxO*maxO)/(maxO*minO*minO-minO*maxO*maxO)*{output}"

        #for key, value in extrema.items():
        #    output = output.replace(key, value)
        
        
        minO = np.min(self.Z)
        maxO = np.max(self.Z)
        minN = self.minHeight
        maxN = self.maxHeight
        a = np.round((minN*maxO-maxN*minO)/(minO*minO*maxO-maxO*maxO*minO), 5)
        b = np.round((maxN*minO*minO-minN*maxO*maxO)/(maxO*minO*minO-minO*maxO*maxO), 5)
        
        output = f"{a}*pow({output},2)+{b}*{output}"
        
        # Raising
        output = f"{output}+{self.normalNiveau}"
        
        replacements = {
            "--": "+"          
        }
          
        for text in replacements:
            output = output.replace(text, replacements[text]) 

        
        return output
                
        
        
            
        
        

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
    
    # Graph initialisieren
    front = graph(lengthX=600, lengthY=3.1415926534*(460+10+30), stepSize=5, niveaus=(20, 30, 50))
    
    
    # Bumps
    #front.textures.add(bump(350, 1350, 200, 80, 20))
    #front.textures.add(bump(400, 240, 100, 70, -10))
    #front.textures.add(bump(560, 240, 80, 50, 15))
    
    #front.textures.add(bump(100, 0.45*front.lengthY, 40, 60, -15))
    #front.textures.add(bump(100, 0.55*front.lengthY, 30, 55, 15))
    '''
    print("bumpList = [")
    for i in range(20):

        posX = random.randrange(math.ceil(1.3*front.lengthX))
        posY = random.randrange(math.ceil(1.3*front.lengthY))
        factorX = random.randrange(50, 150)
        factorY = random.randrange(50, 150)
        height = random.randrange(10,20)
        
        front.textures.add(bump(posX, posY, factorX, factorY, height))
        print(f"\tbump({posX}, {posY}, {factorX}, {factorY}, {height}),")
    print("]")
    '''
    # Rings
    cover1 = bump(0.7*front.lengthX, 0.5*front.lengthY, 100, 370, 1)
    front.textures.add(rings(0.3*front.lengthX, 0.5*front.lengthY, 100, 220, 20, cover1))
    cover2 = bump(0.3*front.lengthX, 0*front.lengthY, 100, 370, 1)
    front.textures.add(rings(0.7*front.lengthX, 0*front.lengthY, 100, 220, 20, cover2))
    #cover2 = bump(150, 250, 120, 120, 1)
    #front.textures.add(rings(150, 250, 70, 70, 13, cover2))
    #cover3 = bump(100,1500,50, 50, 1)
    #front.textures.add(rings(100,1500,40,40,10, cover3))

    #cover5 = bump()
    #front.textures.add(rings(350, 1350, ))
    # Bumpgrids
    #cover4 = bump(430,1530,100, 100, 1)
    #front.textures.add(bumpGrid(430, 1530, 100, 100, 20, cover4))
        
    
    # Kanten
    front.borders.add(smoothEdges("-x", 30, 0.25, 1, front.lengthX, front.lengthY))
    front.borders.add(smoothEdges("+x", 30, 0.25, 1, front.lengthX, front.lengthY))
    print(f"Exportlength: {len(front.exportAutodesk())} characters.")
    print(front.exportAutodesk().replace("y", "200"))
    front.plot()
    
   # print(front.exportAutodesk())
