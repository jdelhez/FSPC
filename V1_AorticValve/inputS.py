import toolbox.gmsh as gmsh
import wrap as w
import os

# |------------------------------------------|
# |   Initialization and Input Parameters    |
# |------------------------------------------|

metafor = None
def getMetafor(parm):

    global metafor
    if metafor: return metafor
    metafor = w.Metafor()

    w.StrVectorBase.useTBB()
    w.StrMatrixBase.useTBB()
    w.ContactInteraction.useTBB()

    # Dimension and DSS solver

    domain = metafor.getDomain()
    domain.getGeometry().setDimPlaneStrain(1)
    metafor.getSolverManager().setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__), 'geometryS.msh')
    importer = gmsh.GmshImport(mshFile,domain)
    groups = importer.groups
    importer.execute()

    # Defines the solid domain

    iset = domain.getInteractionSet()
    app1 = w.FieldApplicator(1)
    app1.push(groups['Solid'])
    iset.add(app1)

    # Material parameters

    EYoung = 1e7
    rho = 1060

    materset = domain.getMaterialSet()
    materset.define(1, w.ElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS, EYoung)
    materset(1).put(w.MASS_DENSITY, rho)
    materset(1).put(w.POISSON_RATIO, 0.3)

    # Proprietes d'un vaisseau sanguin a check ailleurs ! 

    # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL, 1)
    app1.addProperty(prp1)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress2DElement)
    load1 = w.NodInteraction(2)
    load1.push(groups['Leafet_Top'])
    load1.addProperty(prp2)
    iset.add(load1)

    prp3 = w.ElementProperties(w.NodStress2DElement)
    load2 = w.NodInteraction(3)
    load2.push(groups['Leafet_Bot'])
    load2.addProperty(prp3)
    iset.add(load2)
    
    # Contact parameters

    penalty = 1.5*EYoung
    
    # friction = 0.35
    # materset.define(3,w.CoulombContactMaterial)
    # materset(3).put(w.PEN_TANGENT,friction*penalty)
    # materset(3).put(w.COEF_FROT_DYN,friction)
    # materset(3).put(w.COEF_FROT_STA,friction)
    # materset(3).put(w.PEN_NORMALE,penalty)
    # materset(3).put(w.PROF_CONT,0.0005)

    materset.define(2, w.StickingContactMaterial)
    materset(2).put(w.PEN_TANGENT, 4*penalty)
    materset(2).put(w.PEN_NORMALE, 5*penalty)
    materset(2).put(w.PROF_CONT, 0.0005)

    prp4 = w.ElementProperties(w.Contact2DElement)
    prp4.put(w.AREAINCONTACT,w.AIC_ONCE)
    prp4.put(w.MATERIAL, 2)

    # Defines the contact entities

    ci = w.DdContactInteraction(4)
    ci.setTool(groups['Contact_Top'])
    ci.push(groups['Contact_Bot'])
    ci.setSmoothNormals(True)
    ci.setSinglePass()
    ci.addProperty(prp4)
    iset.add(ci)

    # Boundary conditions 
    
    loadingset = domain.getLoadingSet()
    loadingset.define(groups['Sides'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['Sides'],w.Field1D(w.TY,w.RE))

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor)
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim = metafor.getMechanicalIterationManager()
    mim.setResidualTolerance(1e-6)
    mim.setMaxNbOfIterations(25)

    # Time step iterations

    tsm = metafor.getTimeStepManager()
    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Parameters for FSPC

    parm['interaction_M'] = [load1, load2]
    parm['FSInterface'] = groups['FSInterface']
    #parm['polytope'] = [load1.getElementSet(), load2.getElementSet()]

    # Nodal GMSH extractor

    ext = w.GmshNodalExtractor(metafor, 'metafor/output')
    ext.add(1, w.IFNodalValueExtractor(groups['Solid'],w.IF_EVMS))
    parm['extractor'] = ext

    # Build domain and folder

    domain.build()
    os.makedirs('metafor')
    return metafor