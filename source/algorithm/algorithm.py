from ..tools import printY,printG,Logs,Clock,timerPrint
import collections

# %% Parent Algorithm Class

class Algorithm(object):
    def __init__(self,input,param,com):

        printY('Initializing FSI algorithm\n')
        
        self.verified = True
        self.dim = param['dim']

        self.step = input['step']
        self.interp = input['interp']
        self.solver = input['solver']

        if com.rank == 1: self.converg = input['converg']

        self.clock = collections.defaultdict(Clock)
        self.logTime = Logs('Iteration.log',['Time','Time Step'])
        self.logIter = Logs('Iteration.log',['Iteration','Residual'])

        self.totTime = param['tTot']
        self.iterMax = param['maxIt']
        self.dtWrite = param['dtWrite']

# %% Runs the Fluid-Solid Coupling

    def run(self,com):

        print('Begin FSI Computation')
        self.clock['Total time'].start()
        prevWrite = self.step.time

        # External temporal loop
        
        while self.step.time < self.totTime:

            self.logTime.newLine()
            self.logTime.write(self.step.time,self.step.dt)
            printG('FSPC: t =',self.step.time,'| dt =',self.step.dt)

            # Save previous time step

            if self.verified is True:

                prevDisp = self.interp.disp.copy()
                prevLoad = self.interp.load.copy()
                if com.rank == 1: self.vel = self.solver.getVelocity()
                if com.rank == 1: self.acc = self.solver.getAcceleration()

            # Predictor and Internal FSI loop

            if com.rank == 1:
                self.interp.disp += self.step.dt*(self.vel+self.acc*self.step.dt/2)
            self.verified = self.couplingAlgo(com)

            # Restart the time step if fail

            if not self.verified:
                
                self.interp.disp = prevDisp.copy()
                self.interp.load = prevLoad.copy()
                self.step.update(self.verified)
                continue

            # Update the F and S solvers for the next time step
            
            self.clock['Solver update'].start()
            self.solver.update()
            self.clock['Solver update'].end()

            # Write fluid and solid solution
            
            if self.step.time-prevWrite > self.dtWrite:

                self.clock['Solver save'].start()
                self.solver.save()
                self.clock['Solver save'].end()

                prevWrite = self.step.time

            # Update the time step manager class

            self.step.update(self.verified)

        # Ends the FSI simulation

        self.solver.exit()
        self.clock['Total time'].end()
        timerPrint(self.clock)

# %% Transfer and Update Functions

    def residualDispS(self):
        
        disp = self.solver.getDisplacement()
        self.residual = disp-self.interp.disp

    # Transfers mechanical data fluid -> solid

    def transferLoadFS(self,com):

        if com.rank == 0: self.interp.getLoadF()
        self.interp.interpLoadFS(com)
        if com.rank == 1: self.interp.applyLoadS(self.step.nextTime)
        
    # Transfers mechanical data solid -> fluid

    def transferDispSF(self,com):
        
        self.interp.interpDispSF(com)
        if com.rank == 0: self.interp.applyDispF(self.step.dt)
