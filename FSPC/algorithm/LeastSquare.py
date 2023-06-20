from mpi4py.MPI import COMM_WORLD as CW
from .Algorithm import Algorithm
from .. import Toolbox as tb
from .. import Manager as mg
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Square

class ILS(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)

# %% Coupling at Each Time Step

    def couplingAlgo(self):

        verif = False
        self.iteration = 0
        self.resetConverg()

        if (CW.rank == 1) and mg.convMecha:

            self.VP = list()
            self.WP = list()

        if (CW.rank == 1) and mg.convTherm:

            self.VT = list()
            self.WT = list()

        while self.iteration < self.maxIter:

            # Transfer and fluid solver call

            self.transferDirichletSF()
            if CW.rank == 0: verif = mg.solver.run()
            verif = CW.scatter([verif,verif],root=0)
            if not verif: return False

            # Transfer and solid solver call

            self.transferNeumannFS()
            if CW.rank == 1: verif = mg.solver.run()
            verif = CW.scatter([verif,verif],root=1)
            if not verif: return False

            # Compute the coupling residual

            self.computeResidual()
            self.updateConverg()
            self.relaxation()
            
            # Check the coupling converence

            verif = self.verified()
            verif = CW.scatter([verif,verif],root=1)

            # End of the coupling iteration

            self.iteration += 1
            if verif: return True
            
        return False

# %% Relaxation of Solid Interface Displacement
    
    @tb.only_mecha
    def relaxationM(self):

        pos = mg.solver.getPosition()

        # Performs either BGS or IQN iteration

        if self.iteration == 0:
            mg.interp.pos += self.omega*self.resP

        else:

            self.VP.insert(0,np.hstack((self.resP-self.prevResP).T))
            self.WP.insert(0,np.hstack((pos-self.prevPos).T))

            # V and W are stored as transpose and list

            R = np.hstack(-self.resP.T)
            C = np.linalg.lstsq(np.transpose(self.VP),R,-1)[0]
            delta = np.dot(np.transpose(self.WP),C)-R
            delta = np.split(delta,mg.solver.dim)
            mg.interp.pos += np.transpose(delta)

        # Updates the residuals and displacement

        self.prevPos = np.copy(pos)
        self.prevResP = np.copy(self.resP)

# %% Relaxation of Solid Interface Temperature

    @tb.only_therm
    def relaxationT(self):

        temp = mg.solver.getTemperature()

        # Performs either BGS or IQN iteration

        if self.iteration == 0:
            mg.interp.temp += self.omega*self.resT

        else:

            self.VT.insert(0,np.hstack((self.resT-self.prevResT).T))
            self.WT.insert(0,np.hstack((temp-self.prevTemp).T))

            # V and W are stored as transpose and list

            R = np.hstack(-self.resT.T)
            C = np.linalg.lstsq(np.transpose(self.VT),R,-1)[0]
            delta = np.split(np.dot(np.transpose(self.WT),C)-R,1)
            mg.interp.temp += np.transpose(delta)

        # Updates the residuals and displacement

        self.prevTemp = np.copy(temp)
        self.prevResT = np.copy(self.resT)
