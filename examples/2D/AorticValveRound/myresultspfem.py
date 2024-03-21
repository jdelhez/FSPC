import os,sys
sys.path.append('examples')
import toolbox as tb
import gmsh
import numpy as np

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

Velocity = list()
Pressure = list()
ValveX = list()
ValveY = list()
TimeL = list()

# Define here the range of files to be read

imin  = 1
imax  = 2500
di  = 10

# Define the position of the output
# position1 = [-0.01,0.00,0]
position1 = [-0.003694403, 0,0]
position2 = [-0.043, 0,0]
os.chdir('workspace-New3s/pfem')

time,directory = tb.readFiles()

tag = tb.findNode(directory[0],position1)
tag2 = tb.findNode(directory[0],position2)

# Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 


for i, file in enumerate(directory):
    if (imin <= i < imax) and ((i-imin) %  di)==0 :
        tag = tb.findNode(file,position1)

        gmsh.open(file)  
        X = gmsh.model.mesh.getNode(tag)[0][0]
        Y = gmsh.model.mesh.getNode(tag)[0][1]
        print("Time step",i)

        pression = gmsh.view.getModelData(0,i)[2]
        velocity = gmsh.view.getModelData(1,i)[2]
       

        Velocity.append(velocity[tag])
        Pressure.append(pression[tag2])
        TimeL.append(time[i])
       

np.savetxt("../Time.txt",TimeL)
np.savetxt("../Velocity.txt",Velocity)
np.savetxt("../Pressure.txt",Pressure)








