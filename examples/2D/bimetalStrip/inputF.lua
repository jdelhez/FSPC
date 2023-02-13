-- Problem Parameters

Problem = {}
Problem.autoRemeshing = false
Problem.verboseOutput = false
Problem.simulationTime = math.huge
Problem.id = 'Boussinesq'

-- FSPC Parameters

Problem.interface = 'FSInterface'
Problem.maxFactor = 10

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.alpha = 1e3
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.6
Problem.Mesh.hchar = 1e-3
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.addOnFS = true
Problem.Mesh.minAspectRatio = 1e-3
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = false
Problem.Mesh.deleteBoundElements = false
Problem.Mesh.laplacianSmoothingBoundaries = false
Problem.Mesh.boundingBox = {-0.2,-0.05,0.5,0.05}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometryF.msh'
Problem.Mesh.localHcharGroups = {'FSInterface'}
Problem.Mesh.exclusionGroups = {'FSInterface'}
Problem.Mesh.ignoreGroups = {}

-- Extractor Parameters

Problem.Extractors = {}

Problem.Extractors[0] = {}
Problem.Extractors[0].kind = 'GMSH'
Problem.Extractors[0].writeAs = 'NodesElements'
Problem.Extractors[0].outputFile = 'pfem/output.msh'
Problem.Extractors[0].whatToWrite = {'T','velocity','p'}
Problem.Extractors[0].timeBetweenWriting = math.huge

Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'Global'
Problem.Extractors[1].whatToWrite = 'mass'
Problem.Extractors[1].outputFile = 'mass.txt'
Problem.Extractors[1].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 1.73e-5
Problem.Material.gamma = 0
Problem.Material.rho = 1.229
Problem.Material.epsRad = 0
Problem.Material.sigmaRad = 5.670374419e-8
Problem.Material.R = 8.31446261815324
Problem.Material.alphaLin = 69e-6
Problem.Material.DgammaDT = 0
Problem.Material.Tinf = 300
Problem.Material.Tr = 650
Problem.Material.k = 1.4
Problem.Material.cp = 1e3
Problem.Material.h = 30

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'PSPG'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.coeffDTDecrease = math.huge
Problem.Solver.coeffDTincrease = math.huge
Problem.Solver.solveHeatFirst = true

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.residual = 'Ax_f'
Problem.Solver.MomContEq.nlAlgo = 'Picard'
Problem.Solver.MomContEq.sparseSolverLib = 'MKL'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.minRes = 1e-8
Problem.Solver.MomContEq.bodyForce = {0,0}

-- Heat Equation

Problem.Solver.HeatEq = {}
Problem.Solver.HeatEq.residual = 'Ax_f'
Problem.Solver.HeatEq.nlAlgo = 'Picard'
Problem.Solver.HeatEq.sparseSolverLib = 'MKL'

Problem.Solver.HeatEq.maxIter = 25
Problem.Solver.HeatEq.minRes = 1e-8
Problem.Solver.HeatEq.cgTolerance = 1e-9

-- Heat Momentum Continuity BC

Problem.IC = {}
Problem.Solver.HeatEq.BC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.HeatEq.BC['FSInterfaceTExt'] = true
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

function Problem.IC:initStates(pos)
	return {0,0,0,293.15}
end

function Problem.Solver.MomContEq.BC:InletVEuler(pos,t)

	local tmax = 3000
	local vmax = 0.2

	if (t<tmax) then
		return vmax*(t/tmax),0
	else
		return vmax,0
	end
end

function Problem.Solver.HeatEq.BC:InletT(pos,t)

	local tmax = 5000
	local Tmin = 293.15
	local Tmax = 593.15
	local dT = Tmax-Tmin

	if (t<tmax) then
		return Tmin+dT*(t/tmax),0
	else
		return Tmax,0
	end
end

function Problem.Solver.MomContEq.BC:BorderVEuler(pos,initPos,state,t) 
	return 0,0
end

function Problem.Solver.MomContEq.BC:OutletP(pos,initPos,state,t) 
    return 0,0
end

function Problem.Solver.HeatEq.BC:BorderQ(pos,initPos,state,t) 
    return 0,0
end

function Problem.Solver.HeatEq.BC:OutletQ(pos,initPos,state,t) 
    return 0,0
end

function Problem.Mesh:computeHcharFromDistance(pos,t,dist)

	local hchar = Problem.Mesh.hchar
	return hchar+dist*0.1
end