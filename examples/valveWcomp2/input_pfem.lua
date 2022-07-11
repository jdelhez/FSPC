-- Problem Parameters

Problem = {}
Problem.autoRemeshing = false
Problem.verboseOutput = false
Problem.simulationTime = math.huge
Problem.id = 'WCompNewtonNoT'

-- FSPC Parameters

Problem.interface = 'FSInterface'
Problem.maxFactor = 1000

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.6
Problem.Mesh.hchar = 0.003
Problem.Mesh.addOnFS = false
Problem.Mesh.minAspectRatio = 1e-3
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = true
Problem.Mesh.deleteBoundElements = true
Problem.Mesh.laplacianSmoothingBoundaries = false
Problem.Mesh.boundingBox = {-0.8,-1,0.8,1}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometry.msh'
Problem.Mesh.localHcharGroups = {'LocalHchar'}
Problem.Mesh.exclusionGroups = {'Poly1','Poly2','Poly3','Poly4'}
Problem.Mesh.ignoreGroups = {'SolidTop','SolidBot','ClampS','Exterior'}

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
Problem.Material.K0p = 1
Problem.Material.K0 = 100
Problem.Material.mu = 1e-4
Problem.Material.gamma = 0
Problem.Material.rhoStar = 1e-3

-- Initial Conditions

Problem.IC = {}
Problem.IC.InletFixed = true
Problem.IC.OutletFixed = true
Problem.IC.ClampLFixed = true
Problem.IC.FSInterfaceFixed = false

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'CDS_dpdt'
Problem.Solver.securityCoeff = 0.01

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.maxRemeshDT = math.huge

-- Momentum Continuity Equation

Problem.Solver.MomEq = {}
Problem.Solver.MomEq.bodyForce = {0,0}

Problem.Solver.ContEq = {}
Problem.Solver.ContEq.stabilization = 'Meduri'

-- Momentum Continuity BC

Problem.Solver.MomEq.BC = {}
Problem.Solver.ContEq.BC = {}
Problem.Solver.MomEq.BC['FSInterfaceVExt'] = true

function Problem.IC:initStates(pos)
	return {0,0,0,Problem.Material.rhoStar,0,0}
end

function Problem.Solver.MomEq.BC:ClampLV(pos,t)
	return {0,0}
end

function Problem.Solver.MomEq.BC:InletV(pos,t)

	local tmax = 1
	local acc = 10

	if (t<tmax) then
		return {acc,0}
	else
		return {0,0}
	end
end

function Problem.Mesh:computeHcharFromDistance(pos,t,dist)

	local f = 6
	local L = 0.5125
	local hchar = Problem.Mesh.hchar
    return f*dist*hchar/(L/2)+hchar
end