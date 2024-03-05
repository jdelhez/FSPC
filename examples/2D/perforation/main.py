import os.path as path
import numpy as np
import FSPC

# Input parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# Initialize the simulation

FSPC.setResMech(1e-7)
FSPC.setStep(2e-4,1e-9)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.KNN,1)
FSPC.setAlgo(FSPC.algorithm.ILS,25)

# Start the FSPC simulation

FSPC.general.simulate(10)
FSPC.general.printClock()
