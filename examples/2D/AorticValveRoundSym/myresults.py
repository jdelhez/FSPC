import os,sys
sys.path.append('examples')
import toolbox as tb
import gmsh
import numpy as np

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

# SigmaVM a l'interface en y = 0.015 

ValveX = list()
ValveY = list()

position1 = [-0.0074925,0.000564906,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

os.chdir('workspace_AorticR_1/metafor')

time,directory = tb.readFiles()

tag = tb.findNode(directory[0],position1)


 # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 


for i, file in enumerate(directory):

    gmsh.open(file)
    
    X = gmsh.model.mesh.getNode(tag)[0][0]
    Y = gmsh.model.mesh.getNode(tag)[0][1]
    ValveX.append(X)
    ValveY.append(Y)
    
    

    
np.savetxt("../time.txt",time)

np.savetxt("../ValveX.txt",ValveX)
np.savetxt("../ValveY.txt",ValveY)








