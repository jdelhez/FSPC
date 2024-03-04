from ..general import Toolbox as tb
import importlib.util as util
import numpy as np
import wrap as w
import sys

# |-----------------------------------|
# |   Initializes the Solid Wraper    |
# |-----------------------------------|

class Metafor(object):
    def __init__(self,path):
        
        # Convert Metafor into a module

        parm = dict()
        spec = util.spec_from_file_location('module.name',path)
        module = util.module_from_spec(spec)
        sys.modules['module.name'] = module
        spec.loader.exec_module(module)

        # Actually initialize Metafor from file

        self.metafor = module.getMetafor(parm)
        self.geometry = self.metafor.getDomain().getGeometry()
        self.dim = self.geometry.getDimension().getNdim()
        self.tsm = self.metafor.getTimeStepManager()

        # Sets the dimension of the interaction

        if self.dim == 2: self.axis = (w.TX,w.TY)
        if self.dim == 3: self.axis = (w.TX,w.TY,w.TZ)

        # Defines some internal variables

        self.FSI = parm['FSInterface']
        self.exporter = parm['exporter']
        self.polytope = parm['polytope']
        self.rupture = parm['rupture']

        # Mechanical and thermal interactions

        if 'interacM' in parm:
            self.interacM = np.atleast_1d(parm['interacM'])

        if 'interacT' in parm:
            self.interacT = np.atleast_1d(parm['interacT'])

        # Create the memory fac used to restart

        self.mfac = w.MemoryFac()
        self.metaFac = w.MetaFac(self.metafor)
        self.metaFac.mode(False,False,True)
        self.metaFac.save(self.mfac)

        # Initialize the integration and restart

        self.maxDivision = 200
        self.tsm.setInitialTime(0,np.inf)

# |--------------------------------------------|
# |   Run Metafor in the Current Time Frame    |
# |--------------------------------------------|
    
    @tb.write_logs
    @tb.compute_time
    def run(self):

        self.tsm.setNextTime(tb.Step.nexTime(),0,tb.Step.dt)
        self.tsm.setMinimumTimeStep(tb.Step.dt/self.maxDivision)
        return self.metafor.getTimeIntegration().restart(self.mfac)

# |----------------------------------|
# |   Neumann Boundary Conditions    |
# |----------------------------------|

    def applyLoading(self,load):

        P = self.getPosition()
        for i in range(len(load)): # TEST GAUSSIAN LOAD

            x = P[i][0]
            L = -1.2e7*np.exp(-np.power(x/0.5,2))
            load[i] = [0,L,0]


        for interaction in self.interacM:
            for i,data in enumerate(load):

                node = self.FSI.getMeshPoint(i)

                if self.geometry.isAxisymmetric():
                    interaction.setNodTensorAxi(node,*data)

                elif self.geometry.is2D():
                    interaction.setNodTensor2D(node,*data)

                elif self.geometry.is3D():
                    interaction.setNodTensor3D(node,*data)

    # Apply Thermal boundary conditions

    def applyHeatFlux(self,heat):

        for interaction in self.interacT:
            for i,data in enumerate(heat):

                node = self.FSI.getMeshPoint(i)
                interaction.setNodVector(node,*data)

# |-------------------------------------|
# |   Return Mechanical Nodal Values    |
# |-------------------------------------|

    def getPosition(self):

        result = np.zeros((self.getSize(),self.dim))

        for i,axe in enumerate(self.axis):
            for j,data in enumerate(result):

                node = self.FSI.getMeshPoint(j)
                data[i] += node.getValue(w.Field1D(axe,w.AB))
                data[i] += node.getValue(w.Field1D(axe,w.RE))

        return result

    # Computes the nodal velocity result

    def getVelocity(self):

        result = np.zeros((self.getSize(),self.dim))

        for i,axe in enumerate(self.axis):
            for j,data in enumerate(result):

                node = self.FSI.getMeshPoint(j)
                data[i] = node.getValue(w.Field1D(axe,w.GV))
        
        return result

# |----------------------------------|
# |   Return Thermal Nodal Values    |
# |----------------------------------|

    def getTemperature(self):

        result = np.zeros((self.getSize(),1))
        
        for i in range(self.getSize()):

            node = self.FSI.getMeshPoint(i)
            result[i] += node.getValue(w.Field1D(w.TO,w.AB))
            result[i] += node.getValue(w.Field1D(w.TO,w.RE))

        return result

    # Computes the nodal temperature velocity

    def getTempRate(self):

        result = np.zeros((self.getSize(),1))

        for i in range(self.getSize()):

            node = self.FSI.getMeshPoint(i)
            result[i] = node.getValue(w.Field1D(w.TO,w.GV))
        
        return result

# |------------------------------------------|
# |   Backup and Update the PFEM Polytope    |
# |------------------------------------------|

    @tb.compute_time
    def update(self):

        self.checkRupture()
        tb.Interp.sharePolytope()
        self.metaFac.save(self.mfac)

    def __eIndex(self,element):

        size = element.getNumberOfNodes()

        if size == 2: return np.array([[1,0]])
        if size == 3: return np.array([[2,1,0]])
        if size == 4: return np.array([[0,3,2],[2,1,0]])

# |------------------------------|
# |   Other Wrapper Functions    |
# |------------------------------|

    @tb.write_logs
    @tb.compute_time
    def save(self): self.exporter.execute()
    def getSize(self): return self.FSI.getNumberOfMeshPoints()

    @tb.write_logs
    def exit(self): return
    def wayBack(self): self.tsm.removeLastStage()

# |-----------------------------------------|
# |   Build the Facet List from Polytope    |
# |-----------------------------------------|
    
    def getPolytope(self):

        faceList = list()
        if not self.polytope: return list()

        for i in range(self.polytope.size()):

            element = self.polytope.getElement(i)
            if not element.getEnabled(): continue

            # Split the square elements in two triangles

            position = self.__ePos(element)[self.__eIndex(element)]
            for pos in position: faceList.append(pos.ravel())

        return faceList

# |-------------------------------------|
# |   Positions of the Element Nodes    |
# |-------------------------------------|

    def __ePos(self,element):

        size = element.getNumberOfNodes()
        position = np.zeros((size,self.dim))

        for i in range(size):

            node = element.getNodeI(i)
            for j,axe in enumerate(self.axis):

                position[i,j] += node.getValue(w.Field1D(axe,w.AB))
                position[i,j] += node.getValue(w.Field1D(axe,w.RE))

        return position

# |----------------------------------|
# |   2D Rupture Interface Update    |
# |----------------------------------|
    
    def checkRupture(self):

        if tb.Step.time < 2.470e-02:
            self.rupture.checkRuptureCriterion()
        elementSet = self.interacM[0].getElementSet()
        self.polytope.activateBoundaryElements()
        elementSet.activateBoundaryElements()

        # Update the nodes in the FS interface (need FSInterface = InteracM)

        pointSet = set()
        self.FSI.cleanMeshPoints(self.geometry.getMesh())

        for i in range(elementSet.size()):

            element1D = elementSet.getElement(i)
            if not element1D.getEnabled(): continue
            curve = element1D.getMyMesh()

            for j in range(curve.getNbOfDownPoints()):
                pointSet.add(curve.getDownPoint(j))

        for point in pointSet:
            self.FSI.addMeshPoint(point)






        count = 0
        for i in range(elementSet.size()):
            count += 1

        print('\n',count)

        count = 0
        for i in range(elementSet.size()):
            element1D = elementSet.getElement(i)
            if element1D.getEnabled(): count += 1

        print(count,'\n')