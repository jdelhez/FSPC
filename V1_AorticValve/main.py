import os.path as path
import numpy as np
import FSPC

# Path to the solver input files

path_F = path.dirname(__file__)+'/inputF.lua'
path_S = path.dirname(__file__)+'/inputS.py'
solver = FSPC.init_solver(path_F, path_S)

# Force FSPC time step to be the same as PFEM3D

if FSPC.CW.rank == 0: solver.max_division = 1

# Set the coupling algorithm

algorithm = FSPC.algorithm.MVJ(10)
FSPC.set_algorithm(algorithm)

# Set the interface interpolator

RBF = lambda r: np.square(r/1e-3)*np.ma.log(r/1e-3)
interpolator = FSPC.interpolator.RBF(RBF)
FSPC.set_interpolator(interpolator)

# Set the time step manager

step = FSPC.general.TimeStep(1e-4, 1e-3)
FSPC.set_time_step(step)

# Set the convergence manager

residual = FSPC.general.Residual(1e-6)
FSPC.set_mechanical_res(residual)

# Start the FSI simulation

algorithm.simulate(3)
FSPC.general.print_clock()