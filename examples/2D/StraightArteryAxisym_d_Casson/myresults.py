import os,sys
sys.path.append('examples')
import toolbox as tb
import gmsh
import numpy as np

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

# SigmaVM a l'interface en y = 0.015 

SigmaVMCassonAxiSym_0015 = list()
SigmaVMCassonAxiSym_0030 = list()
SigmaVMCassonAxiSym_0045 = list()

SigmaYYCassonAxiSym_0015 = list()
SigmaYYCassonAxiSym_0030 = list()
SigmaYYCassonAxiSym_0045 = list()

SigmaZZCassonAxiSym_0015 = list()
SigmaZZCassonAxiSym_0030 = list()
SigmaZZCassonAxiSym_0045 = list()

SigmaXYCassonAxiSym_0015 = list()
SigmaXYCassonAxiSym_0030 = list()
SigmaXYCassonAxiSym_0045 = list()

position1 = [0.005,0.015,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )
position2 = [0.005,0.030,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )
position3 = [0.005,0.045,0] # a l'interface dans un premier temps (sinon créer un groupe avec des points tout le long de là où veut? )
os.chdir('workspace/metafor')

time,directory = tb.readFiles()

tag1 = tb.findNode(directory[0],position1)
tag2 = tb.findNode(directory[0],position2)
tag3 = tb.findNode(directory[0],position3)

 # Mettre dans la boucle si on veut pas que ca change la position 
# Position du noeud le plus proche de position 


for i, file in enumerate(directory):

    gmsh.open(file)
    
    VMS = gmsh.view.getModelData(0,i)[2]
    SYY = gmsh.view.getModelData(1,i)[2]
    SZZ = gmsh.view.getModelData(2,i)[2]
    SXY = gmsh.view.getModelData(3,i)[2]
    
    SigmaVMCassonAxiSym_0015.append(VMS[tag1-1][0])
    SigmaVMCassonAxiSym_0030.append(VMS[tag2-1][0])
    SigmaVMCassonAxiSym_0045.append(VMS[tag3-1][0])
    
    SigmaYYCassonAxiSym_0015.append(SYY[tag1-1][0])
    SigmaYYCassonAxiSym_0030.append(SYY[tag2-1][0])
    SigmaYYCassonAxiSym_0045.append(SYY[tag3-1][0])

    SigmaZZCassonAxiSym_0015.append(SZZ[tag1-1][0])
    SigmaZZCassonAxiSym_0030.append(SZZ[tag2-1][0])
    SigmaZZCassonAxiSym_0045.append(SZZ[tag3-1][0])

    SigmaXYCassonAxiSym_0015.append(SXY[tag1-1][0])
    SigmaXYCassonAxiSym_0030.append(SXY[tag2-1][0])
    SigmaXYCassonAxiSym_0045.append(SXY[tag3-1][0])

    
np.savetxt("../time.txt",time)
np.savetxt("../SigmaVMCassonAxiSym_0015.txt",SigmaVMCassonAxiSym_0015)
np.savetxt("../SigmaVMCassonAxiSym_0030.txt",SigmaVMCassonAxiSym_0030)
np.savetxt("../SigmaVMCassonAxiSym_0045.txt",SigmaVMCassonAxiSym_0045)

np.savetxt("../SigmaYYCassonAxiSym_0015.txt",SigmaYYCassonAxiSym_0015)
np.savetxt("../SigmaYYCassonAxiSym_0030.txt",SigmaYYCassonAxiSym_0030)
np.savetxt("../SigmaYYCassonAxiSym_0045.txt",SigmaYYCassonAxiSym_0045)

np.savetxt("../SigmaZZCassonAxiSym_0015.txt",SigmaZZCassonAxiSym_0015)
np.savetxt("../SigmaZZCassonAxiSym_0030.txt",SigmaZZCassonAxiSym_0030)
np.savetxt("../SigmaZZCassonAxiSym_0045.txt",SigmaZZCassonAxiSym_0045)

np.savetxt("../SigmaXYCassonAxiSym_0015.txt",SigmaXYCassonAxiSym_0015)
np.savetxt("../SigmaXYCassonAxiSym_0030.txt",SigmaXYCassonAxiSym_0030)
np.savetxt("../SigmaXYCassonAxiSym_0045.txt",SigmaXYCassonAxiSym_0045)







