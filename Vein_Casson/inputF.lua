-- Problem Parameters

Problem = {}
Problem.axiSymmetric = true
Problem.verboseOutput = true
Problem.autoRemeshing = false -- Mettre en false si fluide-structure
Problem.simulationTime = math.huge
Problem.id = 'Casson'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'CGAL'
Problem.Mesh.mshFile = 'geometryF.msh'
Problem.Mesh.localHcharGroups = {'FSInterface'} 
Problem.Mesh.boundingBox = {0, -0.08, 0.02, 0.08}  -- Maybe a changer; jsp trop ce que doit contenit la bounding bow en axisym 
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.0 -- 1.0
Problem.Mesh.omega = 0.85
Problem.Mesh.gamma = 0.5
Problem.Mesh.hchar = 0.001 -- 0.0005
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
Problem.Extractors[1].points = {{0, 0.05}, {0.0005,0.05 }, {0.0010,0.05 }, {0.0015,0.05 }, {0.0020,0.05 }, {0.0025,0.05}, {0.0030,0.05 }, {0.0035,0.05 }, {0.0040,0.05 }, {0.0045,0.05 }, {0.0050,0.05}, {0.0055,0.05 }, {0.0060,0.05 }, {0.0065,0.05}, {0.0070,0.05 }, {0.0075,0.05 }, {0.0080,0.05}, {0.0085,0.05 }, {0.0090,0.05 }, {0.0095,0.05 }, {0.01,0.05 }, {0.0105,0.05 }}
Problem.Extractors[1].timeBetweenWriting =  math.huge

Problem.Extractors[2] =  {}
Problem.Extractors[2].kind = 'Point'
Problem.Extractors[2].whatToWrite = 'p'
Problem.Extractors[2].outputFile = 'PressureDifference.txt'
Problem.Extractors[2].points = {{0, -0.03}, {0.005,-0.03 }, {0.0095,-0.03}, {0, 0.03}, {0.005,0.03 }, {0.0095,0.03}}
Problem.Extractors[2].timeBetweenWriting =  math.huge


-- Material Parameters

Problem.Material = {}
-- Problem.Material.mu = 0.003675

Problem.Material.gamma = 0
Problem.Material.rho = 1050

Problem.Material.mu = 0.0038 -- peut etre il faut mettre mu_m du coup?? 
---Problem.Material.rho = 1000
Problem.Material.mReg = 200
Problem.Material.tau0 = 0.0035

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
    
    v = 0.0010
    r = 0.01
    v = 2.0 * v  * (1 - (x / r)^2)
    p = 0.0

    return {0, v, p}
end


-- function Problem.Solver.MomContEq.BC.InletVEuler(x,y,z,t)
--    return 0,0.1
-- end

function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)
    T = 0.8
    omega = 2*math.pi/T
    q = 1.5388 + 0.1835*math.cos(omega*t-2.6072) +
        0.3697*math.cos(2*omega*t-2.9340) + 0.0504*math.cos(3*omega*t+3.1271) +
        0.0646*math.cos(4*omega*t-1.8944) + 0.0433*math.cos(5*omega*t-2.1515) +
        0.0565*math.cos(6*omega*t-2.8395) 
    q = 0.001*q/60 -- L/min -- > m^3/s (que qqun verifie mdr moi pas douee avec les abaques)
    r = 0.01
    A = math.pi * r * r-- comme ca qu'on fait un carré? je sais plus 
    v = q/A  -- q --> v

    v = v * math.min(1,t/0.1)

    v = 1.5 * v  * (1 - (x / r)^4)
    
    return 0, v
end


function Problem.Solver.MomContEq.BC.OutletP(x, y, z, t)
    t0 = 0.1
    if (t>t0) then
        p0 = 0.
        p = 5
        p = p * 133.33

        p=(p-p0) * math.min(1,(t-t0)/0.3)
    else
        p = 0.
    end

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
    fact = math.max (1,3*(1-dist/0.0075))
    h = c / fact
    return h
end
