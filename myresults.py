import os,sys
sys.path.append('examples')
import toolbox as tb
import gmsh
import numpy as np

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

# SigmaVM a l'interface en y = 0.015 

Time= list()
XWall1 = list()
SigmaVM1 = list()
SigmaYY1 = list()
SigmaZZ1 = list()
SigmaXY1 = list()
SigmaXX1 = list()

XWall2 = list()
SigmaVM2 = list()
SigmaYY2 = list()
SigmaZZ2 = list()
SigmaXY2 = list()
SigmaXX2 = list()

XWall3 = list()
SigmaVM3 = list()
SigmaYY3 = list()
SigmaZZ3 = list()
SigmaXY3 = list()
SigmaXX3 = list()

position1 = [0.01,-0.03,0] 
position2 = [0.01,0.0,0] 
position3 = [0.01,-0.03,0] 
os.chdir('./workspace/metafor')

time,directory = tb.read_files()

tag1 = tb.find_node(directory[0],position1)
tag2 = tb.find_node(directory[0],position2)
tag3 = tb.find_node(directory[0],position3)

# Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 


for i, file in enumerate(directory):

    gmsh.open(file)
    print(file)
    X = gmsh.model.mesh.getNode(tag1)[0][0] 

    VMS = gmsh.view.getModelData(0,i)[2]
    SYY = gmsh.view.getModelData(1,i)[2]
    SZZ = gmsh.view.getModelData(2,i)[2]
    SXY = gmsh.view.getModelData(3,i)[2]
    SXX = gmsh.view.getModelData(4,i)[2]
    
    XWall1.append(X)
    SigmaVM1.append(VMS[tag1-1][0])
    SigmaYY1.append(SYY[tag1-1][0])
    SigmaZZ1.append(SZZ[tag1-1][0])
    SigmaXY1.append(SXY[tag1-1][0])
    SigmaXX1.append(SXX[tag1-1][0])
    
    X = gmsh.model.mesh.getNode(tag2)[0][0] 

    VMS = gmsh.view.getModelData(0,i)[2]
    SYY = gmsh.view.getModelData(1,i)[2]
    SZZ = gmsh.view.getModelData(2,i)[2]
    SXY = gmsh.view.getModelData(3,i)[2]
    SXX = gmsh.view.getModelData(4,i)[2]
    
    XWall2.append(X)
    SigmaVM2.append(VMS[tag2-1][0])
    SigmaYY2.append(SYY[tag2-1][0])
    SigmaZZ2.append(SZZ[tag2-1][0])
    SigmaXY2.append(SXY[tag2-1][0])
    SigmaXX2.append(SXX[tag2-1][0])
    
    X = gmsh.model.mesh.getNode(tag3)[0][0] 

    VMS = gmsh.view.getModelData(0,i)[2]
    SYY = gmsh.view.getModelData(1,i)[2]
    SZZ = gmsh.view.getModelData(2,i)[2]
    SXY = gmsh.view.getModelData(3,i)[2]
    SXX = gmsh.view.getModelData(4,i)[2]
    
    XWall3.append(X)
    SigmaVM3.append(VMS[tag3-1][0])
    SigmaYY3.append(SYY[tag3-1][0])
    SigmaZZ3.append(SZZ[tag3-1][0])
    SigmaXY3.append(SXY[tag3-1][0])
    SigmaXX3.append(SXX[tag3-1][0])
    

Data=[time,XWall1,SigmaVM1,SigmaXX1,SigmaYY1,SigmaZZ1,SigmaXY1,XWall2,SigmaVM2,SigmaXX2,SigmaYY2,SigmaZZ2,SigmaXY2,XWall3,SigmaVM3,SigmaXX3,SigmaYY3,SigmaZZ3,SigmaXY3]
DataA = np.asarray(Data).T

np.savetxt("../MetaforResu.txt",DataA)



