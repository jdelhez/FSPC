import os,sys
sys.path.append('examples')
import toolbox as tb
import gmsh
import numpy as np

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

Velocity = list()

#position1 = [-0.007388806, 0,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )
position1 = [0,0,0]

os.chdir('workspace/pfem')

time,directory = tb.readFiles()

tag = tb.findNode(directory[0],position1)


# Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 


for i, file in enumerate(directory):

    gmsh.open(file)
    
    print(file)
    vel = gmsh.view.getModelData(1,i)[2]
    Velocity.append(vel[tag][0])

         
np.savetxt("../time.txt",time)

np.savetxt("../Velocity.txt",Velocity)








