-- Problem Parameters

Problem = {}
Problem.autoRemeshing = false
Problem.verboseOutput = true
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- FSPC Parameters

Problem.interface = 'FSInterface'
Problem.maxFactor = 10

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.alpha = 1.3
Problem.Mesh.omega = 0.7
Problem.Mesh.gamma = 0.5
Problem.Mesh.hchar = 2e-3
Problem.Mesh.gammaFS = 0.5
Problem.Mesh.addOnFS = true
Problem.Mesh.minAspectRatio = 1e-2
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = false
Problem.Mesh.deleteBoundElements = false
Problem.Mesh.laplacianSmoothingBoundaries = true
Problem.Mesh.boundingBox = {0,0,0,0.35,0.25,0.4}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometryF.msh'
Problem.Mesh.exclusionGroups = {'Polytope'}
Problem.Mesh.localHcharGroups = {'FSInterface','Polytope'}
Problem.Mesh.ignoreGroups = {}

-- Extractor Parameters

Problem.Extractors = {}

Problem.Extractors[0] = {}
Problem.Extractors[0].kind = 'GMSH'
Problem.Extractors[0].writeAs = 'NodesElements'
Problem.Extractors[0].outputFile = 'pfem/fluid.msh'
Problem.Extractors[0].whatToWrite = {'p','velocity'}
Problem.Extractors[0].timeBetweenWriting = math.huge

Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'Global'
Problem.Extractors[1].whatToWrite = 'mass'
Problem.Extractors[1].outputFile = 'mass.txt'
Problem.Extractors[1].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 1
Problem.Material.gamma = 0
Problem.Material.rho = 1220

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'FracStep'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.coeffDTDecrease = math.huge
Problem.Solver.coeffDTincrease = math.huge

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.residual = 'U_P'
Problem.Solver.MomContEq.nlAlgo = 'Picard'
Problem.Solver.MomContEq.sparseSolverLib = 'MKL'
Problem.Solver.MomContEq.PStepSparseSolver = 'LLT'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.gammaFS = 0.5
Problem.Solver.MomContEq.minRes = 1e-6
Problem.Solver.MomContEq.cgTolerance = 1e-8
Problem.Solver.MomContEq.bodyForce = {0,0,0}

-- Momentum Continuity BC

Problem.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true
-- Problem.Solver.MomContEq.BC['BottomFreeSlipEuler'] = true

function Problem.IC:initStates(pos)
    return {0,0,0,0}
end

function Problem.Solver.MomContEq.BC:InletVEuler(pos,t)

    local tmax = 0.1
    local vmax = 0.5
    local v = vmax*t/tmax
    
    if (t<tmax) then
	    return v,0,0
	else
	    return vmax,0,0
    end
end

function Problem.Solver.MomContEq.BC:PolytopeV(pos,t)
    return 0,0,0
end

function Problem.Solver.MomContEq.BC:ReservoirVEuler(pos,t)

    local tmax = 0.1
    local vmax = 0.5
    local v = vmax*t/tmax
    
    if (t<tmax) then
	    return v,0,0
	else
	    return vmax,0,0
    end
end

function Problem.Solver.MomContEq.BC:BottomVEuler(pos,t)
	return 0,0,0
end

function Problem.Mesh:computeHcharFromDistance(pos,t,dist)

	local hchar = Problem.Mesh.hchar
	return hchar+(dist)*0.1
end