import os.path as path
import numpy as np
import FSPC

# Path to the solver input files

path_F = path.dirname(__file__)+'/inputF.lua'
path_S = path.dirname(__file__)+'/inputS.py'
FSPC.init_solver(path_F, path_S)

# Pour limiter le nombre de pas de temps PFEM3D entre 2 appels de FSPC
# from mpi4py.MPI import COMM_WORLD as CW
# if CW.rank == 0: solver.max_division = 1

# Set the coupling algorithm

algorithm = FSPC.algorithm.MVJ(25)
FSPC.set_algorithm(algorithm)

# Set the interface interpolator

RBF = lambda r: np.square(r/0.005)*np.ma.log(r/0.005)
interpolator = FSPC.interpolator.RBF(RBF)
FSPC.set_interpolator(interpolator)

# Set the time step manager

step = FSPC.general.TimeStep(5e-4, 5e-3)
FSPC.set_time_step(step)

# Set the convergence manager

residual = FSPC.general.Residual(1e-6)
FSPC.set_mechanical_res(residual)

# Start the FSI simulation

algorithm.simulate(2)
FSPC.general.print_clock()