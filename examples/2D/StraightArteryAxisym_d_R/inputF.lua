-- Problem Parameters

Problem = {}
Problem.axiSymmetric = true
Problem.verboseOutput = true
Problem.autoRemeshing = false -- Mettre en false si fluide-structure
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometryF.msh'
--Problem.Mesh.localHcharGroups = {'FSInterface','Reservoir','FreeSurface'} -- Mesh non-uniforme --> J'enleve? 
Problem.Mesh.boundingBox = {-0.001, -0.001, 0.0055, 0.09} -- Maybe a changer; jsp trop ce que doit contenit la bounding bow en axisym 
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.3 -- 1.0
Problem.Mesh.omega = 0.7 -- 0.7
Problem.Mesh.gamma = 0.9 -- 0.7
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
Problem.Extractors[2].outputFile = 'pNewtonIncompAxiSym_y0015.txt'
Problem.Extractors[2].points = {{0, 0.015}, {0.0005, 0.015}, {0.001, 0.015}, {0.0015, 0.015}, {0.002, 0.015}, {0.0025, 0.015}, {0.003, 0.015}, {0.0035, 0.015}, {0.004, 0.015}, {0.0045, 0.015}, {0.005, 0.015}} 
Problem.Extractors[2].timeBetweenWriting =  math.huge

-- Idem en y = 0.03 pour toutes les valeurs de x mais surtout au niveau de l'interface

Problem.Extractors[3] =  {}
Problem.Extractors[3].kind = 'Point'
Problem.Extractors[3].whatToWrite = 'p'
Problem.Extractors[3].outputFile = 'pNewtonAxiSym_y003.txt'
Problem.Extractors[3].points = {{0, 0.03}, {0.0005, 0.03}, {0.001, 0.03}, {0.0015, 0.03}, {0.002, 0.03}, {0.0025, 0.03}, {0.003, 0.03}, {0.0035, 0.03}, {0.004, 0.03}, {0.0045, 0.03}, {0.005, 0.03}} 
Problem.Extractors[3].timeBetweenWriting =  math.huge

-- Idem en y = 0.045 pour toutes les valeurs de x mais surtout au niveau de l'interface


Problem.Extractors[4] =  {}
Problem.Extractors[4].kind = 'Point'
Problem.Extractors[4].whatToWrite = 'p'
Problem.Extractors[4].outputFile = 'pNewtonAxiSym_y0045.txt'
Problem.Extractors[4].points = {{0, 0.045}, {0.0005, 0.045}, {0.001, 0.045}, {0.0015, 0.045}, {0.002, 0.045}, {0.0025, 0.045}, {0.003, 0.045}, {0.0035, 0.045}, {0.004, 0.045}, {0.0045, 0.045}, {0.005, 0.045}} 
Problem.Extractors[4].timeBetweenWriting =  math.huge


-- Pression et vitesse en y = 0.015  pour toutes les valeurs de x mais surtout au niveau de l'interface

Problem.Extractors[5] =  {}
Problem.Extractors[5].kind = 'Point'
Problem.Extractors[5].whatToWrite = 'v'
Problem.Extractors[5].outputFile = 'vNewtonAxiSym_y0015.txt'
Problem.Extractors[5].points = {{0, 0.015}, {0.0005, 0.015}, {0.001, 0.015}, {0.0015, 0.015}, {0.002, 0.015}, {0.0025, 0.015}, {0.003, 0.015}, {0.0035, 0.015}, {0.004, 0.015}, {0.0045, 0.015}, {0.005, 0.015}} 
Problem.Extractors[5].timeBetweenWriting =  math.huge

-- Idem en y = 0.03 pour toutes les valeurs de x mais surtout au niveau de l'interface

Problem.Extractors[6] =  {}
Problem.Extractors[6].kind = 'Point'
Problem.Extractors[6].whatToWrite = 'v'
Problem.Extractors[6].outputFile = 'vNewtonAxiSym_y003.txt'
Problem.Extractors[6].points = {{0, 0.03}, {0.0005, 0.03}, {0.001, 0.03}, {0.0015, 0.03}, {0.002, 0.03}, {0.0025, 0.03}, {0.003, 0.03}, {0.0035, 0.03}, {0.004, 0.03}, {0.0045, 0.03}, {0.005, 0.03}} 
Problem.Extractors[6].timeBetweenWriting =  math.huge

-- Idem en y = 0.045 pour toutes les valeurs de x mais surtout au niveau de l'interface


