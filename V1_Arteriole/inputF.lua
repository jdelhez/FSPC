-- Problem Parameters

Problem = {}
Problem.axiSymmetric = true
Problem.verboseOutput = true
Problem.autoRemeshing = false -- Mettre en false si fluide-structure
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'CGAL'
Problem.Mesh.mshFile = 'geometryF.msh'
Problem.Mesh.localHcharGroups = {'FSInterface'} 
Problem.Mesh.boundingBox = {0, -6e-5, 1.6e-5, 6e-5} -- Maybe a changer; jsp trop ce que doit contenit la bounding bow en axisym 
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.0 -- 1.0
Problem.Mesh.omega = 0.85
Problem.Mesh.gamma = 0.5
Problem.Mesh.hchar = 1e-6 -- 0.0005
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.minHeightFactor = 1e-3

Problem.Mesh.addOnFS = true
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = false -- false
Problem.Mesh.deleteBoundElements = false  -- false

-- Extractor Parameters

Problem.Extractors = {}
Problem.Extractors[0] = {}
Problem.Extractors[0].kind = 'GMSH'
Problem.Extractors[0].writeAs = 'NodesElements'
Problem.Extractors[0].outputFile = 'pfem/output.msh'
Problem.Extractors[0].whatToWrite = {'p','velocity'}
Problem.Extractors[0].timeBetweenWriting = math.huge --FSPC decide quand ecrire

-- Profil de vitesse au milieu

Problem.Extractors[1] =  {}
Problem.Extractors[1].kind = 'Point'
Problem.Extractors[1].whatToWrite = 'v'
Problem.Extractors[1].outputFile = 'VelocityProfile.txt'
Problem.Extractors[1].points = {{0, 0}, {0.0005,0 }, {0.0010,0 }, {0.0015,0 }, {0.0020,0 }, {0.0025,0 }, {0.0030,0 }, {0.0035,0 }, {0.0040,0 }, {0.0045,0 }, {0.0050,0 }, {0.0055,0 }, {0.0060,0 }, {0.0065,0 }, {0.0070,0 }, {0.0075,0 }, {0.0080,0 }, {0.0085,0 }, {0.0090,0 }, {0.0095,0 }, {0.01,0 }, {0.0105,0 }}
Problem.Extractors[1].timeBetweenWriting =  math.huge

Problem.Extractors[2] =  {}
Problem.Extractors[2].kind = 'Point'
Problem.Extractors[2].whatToWrite = 'p'
Problem.Extractors[2].outputFile = 'PressureDifference.txt'
Problem.Extractors[2].points = {{0, -0.03}, {0.005,-0.03 }, {0.0095,-0.03}, {0, 0.03}, {0.005,0.03 }, {0.0095,0.03}}
Problem.Extractors[2].timeBetweenWriting =  math.huge


-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 0.003675
-- Problem.Material.mu = 0.0035
Problem.Material.gamma = 0
---Problem.Material.rho = 1000
Problem.Material.rho = 1050

-- Solver Parameters

Problem.Solver = {}

Problem.Solver.id = 'PSPG'
-- Problem.Solver.id = 'FracStep'
--

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.coeffDTDecrease = 2
Problem.Solver.coeffDTincrease = 1

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.nlAlgo = 'NR'
-- Problem.Solver.MomContEq.nlAlgo = 'Picard'
Problem.Solver.MomContEq.residual = 'Ax_f'
Problem.Solver.MomContEq.sparseSolverLib = 'MKL'

--
Problem.Solver.MomContEq.tolerance = 1e-6 
Problem.Solver.MomContEq.gammaFS = 0.5 
--

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.minRes = 1e-6
Problem.Solver.MomContEq.bodyForce = {0,0}

-- Fluid Structure Interface

Problem.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true -- FSInterface + VExt Pour FSPC
-- Problem.Solver.MomContEq.BC['AxisFreeSlipEuler'] = true
Problem.Solver.MomContEq.BC['one_epsFreeSlip'] = 1e4

-- Boundary Condition Functions

function Problem.IC.initStates(x,y,z)
    
    v = 0.0
    p = 0.0

    return {0, v, p}
end


-- function Problem.Solver.MomContEq.BC.InletVEuler(x,y,z,t)
--    return 0,0.1
-- end

function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)
    dt = 0.0
    td = t-dt 
    v = 0.03*math.cos(0*td + 0) + 
    0.015*math.cos(5.74759839519073*td -2.2) + 
    0.007*math.cos(11.4951967903815*td + 1.5)
    v = v * math.min(1,t/0.15)
    r = 14e-6
    v = v  * math.max(0.,(1 - (x / r)^4))
    
    return 0, v
end

function Problem.Solver.MomContEq.BC.OutletP(x, y, z, t)
    p0 = 10018.3

    dt = 0.
    td = t-dt 
    p = 10500*math.cos(0*td + 0) + 
    1000*math.cos(5.80640640376384*td + 2.8) + 
    500*math.cos(11.6128128075277*td + 0.4) 
    
    p=(p-p0) * math.min(1,t/0.15)
    
    return p
end


-- function Problem.Solver.MomContEq.BC.InletP(x, y, z, t)
--     td = t 
--     p = 6471.68782493127*math.cos(0*td + 0) + 
--         4546.40390397331*math.cos(5.80640640376384*td + 2.88303288234243) + 
--         2912.28391822816*math.cos(11.6128128075277*td + 0.437321132460916) + 
--         1999.49340669353*math.cos(17.4192192112915*td -1.80886753960572) + 
--         1365.06363497520*math.cos(23.2256256150554*td + 2.00090876389695) + 
--         674.792594796269*math.cos(29.0320320188192*td -0.524481534622267) + 
--         144.936378283116*math.cos(34.8384384225831*td -2.31301923374297) + 
--         320.573352689215*math.cos(40.6448448263469*td + 2.87413985644085) + 
--         380.090549614032*math.cos(46.4512512301107*td + 0.221634032043418) + 
--         286.600758107930*math.cos(52.2576576338746*td -2.47517628449584) 
--     p = p * math.min(1,t/0.1)
    
--     return p
-- end

function Problem.Solver.MomContEq.BC.FixedV(x, y, z, t)
    return 0,0
end


function Problem.Mesh.computeHcharFromDistance(x,y,z,t,dist) -- Mesh non-uniforme
	c = Problem.Mesh.hchar
    r = 15e-6
    fact = math.max (1,1.5*(1-dist/r))
    h = c / fact
    return h
end