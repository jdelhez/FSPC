import os.path as path
import numpy as np
import FSPC

# Path to the solver input files

path_F = path.dirname(__file__) + '/input_F.lua'
path_S = path.dirname(__file__) + '/input_S.py'

# Initialize the fluid and solid solvers

FSPC.set_mechanical_res(1e-6)
FSPC.set_time_step(5e-4, 1e-3)
FSPC.init_solver(path_F, path_S)

# Set the interpolator and algorithm

RBF = lambda r: np.square(r/0.01)*np.ma.log(r/0.01)
interpolator = FSPC.interpolator.RBF(RBF)
FSPC.set_interpolator(interpolator)

algorithm = FSPC.algorithm.MVJ(25)
FSPC.set_algorithm(algorithm)

# Start the FSI simulation

algorithm.simulate(0.4)
FSPC.general.print_clock()