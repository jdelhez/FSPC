-- Problem Parameters

Problem = {}
Problem.axiSymmetric = true
Problem.verboseOutput = true
Problem.autoRemeshing = false -- Mettre en false si fluide-structure
Problem.simulationTime = math.huge
Problem.id = "Casson"

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometryF.msh'
--Problem.Mesh.localHcharGroups = {'FSInterface','Reservoir','FreeSurface'} -- Mesh non-uniforme --> J'enleve? 
Problem.Mesh.boundingBox = {-0.001, -0.001, 0.0055, 0.09} -- Maybe a changer; jsp trop ce que doit contenit la bounding bow en axisym 
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.7
Problem.Mesh.gamma = 0.7
Problem.Mesh.hchar = 0.0005
Problem.Mesh.gammaFS = 0.5
Problem.Mesh.minHeightFactor = 1e-4

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

-- Pression et vitesse en y = 0.015  pour toutes les valeurs de x mais surtout au niveau de l'interface

Problem.Extractors[2] =  {}
Problem.Extractors[2].kind = 'Point'
Problem.Extractors[2].whatToWrite = 'p'
Problem.Extractors[2].outputFile = 'pCassonIncompAxiSym_y0015.txt'
Problem.Extractors[2].points = {{0, 0.015}, {0.00025, 0.015}, {0.0005, 0.015}, {0.00075, 0.015}, {0.001, 0.015}, {0.00125, 0.015}, {0.0015, 0.015}, {0.00175, 0.015}, {0.002, 0.015}, {0.00225, 0.015},{0.0025, 0.015}, {0.00275, 0.015},{0.003, 0.015},{0.00325, 0.015}, {0.0035, 0.015}, {0.00375, 0.015}, {0.004, 0.015}, {0.00425, 0.015}, {0.0045, 0.015}, {0.00475, 0.015},{0.005, 0.015}} 
Problem.Extractors[2].timeBetweenWriting =  math.huge

-- Idem en y = 0.03 pour toutes les valeurs de x mais surtout au niveau de l'interface

Problem.Extractors[3] =  {}
Problem.Extractors[3].kind = 'Point'
Problem.Extractors[3].whatToWrite = 'p'
Problem.Extractors[3].outputFile = 'pCassonAxiSym_y003.txt'
Problem.Extractors[3].points = {{0, 0.03}, {0.00025, 0.03}, {0.0005, 0.03}, {0.00075, 0.03}, {0.001, 0.03}, {0.00125, 0.03}, {0.0015, 0.03}, {0.00175, 0.03}, {0.002, 0.03}, {0.00225, 0.03},{0.0025, 0.03}, {0.00275, 0.03},{0.003, 0.03},{0.00325, 0.03}, {0.0035, 0.03}, {0.00375, 0.03}, {0.004, 0.03}, {0.00425, 0.03}, {0.0045, 0.03}, {0.00475, 0.03},{0.005, 0.03}} 
Problem.Extractors[3].timeBetweenWriting =  math.huge

-- Idem en y = 0.045 pour toutes les valeurs de x mais surtout au niveau de l'interface


Problem.Extractors[4] =  {}
Problem.Extractors[4].kind = 'Point'
Problem.Extractors[4].whatToWrite = 'p'
Problem.Extractors[4].outputFile = 'pCassonAxiSym_y0045.txt'
Problem.Extractors[4].points = {{0, 0.045}, {0.00025, 0.045}, {0.0005, 0.045}, {0.00075, 0.045}, {0.001, 0.045}, {0.00125, 0.045}, {0.0015, 0.045}, {0.00175, 0.045}, {0.002, 0.045}, {0.00225, 0.045},{0.0025, 0.045}, {0.00275, 0.045},{0.003, 0.045},{0.00325, 0.045}, {0.0035, 0.045}, {0.00375, 0.045}, {0.004, 0.045}, {0.00425, 0.045}, {0.0045, 0.045}, {0.00475, 0.045},{0.005, 0.045}} 
Problem.Extractors[4].timeBetweenWriting =  math.huge


-- Pression et vitesse en y = 0.015  pour toutes les valeurs de x mais surtout au niveau de l'interface

