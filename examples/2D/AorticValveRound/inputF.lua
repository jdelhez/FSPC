-- Problem Parameters

Problem = {}
Problem.verboseOutput = true
Problem.autoRemeshing = false -- Mettre en false si fluide-structure
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'CGAL'
Problem.Mesh.mshFile = 'geometryF.msh'
--Problem.Mesh.localHcharGroups = {'FSInterface','Reservoir','FreeSurface'} -- Mesh non-uniforme --> J'enleve? 
Problem.Mesh.boundingBox = {-0.043, -0.025 , 0.043, 0.025}
Problem.Mesh.exclusionZones = {}



Problem.Mesh.alpha = 1.3
Problem.Mesh.omega = 0.7
Problem.Mesh.gamma = 0.9
Problem.Mesh.hchar = 1e-3
Problem.Mesh.gammaFS = 0.5
Problem.Mesh.minHeightFactor = 1e-3


Problem.Mesh.addOnFS = false
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = true
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
Problem.Solver.MomContEq.maxIter = 25
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
    T = 0.85;
    omega = 2*math.pi/T
    tf = t 

    pout = 96.2370 + 
    14.6545 * math.cos( omega*tf-2.0739) +
    6.7286 * math.cos(2*omega*tf-2.7146) +
    4.6804 * math.cos(3*omega*tf+2.8162) +
    2.8994 * math.cos(4*omega*tf+1.6577) +
    0.6598 * math.cos(5*omega*tf-0.0469) +
    0.8857 * math.cos(6*omega*tf+2.0975) +
    0.7511 * math.cos(7*omega*tf+0.4694)

    p= pout * 133.3
    p = p * math.min(1,t/0.1)
    return p
end

function Problem.Solver.MomContEq.BC.BoundaryV(x, y, z, t)
    return 0, 0
end

function Problem.Solver.MomContEq.BC.InletP(x, y, z, t)
    T = 0.85;
    omega = 2*math.pi/T
    tf = t + 0.01
    tf = t 

    pin = 35.70000 + 
    58.5464 * math.cos(  omega*tf-1.2271) +
    31.0920 * math.cos(2*omega*tf-2.4152) +
    6.6977 * math.cos(3*omega*tf-3.1301) +
    6.8385 * math.cos(4*omega*tf-2.2885) +
    4.8078 * math.cos(5*omega*tf-3.1124) +
    1.9073 * math.cos(6*omega*tf-2.5235) +
    2.9315 * math.cos(7*omega*tf-2.9273)

    tf = t
    pout = 96.2370 + 
    14.6545 * math.cos( omega*t-2.0739) +
    6.7286 * math.cos(2*omega*t-2.7146) +
    4.6804 * math.cos(3*omega*t+2.8162) +
    2.8994 * math.cos(4*omega*t+1.6577) +
    0.6598 * math.cos(5*omega*t-0.0469) +
    0.8857 * math.cos(6*omega*t+2.0975) +
    0.7511 * math.cos(7*omega*t+0.4694)


    pin = math.max(pin,pout-4)

    p= pin * 133.3
    p = p * math.min(1,t/0.1)
    return p
 end

-- function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)
--     tr  = t-math.floor(t)
--     if (tr<0.41) then
--         vx=179.212434923075 + 
--         346.133181397307 * math.cos(6.28318530717959*tr-1.03814633164985)+ 
--         273.464992134736 * math.cos(12.5663706143592*tr-2.11882642434818)+ 
--         170.398012407865 * math.cos(18.8495559215388*tr+3.01708979440978)+ 
--         71.0138350893899 * math.cos(25.1327412287183*tr+1.68057926325852)
--         vx = vx / 1000
--     else
--         vx = 0
--     end
--     return vx, 0
-- end



--function Problem.Mesh.computeHcharFromDistance(x,y,z,t,dist) -- Mesh non-uniforme
--	return Problem.Mesh.hchar+dist*0.1
-- end
