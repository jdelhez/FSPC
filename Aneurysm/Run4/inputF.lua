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
Problem.Mesh.localHcharGroups = {'FSInterface'} -- Mesh non-uniforme --> J'enleve? 
Problem.Mesh.boundingBox = {0, -0.12, 0.06, 0.12} -- Maybe a changer; jsp trop ce que doit contenit la bounding bow en axisym 
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

Problem.Extractors[1] =  {}
Problem.Extractors[1].kind = 'Point'
Problem.Extractors[1].whatToWrite = 'v'
Problem.Extractors[1].outputFile = 'VelocityProbes.txt'
Problem.Extractors[1].points = {{0, 0}, {0.0025,0 }, {0.0050,0 }, {0.0075,0 }, {0.0100,0 }, {0.0125,0 }, {0.0150,0 }, {0.0175,0 }, {0.0200,0 }, {0.0225,0 }, {0.0250,0 }, {0.0275,0 }, {0.0300,0},{0,-0.06}, {0.0025,-0.06 }, {0.0050,-0.06 }, {0.0075,-0.06 }, {0.0100,-0.06 }, {0, 0.06}, {0.0025,0.06 }, {0.0050,0.06 }, {0.0075,0.06 }, {0.0100,0.06 }}
Problem.Extractors[1].timeBetweenWriting =  math.huge

Problem.Extractors[2] =  {}
Problem.Extractors[2].kind = 'Point'
Problem.Extractors[2].whatToWrite = 'p'
Problem.Extractors[2].outputFile = 'PressureDifference.txt'
Problem.Extractors[2].points = {{0, -0.06}, {0.005,-0.06 }, {0.0095,-0.06}, {0, 0.06}, {0.005,0.06 }, {0.0095,0.06}}
Problem.Extractors[2].timeBetweenWriting =  math.huge

-- Material Parameters
-- Laisser ca comme ca ? meme si ca ne permet pas de comparaison avec l'article 

Problem.Material = {}
--Problem.Material.mu = 0.003675
Problem.Material.mu = 0.0035
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


-- function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)
--     T = 1.
--     omega = 2*math.pi/T
--     v = 5.7106 + 5.6858*math.cos(omega*t-2.2261) +
--         5.2551*math.cos(2*omega*t+1.9211) + 4.5999*math.cos(3*omega*t-0.2188) +
--         2.1677*math.cos(4*omega*t-2.3788) + 1.3145*math.cos(5*omega*t+2.7684) +
--         1.2146*math.cos(6*omega*t+1.0377) + 1.5133*math.cos(7*omega*t-0.9154) +
--         1.0345*math.cos(8*omega*t+3.1026) + .60400*math.cos(9*omega*t+1.4442) +
--         .48600*math.cos(10*omega*t+0.0435)+ .73920*math.cos(11*omega*t-2.0025) +
--         .61970*math.cos(12*omega*t+2.0332)+ .46680*math.cos(13*omega*t+0.0295) +
--         .27580*math.cos(14*omega*t-1.6709)+ .32240*math.cos(15*omega*t+2.8396) +
--         .31060*math.cos(16*omega*t+0.7295)+ .27410*math.cos(17*omega*t-1.4477)
--     v = v*0.01  -- cm/s -- > m/s

--     v = v * math.min(1,t/0.05)
    
--     r = 0.01
--     v = 1.5 * v  * (1 - (x / r)^4)
    
--     return 0, v
-- end

function Problem.Solver.MomContEq.BC.InletP(x, y, z, t)
    T = 1.
    dt = -0.12
    
    omegatp = 2*math.pi*(t-dt)/T
    
    p = 89.2632000000000 + 14.2636	* math.cos(omegatp-3.06220) +
        .14560 * math.cos(2*omegatp+1.16220) + 6.43040 * math.cos(3*omegatp-0.6977) +
        3.91530 * math.cos(4*omegatp-2.81270) + 1.36180 * math.cos(5*omegatp+1.4279) +
        .672500 * math.cos(6*omegatp+1.17040) + 1.20920 * math.cos(7*omegatp-0.9584) +
        1.09780 * math.cos(8*omegatp+2.85340) + .637100 * math.cos(9*omegatp+0.6059) +
        .251900 * math.cos(10*omegatp-0.8007) + .280800 * math.cos(11*omegatp-2.3522) +
        .233100 * math.cos(12*omegatp+1.8069) + .170100 * math.cos(13*omegatp+0.3118) +
        .152000 * math.cos(14*omegatp-1.2515) + .126500 * math.cos(15*omegatp+2.9940) +
        .100800 * math.cos(16*omegatp+1.3613) + .131100 * math.cos(17*omegatp-0.1955)
    p = p * 133.33

    omegatu = 2*math.pi*t/T
    v = 5.7106 + 5.6858*math.cos(omegatu-2.2261) +
        5.2551*math.cos(2*omegatu+1.9211) + 4.5999*math.cos(3*omegatu-0.2188) +
        2.1677*math.cos(4*omegatu-2.3788) + 1.3145*math.cos(5*omegatu+2.7684) +
        1.2146*math.cos(6*omegatu+1.0377) + 1.5133*math.cos(7*omegatu-0.9154) +
        1.0345*math.cos(8*omegatu+3.1026) + .60400*math.cos(9*omegatu+1.4442) +
        .48600*math.cos(10*omegatu+0.0435)+ .73920*math.cos(11*omegatu-2.0025) +
        .61970*math.cos(12*omegatu+2.0332)+ .46680*math.cos(13*omegatu+0.0295) +
        .27580*math.cos(14*omegatu-1.6709)+ .32240*math.cos(15*omegatu+2.8396) +
        .31060*math.cos(16*omegatu+0.7295)+ .27410*math.cos(17*omegatu-1.4477)
    v = (v-1.) *0.01  -- cm/s -- > m/s

    alpha = 75.
    p = p + alpha*v

    p=p * math.min(1,t/0.5)
    
    return p
end


function Problem.Solver.MomContEq.BC.OutletP(x, y, z, t)
    T = 1.
    dt = -(0.12-0.010)
    alpha = 1.00
    omegat = 2*math.pi*(t-dt)/T
    p = 89.2632000000000 + 14.2636	* math.cos(omegat-3.06220) +
        .14560 * math.cos(2*omegat+1.16220) + 6.43040 * math.cos(3*omegat-0.6977) +
        3.91530 * math.cos(4*omegat-2.81270) + 1.36180 * math.cos(5*omegat+1.4279) +
        .672500 * math.cos(6*omegat+1.17040) + 1.20920 * math.cos(7*omegat-0.9584) +
        1.09780 * math.cos(8*omegat+2.85340) + .637100 * math.cos(9*omegat+0.6059) +
        .251900 * math.cos(10*omegat-0.8007) + .280800 * math.cos(11*omegat-2.3522) +
        .233100 * math.cos(12*omegat+1.8069) + .170100 * math.cos(13*omegat+0.3118) +
        .152000 * math.cos(14*omegat-1.2515) + .126500 * math.cos(15*omegat+2.9940) +
        .100800 * math.cos(16*omegat+1.3613) + .131100 * math.cos(17*omegat-0.1955)
    p = p * 133.33 * alpha
    p=p * math.min(1,t/0.5)
    
    return p
end


function Problem.Solver.MomContEq.BC.FixedV(x, y, z, t)
    return 0,0
end



function Problem.Mesh.computeHcharFromDistance(x,y,z,t,dist) -- Mesh non-uniforme
	c = Problem.Mesh.hchar
    fact = math.max (1,2*(1-dist/0.0075))
    h = c / fact
    return h
end
