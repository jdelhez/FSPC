import os.path as path
import numpy as np
import FSPC

# %% Paths to the input files

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# %% Fluid Structure Coupling

process = FSPC.Process()
solver = process.getSolver(pathF,pathS)
RBF = lambda r: np.square(r)*np.ma.log(r)

# Configure the algorithm

algorithm = FSPC.IQN_MVJ(solver)
algorithm.interp = FSPC.RBF(solver,RBF)
algorithm.convergM = FSPC.Convergence(1e-8)
algorithm.step = FSPC.TimeStep(1e-3)

algorithm.endTime = 1
algorithm.omega = 0.5
algorithm.maxIter = 25
algorithm.dtWrite = 1e-2

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()