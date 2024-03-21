-- Problem Parameters

Problem = {}
Problem.verboseOutput = true
Problem.autoRemeshing = false -- Mettre en false si fluide-structure
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometryF.msh'
--Problem.Mesh.localHcharGroups = {'FSInterface','Reservoir','FreeSurface'} -- Mesh non-uniforme --> J'enleve? 
Problem.Mesh.boundingBox = {-0.043, -0.025 , 0.043, 0.0}
Problem.Mesh.exclusionZones = {}



Problem.Mesh.alpha = 1.3
Problem.Mesh.omega = 0.7
Problem.Mesh.gamma = 0.9
Problem.Mesh.hchar = 5e-4
Problem.Mesh.gammaFS = 0.5
Problem.Mesh.minHeightFactor = 5e-4


Problem.Mesh.addOnFS = false
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = false
Problem.Mesh.deleteBoundElements = false

-- Extractor Parameters

Problem.Extractors = {}
Problem.Extractors[0] = {}
Problem.Extractors[0].kind = 'GMSH'
Problem.Extractors[0].writeAs = 'NodesElements'
Problem.Extractors[0].outputFile = 'pfem/output.msh'
Problem.Extractors[0].whatToWrite = {'p','velocity'}
Problem.Extractors[0].timeBetweenWriting = math.huge --FSPC decide quand ecrire

Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'Global'
Problem.Extractors[1].whatToWrite = 'mass'
Problem.Extractors[1].outputFile = 'mass.txt'
Problem.Extractors[1].timeBetweenWriting = math.huge

-- Essai Jeanne: 

Problem.Extractors[2] =  {}
Problem.Extractors[2].kind = 'Point'
Problem.Extractors[2].whatToWrite = 'p'
Problem.Extractors[2].outputFile = 'pCenter.txt'
Problem.Extractors[2].points = {{0, 0}} -- je suppose on fait comme ça mais sans certitude? 
Problem.Extractors[2].timeBetweenWriting = math.huge

Problem.Extractors[3] =  {}
Problem.Extractors[3].kind = 'Point'
Problem.Extractors[3].whatToWrite = 'u'
Problem.Extractors[3].outputFile = 'uOutlet.txt'
Problem.Extractors[3].points = {{0.043, -0.0125}, {0.043, -0.01}, {0.043, -0.0075}, {0.043, -0.005}, {0.043, -0.0025}, {0.043, 0}, {0.043, 0.0025}, {0.043, 0.005},{0.043, 0.0075}, {0.043, 0.01}, {0.043, 0.0125} } -- je suppose on fait comme ça mais sans certitude? 
Problem.Extractors[3].timeBetweenWriting = math.huge


-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 0.0035578
Problem.Material.gamma = 0
Problem.Material.rho = 1060

-- Solver Parameters

Problem.Solver = {}

Problem.Solver.id = 'PSPG'
-- Problem.Solver.id = 'FracStep'
--

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.coeffDTDecrease = math.huge
Problem.Solver.coeffDTincrease = math.huge

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.nlAlgo = 'NR'
Problem.Solver.MomContEq.residual = 'Ax_f'
Problem.Solver.MomContEq.sparseSolverLib = 'MKL'

--

Problem.Solver.MomContEq.tolerance = 1e-7
Problem.Solver.MomContEq.gammaFS = 1

--

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 15
Problem.Solver.MomContEq.minRes = 1e-8
Problem.Solver.MomContEq.bodyForce = {0,0}


-- Fluid Structure Interface

Problem.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true -- FSInterface + VExt Pour FSPC

Problem.Solver.MomContEq.BC['AxisFreeSlipEuler'] = true
Problem.Solver.MomContEq.BC['one_epsFreeSlip'] = 1e4

-- Boundary Condition Functions

function Problem.IC.initStates(x,y,z)
    --p = 10*(1-x/0.06)
	return {0,0,0}
end

-- Du coup je ne dois pas avoir de BC sur les FSIinterface? Ou quand même si? Car si je mets que vy = 0, comment ça pourrait se déformer?? 


function Problem.Solver.MomContEq.BC.OutletP(x, y, z, t)
    pout = 95.3959190013472 + 
    15.8037197086139 *math.cos(6.28318530717959*t-2.07014241773753)  +
    6.92306732637227 *math.cos(12.5663706143592*t-2.65812155666215)  +
    4.61979791830862 *math.cos(18.8495559215388*t+2.87871514830170) +
    2.71403505419131 *math.cos(25.1327412287183*t+1.64986000295816) +
    0.735607741115687*math.cos(31.4159265358979*t-0.299121420016275)+
    0.743126679832966*math.cos(37.6991118430775*t+2.13292382118801) +
    0.775496159754907*math.cos(43.9822971502571*t+0.287872588274476)

    p= pout * 133.3
    return p
end

function Problem.Solver.MomContEq.BC.BoundaryV(x, y, z, t)
    return 0, 0
end

-- function Problem.Solver.MomContEq.BC.InletP(x, y, z, t)
--     p = 400*math.sin(2*3.14159*(t+0.061))-150.
--     p = math.max(p,-15)
--     -- if (t>0 and t<1) then
--     --    p = t
--     -- else
--     --    p = -100*math.sin(2*3.14159*t)
--     -- end
--     return p
--  end

function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)
    tr  = t-math.floor(t)
    if (tr<0.41) then
        vx=179.212434923075 + 
        346.133181397307 * math.cos(6.28318530717959*tr-1.03814633164985)+ 
        273.464992134736 * math.cos(12.5663706143592*tr-2.11882642434818)+ 
        170.398012407865 * math.cos(18.8495559215388*tr+3.01708979440978)+ 
        71.0138350893899 * math.cos(25.1327412287183*tr+1.68057926325852)
        vx = vx / 1000
    else
        vx = 0
    end
    return vx, 0
end



--function Problem.Mesh.computeHcharFromDistance(x,y,z,t,dist) -- Mesh non-uniforme
--	return Problem.Mesh.hchar+dist*0.1
-- end
