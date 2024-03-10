import os.path as path
import numpy as np
import FSPC

# FSPC en 5 étapes
# [1] On prédit un déplacemeent solide
# [2] On lance PFEM3D sous cette condition, on obtient une contrainte de surface
# [3] On lance Metafor sous cette condition, on obtient un déplacement
# [4] On compare le déplacement prédit en [1] et celui obtenu en [4] => résidu
# [5] Si résidu > tolerance, on update le déplacement prédit avec un algo au choix (*), on
# revient en arrière et on recommmence. Si résidu < tolerance, on passe au pas de temps suivant

R = 0.005 # Rayon pour la RBF, entre 1 et 20x la taille carac du mesh solide ou fluide
RBF = lambda r: np.square(r/R)*np.ma.log(r/R) # Une RBF qui fonctionne bien (**)
pathF = path.dirname(__file__)+'/inputF.lua' # = Dossier_courrant/inputF.lua
pathS = path.dirname(__file__)+'/inputS.py' # Chemin vers inputS.lua


FSPC.setResMech(1e-6) # Tolerance plus petite ou égale à minRes PFEM3D/Metafor
# FSPC.setStep(1e-2,25e-3) # Time step, time between writing
FSPC.setStep(1e-4,12e-4) # Time step, time between writing
FSPC.setSolver(pathF,pathS)

# (FSPC.interpolator.KNN,1) Si même nombre de noeuds pour l'interface fluide et solide.
# (FSPC.interpolator.KNN,2) Ok si les maillages son non conformes en 2D.
# (FSPC.interpolator.RBF,RBF) OK (**) dans 99% des cas, plus long à calculer
FSPC.setInterp(FSPC.interpolator.RBF,RBF) # Interpolation des données PFEM <=> Metafor

# Algo de prédiction FSI = g(û-u) dans les slides
# BGS = Block gauss seidel le moins bon mais le plus simple
# ILS = Interface quasi newton with inverse least square
# MVJ = le ILS mais avec mémoire du pas de temps prévcédent, utile si le pas de temps ne change pas trop.
FSPC.setAlgo(FSPC.algorithm.MVJ,25) # algo (*), nombre max d'itérations


# Start the FSPC simulation

# FSPC.general.simulate(1.3) # Run 1.3 seconde
FSPC.general.simulate(0.03) 
FSPC.general.printClock() # Print time stats