Problem.Extractors[7] =  {}
Problem.Extractors[7].kind = 'Point'
Problem.Extractors[7].whatToWrite = 'v'
Problem.Extractors[7].outputFile = 'vNewtonAxiSym_y0045.txt'
Problem.Extractors[7].points = {{0, 0.045}, {0.0005, 0.045}, {0.001, 0.045}, {0.0015, 0.045}, {0.002, 0.045}, {0.0025, 0.045}, {0.003, 0.045}, {0.0035, 0.045}, {0.004, 0.045}, {0.0045, 0.045}, {0.005, 0.045}} 
Problem.Extractors[7].timeBetweenWriting =  math.huge


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
    td = 0 + 0.21
    p0= 0
    --p0 = 6471.68782493127*math.cos(0*td + 0) + 
    --4546.40390397331*math.cos(5.80640640376384*td + 2.88303288234243) + 
    --2912.28391822816*math.cos(11.6128128075277*td + 0.437321132460916) + 
    --1999.49340669353*math.cos(17.4192192112915*td -1.80886753960572) + 
    --1365.06363497520*math.cos(23.2256256150554*td + 2.00090876389695) + 
    --674.792594796269*math.cos(29.0320320188192*td -0.524481534622267) + 
    --144.936378283116*math.cos(34.8384384225831*td -2.31301923374297) + 
    --320.573352689215*math.cos(40.6448448263469*td + 2.87413985644085) + 
    --380.090549614032*math.cos(46.4512512301107*td + 0.221634032043418) + 
    --286.600758107930*math.cos(52.2576576338746*td -2.47517628449584) 
    v0 = 0.0685123642679439*math.cos(0*td + 0) + 
    0.126514121510227*math.cos(5.74759839519073*td -2.17096143198117) + 
    0.125541265762513*math.cos(11.4951967903815*td + 1.45334193151593) + 
    0.0453077057278536*math.cos(17.2427951855722*td -0.806586010701596) + 
    0.0494034611660211*math.cos(22.9903935807629*td -2.69330226694046) + 
    0.0224653857684426*math.cos(28.7379919759537*td + 1.07426355614492) + 
    0.0134055314219953*math.cos(34.4855903711444*td - 0.567424391681387) + 
    0.00593831629572069*math.cos(40.2331887663351*td + 2.75397232683334)  

    return {0, v0, p0}
end

-- Du coup je ne dois pas avoir de BC sur les FSIinterface? Ou quand même si? Car si je mets que vy = 0, comment ça pourrait se déformer?? 

-- function Problem.Solver.MomContEq.BC.InletV(x,y,z,t)
--    return 0,0.1
-- end

function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)
    if (x<0.0045) then
        td = t + 0.21 
        v = 0.0685123642679439*math.cos(0*td + 0) + 
        0.126514121510227*math.cos(5.74759839519073*td -2.17096143198117) + 
        0.125541265762513*math.cos(11.4951967903815*td + 1.45334193151593) + 
        0.0453077057278536*math.cos(17.2427951855722*td -0.806586010701596) + 
        0.0494034611660211*math.cos(22.9903935807629*td -2.69330226694046) + 
        0.0224653857684426*math.cos(28.7379919759537*td + 1.07426355614492) + 
        0.0134055314219953*math.cos(34.4855903711444*td - 0.567424391681387) + 
        0.00593831629572069*math.cos(40.2331887663351*td + 2.75397232683334)  
    else
        v=0
    end
    return 0, v
 end



--function Problem.Solver.MomContEq.BC.FreeP(x, y, z, t)
  --  return 10
--end

function Problem.Solver.MomContEq.BC.OutletP(x, y, z, t)
    td = t + 0.21
    p = 6471.68782493127*math.cos(0*td + 0) + 
        4546.40390397331*math.cos(5.80640640376384*td + 2.88303288234243) + 
        2912.28391822816*math.cos(11.6128128075277*td + 0.437321132460916) + 
        1999.49340669353*math.cos(17.4192192112915*td -1.80886753960572) + 
        1365.06363497520*math.cos(23.2256256150554*td + 2.00090876389695) + 
        674.792594796269*math.cos(29.0320320188192*td -0.524481534622267) + 
        144.936378283116*math.cos(34.8384384225831*td -2.31301923374297) + 
        320.573352689215*math.cos(40.6448448263469*td + 2.87413985644085) + 
        380.090549614032*math.cos(46.4512512301107*td + 0.221634032043418) + 
        286.600758107930*math.cos(52.2576576338746*td -2.47517628449584) 
    p = p*0.7
    return p
end

--function Problem.Mesh.computeHcharFromDistance(x,y,z,t,dist) -- Mesh non-uniforme
--	return Problem.Mesh.hchar+dist*0.1
-- end
