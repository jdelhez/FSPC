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
XWall = list()
SigmaVM = list()
SigmaYY = list()
SigmaZZ = list()
SigmaXY = list()
SigmaXX = list()

position = [0.01,0.0,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )
os.chdir('workspace/metafor')

time,directory = tb.read_files()

tag = tb.find_node(directory[0],position)

# Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 


for i, file in enumerate(directory):

    gmsh.open(file)
    print(file)
    X = gmsh.model.mesh.getNode(tag)[0][0] 

    VMS = gmsh.view.getModelData(0,i)[2]
    SYY = gmsh.view.getModelData(1,i)[2]
    SZZ = gmsh.view.getModelData(2,i)[2]
    SXY = gmsh.view.getModelData(3,i)[2]
    SXX = gmsh.view.getModelData(4,i)[2]
    
    XWall.append(X)
    SigmaVM.append(VMS[tag-1][0])
    SigmaYY.append(SYY[tag-1][0])
    SigmaZZ.append(SZZ[tag-1][0])
    SigmaXY.append(SXY[tag-1][0])
    SigmaXX.append(SXX[tag-1][0])
    

Data=[time,XWall,SigmaVM,SigmaXX,SigmaYY,SigmaZZ,SigmaXY]
DataA = np.asarray(Data).T

np.savetxt("../MetaforResu.txt",DataA)



