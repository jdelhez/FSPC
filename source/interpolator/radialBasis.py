from .interpolator import Interpolator
from scipy import linalg
import numpy as np

# %% Energy Conservative Radial Basis Function

class EC_RBF(Interpolator):
    def __init__(self,input,com):
        Interpolator.__init__(self,input,com)

        # Initialize the FS interpolation matrix

        if com.rank == 0:

            positionS = np.zeros((self.recvNode,self.dim))
            positionF = self.solver.getPosition()
            com.Recv(positionS,source=1)

            # Compute A,B and send their transpose to Solid

            A = self.computeMappingF(positionS,positionF)
            com.send(np.transpose(self.B),dest=1)
            com.send(np.transpose(A),dest=1)
            self.LU = linalg.lu_factor(A)

        if com.rank == 1:

            self.B = None
            com.Send(self.solver.getPosition(),dest=0)
            self.B = com.recv(self.B,source=0)

            # Precompute the LU decomposition for solve

            A = None
            A = com.recv(A,source=0)
            self.LU = linalg.lu_factor(A)

# %% Mapping matrix from Solid to Fluid

    def computeMappingF(self,positionS,positionF):

        size = self.recvNode+self.dim+1
        self.B = np.ones((self.nbrNode,size))
        A = np.ones((size,size))

        # Fill the matrices A,B with raw positions

        self.B[:,(self.recvNode+1):] = positionF
        A[(self.recvNode+1):,:self.recvNode] = positionS.T
        A[:self.recvNode,(self.recvNode+1):] = positionS

        # Fill the matrices A,B using the basis function

        for i in range(self.recvNode):
            
            r = np.linalg.norm(positionS[i]-positionS,axis=1)
            A[i,:self.recvNode] = self.phiTPS(r)

            r = np.linalg.norm(positionF-positionS[i],axis=1)
            self.B[:,i] = self.phiTPS(r)

        return A

# %% Interpolate recvData and return the result

    def interpDataSF(self,recvData):

        zero = np.zeros((self.dim+1,self.dim))
        recvData = np.append(recvData,zero,axis=0)
        recvData = linalg.lu_solve(self.LU,recvData)
        return self.B.dot(recvData)

    def interpDataFS(self,recvData):
        
        recvData = self.B.dot(recvData)
        recvData = linalg.lu_solve(self.LU,recvData)
        return recvData[:self.nbrNode]

# %% Thin Plate Spline Function

    def phiTPS(self,dist):
        return (dist*dist)*np.ma.log10(dist)