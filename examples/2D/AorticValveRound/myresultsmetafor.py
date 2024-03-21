import os,sys
sys.path.append('examples')
import toolbox as tb
import gmsh
import numpy as np

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

ValveX = list()
ValveY = list()
TimeL = list()

# Define here the range of files to be read

imin  = 1
imax  = 2500
di  = 10

# Define the position of the output
# position1 = [-0.01,0.00,0]
#position1 = [-0.003694403, 0,0]
position1 = [-0.0073888062, 0.00079238309,0]
os.chdir('workspace-New3s/metafor')

time,directory = tb.readFiles()

tag = tb.findNode(directory[0],position1)

# Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 


for i, file in enumerate(directory):
    if (imin <= i < imax) and ((i-imin) %  di)==0 :
        tag = tb.findNode(file,position1)

        gmsh.open(file)  
        X = gmsh.model.mesh.getNode(tag)[0][0]
        Y = gmsh.model.mesh.getNode(tag)[0][1]
        print("Time step",i)

        TimeL.append(time[i])
        ValveX.append(X)
        ValveY.append(Y)
    

#np.savetxt("../Time.txt",TimeL)
np.savetxt("../ValveX.txt",ValveX)
np.savetxt("../ValveY.txt",ValveY) 







