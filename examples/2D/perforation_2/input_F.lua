-- Problem Parameters

Problem = {}
Problem.verboseOutput = true
Problem.autoRemeshing = false
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometry_F.msh'
Problem.Mesh.boundingBox = {-0.075, 0, 0.075, 8.15e-3}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.3
Problem.Mesh.hchar = 5e-5
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.minHeightFactor = 1e-2

Problem.Mesh.addOnFS = true
Problem.Mesh.deleteFlyingNodes = true
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteBoundElements = false

-- Extractor Parameters

Problem.Extractors = {}
Problem.Extractors[0] = {}
Problem.Extractors[0].kind = 'GMSH'
Problem.Extractors[0].writeAs = 'NodesElements'
Problem.Extractors[0].outputFile = 'pfem/output.msh'
Problem.Extractors[0].whatToWrite = {'p', 'velocity'}
Problem.Extractors[0].timeBetweenWriting = math.huge

Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'Global'
Problem.Extractors[1].whatToWrite = 'mass'
Problem.Extractors[1].outputFile = 'mass.txt'
Problem.Extractors[1].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 1e-3
Problem.Material.gamma = 0
Problem.Material.rho = 1000

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'PSPG'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.coeffDTDecrease = 2
Problem.Solver.coeffDTincrease = 1

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.nlAlgo = 'Picard'
Problem.Solver.MomContEq.residual = 'Ax_f'
Problem.Solver.MomContEq.sparseSolverLib = 'MKL'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.gammaFS = 0.5
Problem.Solver.MomContEq.minRes = 1e-6
Problem.Solver.MomContEq.tolerance = 1e-16
Problem.Solver.MomContEq.bodyForce = {0, -9.81}

-- Momentum Continuity BC

Problem.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

function Problem.IC.initStates(x, y, z)
	return {0, -200, 0}
end

function Problem.IC.initFSInterfaceStates(x, y, z)
	return {0, 0, 0}
end

function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)

	tmin = 1e-5
	vmin = -200

	tmax = 1e-4
	vmax = -1000

	if (t<tmin) then
		return 0, vmin

	elseif(t<tmax) then
		local v = vmin + (vmax - vmin)*(t - tmin)/(tmax - tmin)
		return 0, v

	else
		return 0, vmax
	end
end
