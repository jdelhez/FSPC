import os,sys
sys.path.append('examples')
import toolbox as tb
import gmsh

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

# SigmaVM a l'interface en y = 0.015 

SigmaVMNewtonAxiSym_0015 = list()
position = [0.005,0.015,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )
os.chdir('workspace/metafor')

time,directory = tb.readFiles()

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaVMNewtonAxiSym_0015.append(gmsh.model.mesh.getNode(tag)[0][0])
    xn=gmsh.model.mesh.getNode(1)[0]
    print(xn)

import numpy as np
np.savetxt("SigmaVMNewtonAxiSym_0015.txt",SigmaVMNewtonAxiSym_0015)
np.savetxt("time.txt",time)

# SigmaVM a l'interface en y = 0.03

SigmaVMNewtonAxiSym_003 = list()
position = [0.005,0.03,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )



tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaVMNewtonAxiSym_003.append(gmsh.model.mesh.getNode(tag)[0][0])

import numpy as np
np.savetxt("SigmaVMNewtonAxiSym_003.txt",SigmaVMNewtonAxiSym_003)

# SigmaVM a l'interface en y = 0.045

SigmaVMNewtonAxiSym_0045 = list()
position = [0.005,0.045,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaVMNewtonAxiSym_0045.append(gmsh.model.mesh.getNode(tag)[0][0])

import numpy as np
np.savetxt("SigmaVMNewtonAxiSym_0045.txt",SigmaVMNewtonAxiSym_0045)


# SigmaYY a l'interface en y = 0.015 

SigmaYYNewtonAxiSym_0015 = list()
position = [0.005,0.015,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )


tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaYYNewtonAxiSym_0015.append(gmsh.model.mesh.getNode(tag)[0][1])

import numpy as np
np.savetxt("SigmaYYNewtonAxiSym_0015.txt",SigmaYYNewtonAxiSym_0015)

# SigmaYY a l'interface en y = 0.03

SigmaYYNewtonAxiSym_003 = list()
position = [0.005,0.03,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaYYNewtonAxiSym_003.append(gmsh.model.mesh.getNode(tag)[0][1])

import numpy as np
np.savetxt("SigmaYYNewtonAxiSym_003.txt",SigmaYYNewtonAxiSym_003)

# SigmaVM a l'interface en y = 0.045

SigmaYYNewtonAxiSym_0045 = list()
position = [0.005,0.045,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaYYNewtonAxiSym_0045.append(gmsh.model.mesh.getNode(tag)[0][1])

import numpy as np
np.savetxt("SigmaYYNewtonAxiSym_0045.txt",SigmaYYNewtonAxiSym_0045)

# SigmaZZ a l'interface en y = 0.015 

SigmaZZNewtonAxiSym_0015 = list()
position = [0.005,0.015,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaZZNewtonAxiSym_0015.append(gmsh.model.mesh.getNode(tag)[0][2])

import numpy as np
np.savetxt("SigmaZZNewtonAxiSym_0015.txt",SigmaZZNewtonAxiSym_0015)

# SigmaZZ a l'interface en y = 0.03

SigmaZZNewtonAxiSym_003 = list()
position = [0.005,0.03,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaZZNewtonAxiSym_003.append(gmsh.model.mesh.getNode(tag)[0][2])

import numpy as np
np.savetxt("SigmaZZNewtonAxiSym_003.txt",SigmaZZNewtonAxiSym_003)

# SigmaZZ a l'interface en y = 0.045

SigmaZZNewtonAxiSym_0045 = list()
position = [0.005,0.045,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaZZNewtonAxiSym_0045.append(gmsh.model.mesh.getNode(tag)[0][2])

import numpy as np
np.savetxt("SigmaZZNewtonAxiSym_0045.txt",SigmaZZNewtonAxiSym_0045)

# SigmaXY a l'interface en y = 0.015 

SigmaXYNewtonAxiSym_0015 = list()
position = [0.005,0.015,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaXYNewtonAxiSym_0015.append(gmsh.model.mesh.getNode(tag)[0][3])

import numpy as np
np.savetxt("SigmaXYNewtonAxiSym_0015.txt",SigmaXYNewtonAxiSym_0015)

# SigmaXY a l'interface en y = 0.03

SigmaXYNewtonAxiSym_003 = list()
position = [0.005,0.03,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaVMNewtonAxiSym_003.append(gmsh.model.mesh.getNode(tag)[0][3])

import numpy as np
np.savetxt("SigmaXYNewtonAxiSym_003.txt",SigmaXYNewtonAxiSym_003)

# SigmaXY a l'interface en y = 0.045

SigmaXYNewtonAxiSym_0045 = list()
position = [0.005,0.045,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )

tag = tb.findNode(directory[0],position) # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 

for file in directory:

    gmsh.open(file)
    SigmaXYNewtonAxiSym_0045.append(gmsh.model.mesh.getNode(tag)[0][3])

import numpy as np
np.savetxt("SigmaXYNewtonAxiSym_0045.txt",SigmaXYNewtonAxiSym_0045)




