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
Problem.Mesh.boundingBox = {-0.043, -0.02155 , 0.043, 0.02155}
Problem.Mesh.exclusionZones = {}



Problem.Mesh.alpha = 1
Problem.Mesh.omega = 0.7
Problem.Mesh.gamma = 0.9
Problem.Mesh.hchar = 1e-3
Problem.Mesh.gammaFS = 0.5
Problem.Mesh.minHeightFactor = 1e-3


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
Problem.Material.mu = 0.003675
Problem.Material.gamma = 0
Problem.Material.rho = 1000

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
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.minRes = 1e-8
Problem.Solver.MomContEq.bodyForce = {0,0}


-- Fluid Structure Interface

Problem.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true -- FSInterface + VExt Pour FSPC

-- Boundary Condition Functions

function Problem.IC.initStates(x,y,z)
    --p = 10*(1-x/0.06)
	return {0,0,0}
end

-- Du coup je ne dois pas avoir de BC sur les FSIinterface? Ou quand même si? Car si je mets que vy = 0, comment ça pourrait se déformer?? 


function Problem.Solver.MomContEq.BC.OutletP(x, y, z, t)
    return 0
end

function Problem.Solver.MomContEq.BC.BoundaryV(x, y, z, t)
    return 0, 0
end

function Problem.Solver.MomContEq.BC.InletP(x, y, z, t)
    -- p = 10*math.min(1,t/0.3)
    if (t>0 and t<1) then
        p = t
    else
        p = -100*math.sin(2*3.14159*t)
    end
    return p
 end

--function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)
-- p = 10
--   if (t>0 and t<0.5) then
--    vx = 0.3*(1-math.cos(2*3.1415926*t/0.5))/2
--    else
--    vx = 0
--    end
-- return vx, 0
-- end



--function Problem.Mesh.computeHcharFromDistance(x,y,z,t,dist) -- Mesh non-uniforme
--	return Problem.Mesh.hchar+dist*0.1
-- end
