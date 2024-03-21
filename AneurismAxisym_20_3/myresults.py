import os,sys
sys.path.append('examples')
import toolbox as tb
import gmsh
import numpy as np

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

# SigmaVM a l'interface en y = 0.015 

SigmaVMNewtonAxiSym_0015 = list()
SigmaVMNewtonAxiSym_0030 = list()
SigmaVMNewtonAxiSym_0045 = list()

SigmaYYNewtonAxiSym_0015 = list()
SigmaYYNewtonAxiSym_0030 = list()
SigmaYYNewtonAxiSym_0045 = list()

SigmaZZNewtonAxiSym_0015 = list()
SigmaZZNewtonAxiSym_0030 = list()
SigmaZZNewtonAxiSym_0045 = list()

SigmaXYNewtonAxiSym_0015 = list()
SigmaXYNewtonAxiSym_0030 = list()
SigmaXYNewtonAxiSym_0045 = list()

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
    
    SigmaVMNewtonAxiSym_0015.append(VMS[tag1-1][0])
    SigmaVMNewtonAxiSym_0030.append(VMS[tag2-1][0])
    SigmaVMNewtonAxiSym_0045.append(VMS[tag3-1][0])
    
    SigmaYYNewtonAxiSym_0015.append(SYY[tag1-1][0])
    SigmaYYNewtonAxiSym_0030.append(SYY[tag2-1][0])
    SigmaYYNewtonAxiSym_0045.append(SYY[tag3-1][0])

    SigmaZZNewtonAxiSym_0015.append(SZZ[tag1-1][0])
    SigmaZZNewtonAxiSym_0030.append(SZZ[tag2-1][0])
    SigmaZZNewtonAxiSym_0045.append(SZZ[tag3-1][0])

    SigmaXYNewtonAxiSym_0015.append(SXY[tag1-1][0])
    SigmaXYNewtonAxiSym_0030.append(SXY[tag2-1][0])
    SigmaXYNewtonAxiSym_0045.append(SXY[tag3-1][0])

    
np.savetxt("../time.txt",time)
np.savetxt("../SigmaVMNewtonAxiSym_0015.txt",SigmaVMNewtonAxiSym_0015)
np.savetxt("../SigmaVMNewtonAxiSym_0030.txt",SigmaVMNewtonAxiSym_0030)
np.savetxt("../SigmaVMNewtonAxiSym_0045.txt",SigmaVMNewtonAxiSym_0045)

np.savetxt("../SigmaYYNewtonAxiSym_0015.txt",SigmaYYNewtonAxiSym_0015)
np.savetxt("../SigmaYYNewtonAxiSym_0030.txt",SigmaYYNewtonAxiSym_0030)
np.savetxt("../SigmaYYNewtonAxiSym_0045.txt",SigmaYYNewtonAxiSym_0045)

np.savetxt("../SigmaZZNewtonAxiSym_0015.txt",SigmaZZNewtonAxiSym_0015)
np.savetxt("../SigmaZZNewtonAxiSym_0030.txt",SigmaZZNewtonAxiSym_0030)
np.savetxt("../SigmaZZNewtonAxiSym_0045.txt",SigmaZZNewtonAxiSym_0045)

np.savetxt("../SigmaXYNewtonAxiSym_0015.txt",SigmaXYNewtonAxiSym_0015)
np.savetxt("../SigmaXYNewtonAxiSym_0030.txt",SigmaXYNewtonAxiSym_0030)
np.savetxt("../SigmaXYNewtonAxiSym_0045.txt",SigmaXYNewtonAxiSym_0045)







