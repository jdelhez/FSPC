from .Algorithm import Algorithm
import numpy as np

# %% Block-Gauss Seidel with Aitken Dynamic Relaxation

class BGS_ADR(Algorithm):
    def __init__(self,solver):
        Algorithm.__init__(self,solver)

# %% Coupling at Each Time Step

    def couplingAlgo(self,com):

        verif = False
        self.iteration = 0
        timeFrame = self.step.timeFrame()
        self.resetConverg()

        while True:

            # Transfer and fluid solver call

            self.transferDirSF(com)
            if com.rank == 0: verif = self.solver.run(*timeFrame)
            verif = com.scatter([verif,verif],root=0)
            if not verif: return False
                
            # Transfer and solid solver call

            self.transferNeuFS(com)
            if com.rank == 1: verif = self.solver.run(*timeFrame)
            verif = com.scatter([verif,verif],root=1)
            if not verif: return False

            # Compute the coupling residual

            if com.rank == 1:
                
                self.computeResidual()
                self.updateConverg()
                self.relaxation()

            # Check the converence of the FSI

            if com.rank == 1: verif = self.isVerified()
            verif = com.scatter([verif,verif],root=1)

            # End of the coupling iteration

            if verif: break
            self.iteration += 1
            if self.iteration > self.maxIter: return False
        
        return True

# %% Relaxation of Solid Interface Displacement

    def relaxationM(self):

        if self.aitken: correction = self.getOmegaM()*self.resDisp
        else: correction = self.omega*self.resDisp
        self.interp.disp += correction

    # Compute omega with Aitken relaxation

    def getOmegaM(self):

        if self.iteration == 0:
            self.omegaM = self.omega

        else:

            dRes = self.resDisp-self.prevResDisp
            prodRes = np.sum(dRes*self.prevResDisp)
            dResNormSqr = np.sum(np.linalg.norm(dRes,axis=0)**2)
            if dResNormSqr != 0: self.omegaM *= -prodRes/dResNormSqr
            else: self.omegaM = 0

        # Changes omega if out of the range

        self.omegaM = min(self.omegaM,1)
        self.omegaM = max(self.omegaM,0)
        self.prevResDisp = self.resDisp.copy()
        return self.omegaM

# %% Relaxation of Solid Interface Temperature

    def relaxationT(self):

        if self.aitken: correction = self.getOmegaT()*self.resTemp
        else: correction = self.omega*self.resTemp
        self.interp.temp += correction

    # Compute omega with Aitken relaxation

    def getOmegaT(self):

        if self.iteration == 0:
            self.omegaT = self.omega

        else:

            dRes = self.resTemp-self.prevResTemp
            prodRes = np.sum(dRes*self.prevResTemp)
            dResNormSqr = np.sum(np.linalg.norm(dRes,axis=0)**2)
            if dResNormSqr != 0: self.omegaT *= -prodRes/dResNormSqr
            else: self.omegaT = 0

        # Changes omega if out of the range

        self.omegaT = min(self.omegaT,1)
        self.omegaT = max(self.omegaT,0)
        self.prevResTemp = self.resTemp.copy()
        return self.omegaT