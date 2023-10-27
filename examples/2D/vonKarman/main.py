import os.path as path
import FSPC

# Input parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# Initialize the simulation 

FSPC.setConvMech(1e-6)
FSPC.setStep(1e-3,1e-2)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.ETM,9)
FSPC.setAlgo(FSPC.algorithm.MVJ,25)

# Start the FSPC simulation

FSPC.general.simulate(15)
FSPC.general.printClock()
