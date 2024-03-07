-- Problem Parameters

Problem = {}
Problem.verboseOutput = true
Problem.autoRemeshing = false -- Mettre en false si fluide-structure
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'
-- Problem.id = 'Bingham'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometryF.msh'
-- Ligne d'apres a enlever si pas pas maillage regulier 
Problem.Mesh.localHcharGroups = {'FSInterface','Inlet','Outlet'} -- Mesh non-uniforme --> J'enleve? -
Problem.Mesh.boundingBox = {-0.001, -0.001, 0.06, 0.01}
--Problem.Mesh.boundingBox = {-0.001, -0.001, 0.2, 0.01}

Problem.Mesh.exclusionZones = {}

--Problem.Mesh.alpha = 2 -- En général on met 1.2, ici j'ai mit 2 pour autoriser des éléments un peu plus déformés, prudence tout de même (Martin 
Problem.Mesh.alpha = 1.2 -- En général on met 1.2, ici j'ai mit 2 pour autoriser des éléments un peu plus déformés, prudence tout de même (Martin)

Problem.Mesh.omega = 0.7 -- 0.7
Problem.Mesh.gamma = 0.7 -- 0.7
Problem.Mesh.hchar = 0.0005  -- 0.001
Problem.Mesh.gammaFS = 0.5 -- 0.5
Problem.Mesh.minHeightFactor = 1e-4 -- 1e-3

Problem.Mesh.addOnFS = true -- Mettre à true dans des simulations type tuyaux avec surface libre au bout (Martin), ça évite d'avoir des trous.
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
Problem.Extractors[2].outputFile = 'pNewtonIncomp.txt'
Problem.Extractors[2].points = {{0.01, 0.005}} -- je suppose on fait comme ça mais sans certitude? 
Problem.Extractors[2].timeBetweenWriting =  math.huge

Problem.Extractors[3] =  {}
Problem.Extractors[3].kind = 'Point'
Problem.Extractors[3].whatToWrite = 'u'
Problem.Extractors[3].outputFile = 'VxNewtonIncomp.txt'
Problem.Extractors[3].points = {{0.01, 0.005}} -- je suppose on fait comme ça mais sans certitude? 
Problem.Extractors[3].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 0.003675
Problem.Material.gamma = 0
Problem.Material.rho = 1000
--Problem.Material.mReg = 30
--Problem.Material.tau0 = 0.014

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
Problem.Solver.MomContEq.gammaFS = 1 -- ne sert qu'en FracStep (Martin)

--

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.minRes = 1e-7
Problem.Solver.MomContEq.bodyForce = {0,0}


-- Fluid Structure Interface

Problem.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true -- FSInterface + VExt Pour FSPC

-- Boundary Condition Functions

function Problem.IC.initStates(x,y,z)
    -- p = 10*(1-x/0.06)
	-- return {0,0,p}
    return {0, 0, 0}
end

-- "Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true" stipule que la BC sur FSInterface est récupérée par Metafor (Martin)

function Problem.Solver.MomContEq.BC.InletP(x, y, z, t)
    -- p = 10
    if (t>0 and t<0.005) then
        --p = 2000*(1-math.cos(2*3.1415926*t/0.005))/2
        p = 2000
     else
        p = 0
    end
    return p
end

-- Remettre ça si outlet pressure = 0 !! 
function Problem.Solver.MomContEq.BC.OutletP(x, y, z, t)
    return 0
end

-- Test
-- function Problem.Solver.MomContEq.BC.OutletV(x, y, z, t)
--     return 0, 0
-- end


-- Mettre ca si maillage pas regulier 
function Problem.Mesh.computeHcharFromDistance(x,y,z,t,dist) -- Mesh non-uniforme
	return Problem.Mesh.hchar+dist*0.2
end
