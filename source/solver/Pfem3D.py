import pfem3Dw as w
import numpy as np

# %% Initializes the Fluid Wraper

class Pfem3D(object):

    def __init__(self,param):

        path = param['inputF']
        self.read(path)

        # Problem class and functions initialization

        if self.ID == 'IncompNewtonNoT':

            self.run = self.runIncomp
            self.problem = w.ProbIncompNewton(path)
            self.applyDispBC = self.applyDispIncomp

        elif self.ID == 'WCompNewtonNoT':

            self.run = self.runWcomp
            self.problem = w.ProbWCompNewton(path)
            self.applyDispPC = self.applyDispWcomp

        else: raise Exception('Problem type not supported')

        # Stores the important objects and variables

        self.solver = self.problem.getSolver()
        self.prevSolution = w.SolutionData()
        self.mesh = self.problem.getMesh()
        self.dim = self.mesh.getDim()
        self.FSI = w.VectorInt()

        # FSI data and stores the previous time step 

        self.problem.copySolution(self.prevSolution)
        self.mesh.getNodesIndex(self.group,self.FSI)
        self.mesh.setComputeNormalCurvature(True)
        self.nbrNode = self.FSI.size()

        # Initializes the simulation data

        self.disp = np.zeros((self.nbrNode,self.dim))
        self.initPos =  self.getPosition()
        self.reload = False
        self.factor = 1
        self.ok = True

        # Prints the initial solution and stats

        self.problem.displayParams()
        self.problem.dump()

# %% Run for Incompressible Flows

    def runIncomp(self,t1,t2):

        print('\nSolve ({:.5e}, {:.5e})'.format(t1,t2))
        print('----------------------------')

        # The line order is important here

        if not (self.reload and self.ok): self.factor //= 2
        self.factor = max(1,self.factor)
        self.resetSystem(t2-t1)
        iteration = 0

        # Main solving loop for the FSPC time step

        while iteration < self.factor:
            
            iteration += 1
            dt = (t2-t1)/self.factor
            self.solver.setTimeStep(dt)
            self.timeStats(dt+self.problem.getCurrentSimTime(),dt)
            self.ok = self.solver.solveOneTimeStep()

            if not self.ok:

                print('PFEM3D: Problem occured')
                if 2*self.factor > self.maxFactor: return False
                self.factor = 2*self.factor
                self.resetSystem(t2-t1)
                iteration = 0

        print('PFEM3D: Successful run')
        return True

# %% Run for Weakly Compressible Flows

    def runWcomp(self,t1,t2):

        print('\nSolve ({:.5e}, {:.5e})'.format(t1,t2))
        print('----------------------------')

        # Estimate the time step only once
        
        self.resetSystem(t2-t1)
        self.solver.computeNextDT()
        self.factor = int((t2-t1)/self.solver.getTimeStep())
        if self.factor > self.maxFactor: return False
        dt = (t2-t1)/self.factor
        self.timeStats(t2,dt)
        iteration = 0

        # Main solving loop for the FSPC time step

        while iteration < self.factor:
    
            iteration += 1
            self.solver.setTimeStep(dt)
            self.solver.solveOneTimeStep()

        print('PFEM3D: Successful run')
        return True

# %% Apply Boundary Conditions

    def applyDisplacement(self,disp):
        self.disp = disp.copy()

    # For implicit and incompressible flows

    def applyDispIncomp(self,distance,dt):

        BC = (distance)/dt
        for i in range(self.dim):
            for j in range(self.nbrNode):
                self.mesh.setNodeState(self.FSI[j],i,BC[j,i])

    # For explicit weakly compressive flows

    def applyDispWcomp(self,distance,dt):

        velocity = self.getVelocity()
        BC = 2*(distance-velocity*dt)/(dt*dt)

        # Update the FSI node states BC

        for i in range(self.dim):
            idx = int(self.dim+2+i)

            for j in range(self.nbrNode):
                self.mesh.setNodeState(self.FSI[j],idx,BC[j,i])

# %% Return Nodal Values

    def getPosition(self):

        pos = self.disp.copy()
        for i in range(self.dim):
            for j in range(self.nbrNode):
                pos[j,i] = self.mesh.getNode(self.FSI[j]).getCoordinate(i)

        return pos

    # Computes the nodal velocity vector

    def getVelocity(self):

        vel = self.disp.copy()
        for i in range(self.dim):
            for j in range(self.nbrNode):
                vel[j,i] = self.mesh.getNode(self.FSI[j]).getState(i)

        return vel
        
    # Computes the reaction nodal loads

    def getLoading(self):

        vec = w.VectorArrayDouble3()
        load = np.zeros((self.nbrNode,self.dim))
        self.solver.computeLoads(self.group,self.FSI,vec)
        for i in range(self.nbrNode): load[i] = vec[i][:self.dim]
        return -load

# %% Reads From the Lua File

    def read(self,path):

        file = open(path,'r')
        text = file.read().splitlines()
        file.close()

        for S in text:

            S = S.replace('"','').replace("'",'')
            try: value = S.replace(' ','').split('=')[1]
            except: continue

            if 'Problem.id' in S: self.ID = value
            if 'Problem.interface' in S: self.group = value
            if 'Problem.maxFactor' in S: self.maxFactor = int(value)
            if 'Problem.autoRemeshing' in S: self.autoRemesh = (value=='true')

# %% Other Functions

    def update(self):

        self.mesh.remesh(False)
        if (self.ID == 'IncompNewtonNoT'): self.solver.precomputeMatrix()
        self.problem.copySolution(self.prevSolution)
        self.reload = False

    # Prepare to solve one time step

    def resetSystem(self,dt):

        if self.reload: self.problem.loadSolution(self.prevSolution)
        if self.autoRemesh and (self.ID == 'IncompNewtonNoT'):
            if self.reload: self.solver.precomputeMatrix()

        distance = self.disp-(self.getPosition()-self.initPos)
        self.applyDispBC(distance,dt)
        self.reload = True

    # Display the current simulation state

    def timeStats(self,time,dt):

        start = self.problem.getCurrentSimTime()
        print('t1 = {:.5e} - dt = {:.3e}'.format(start,dt))
        print('t2 = {:.5e} - factor = {:.0f}'.format(time,self.factor))
        print('----------------------------')

    # Save the results or finalize

    def save(self):
        self.problem.dump()

    def exit(self):
        self.problem.displayTimeStats()
        