Problem.Extractors[5] =  {}
Problem.Extractors[5].kind = 'Point'
Problem.Extractors[5].whatToWrite = 'v'
Problem.Extractors[5].outputFile = 'vCassonAxiSym_y0015.txt'
Problem.Extractors[5].points = {{0, 0.015}, {0.00025, 0.015}, {0.0005, 0.015}, {0.00075, 0.015}, {0.001, 0.015}, {0.00125, 0.015}, {0.0015, 0.015}, {0.00175, 0.015}, {0.002, 0.015}, {0.00225, 0.015},{0.0025, 0.015}, {0.00275, 0.015},{0.003, 0.015},{0.00325, 0.015}, {0.0035, 0.015}, {0.00375, 0.015}, {0.004, 0.015}, {0.00425, 0.015}, {0.0045, 0.015}, {0.00475, 0.015},{0.005, 0.015}} 
Problem.Extractors[5].timeBetweenWriting =  math.huge

-- Idem en y = 0.03 pour toutes les valeurs de x mais surtout au niveau de l'interface

Problem.Extractors[6] =  {}
Problem.Extractors[6].kind = 'Point'
Problem.Extractors[6].whatToWrite = 'v'
Problem.Extractors[6].outputFile = 'vCassonAxiSym_y003.txt'
Problem.Extractors[6].points = {{0, 0.03}, {0.00025, 0.03}, {0.0005, 0.03}, {0.00075, 0.03}, {0.001, 0.03}, {0.00125, 0.03}, {0.0015, 0.03}, {0.00175, 0.03}, {0.002, 0.03}, {0.00225, 0.03},{0.0025, 0.03}, {0.00275, 0.03},{0.003, 0.03},{0.00325, 0.03}, {0.0035, 0.03}, {0.00375, 0.03}, {0.004, 0.03}, {0.00425, 0.03}, {0.0045, 0.03}, {0.00475, 0.03},{0.005, 0.03}} 
Problem.Extractors[6].timeBetweenWriting =  math.huge

-- Idem en y = 0.045 pour toutes les valeurs de x mais surtout au niveau de l'interface


Problem.Extractors[7] =  {}
Problem.Extractors[7].kind = 'Point'
Problem.Extractors[7].whatToWrite = 'v'
Problem.Extractors[7].outputFile = 'vCassonAxiSym_y0045.txt'
Problem.Extractors[7].points = {{0, 0.045}, {0.00025, 0.045}, {0.0005, 0.045}, {0.00075, 0.045}, {0.001, 0.045}, {0.00125, 0.045}, {0.0015, 0.045}, {0.00175, 0.045}, {0.002, 0.045}, {0.00225, 0.045},{0.0025, 0.045}, {0.00275, 0.045},{0.003, 0.045},{0.00325, 0.045}, {0.0035, 0.045}, {0.00375, 0.045}, {0.004, 0.045}, {0.00425, 0.045}, {0.0045, 0.045}, {0.00475, 0.045},{0.005, 0.045}} 
Problem.Extractors[7].timeBetweenWriting =  math.huge


-- Material Parameters
-- Laisser ca comme ca ? meme si ca ne permet pas de comparaison avec l'article 

Problem.Material = {}
--Problem.Material.mu = 0.003675
Problem.Material.mu = 0.0038
Problem.Material.gamma = 0
---Problem.Material.rho = 1000
Problem.Material.rho = 1050
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
Problem.Solver.coeffDTDecrease = math.huge
Problem.Solver.coeffDTincrease = math.huge

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.nlAlgo = 'NR'
-- Problem.Solver.MomContEq.nlAlgo = 'Picard'
Problem.Solver.MomContEq.residual = 'Ax_f'
-- Problem.Solver.MomContEq.sparseSolverLib = 'MKL'

--
Problem.Solver.MomContEq.tolerance = 1e-7 
Problem.Solver.MomContEq.gammaFS = 0.5 
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

    return {0, 0, 0}
end

-- Du coup je ne dois pas avoir de BC sur les FSIinterface? Ou quand même si? Car si je mets que vy = 0, comment ça pourrait se déformer?? 


function Problem.Solver.MomContEq.BC.InletP(x, y, z, t)
    -- p = 10
    if (t>0 and t<0.005) then
        p = 2000*(1-math.cos(2*3.1415926*t/0.005))/2
    else
        p = 0
    end
    return p
end

--function Problem.Solver.MomContEq.BC.FreeP(x, y, z, t)
  --  return 10
--end

function Problem.Solver.MomContEq.BC.OutletP(x, y, z, t)
    return 0
end

--function Problem.Mesh.computeHcharFromDistance(x,y,z,t,dist) -- Mesh non-uniforme
--	return Problem.Mesh.hchar+dist*0.1
-- end
