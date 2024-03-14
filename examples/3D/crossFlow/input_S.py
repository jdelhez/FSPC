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
    domain.getGeometry().setDim3D()
    metafor.getSolverManager().setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__), 'geometry_S.msh')
    importer = gmsh.GmshImport(mshFile, domain)
    groups = importer.groups
    importer.execute()

    parm['FSInterface'] = groups['FSInterface']

    # Defines the solid domain

    iset = domain.getInteractionSet()
    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    iset.add(app)

    # Material parameters

    materset = domain.getMaterialSet()
    materset.define(1, w.ElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS, 1.23e6)
    materset(1).put(w.POISSON_RATIO, 0.3)
    materset(1).put(w.MASS_DENSITY, 1030)
    
    # Finite element properties

    prp = w.ElementProperties(w.Volume3DElement)
    prp.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_EAS)
    prp.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp.put(w.TOTAL_LAGRANGIAN, True)
    prp.put(w.GRAVITY_Z, -9.81)
    prp.put(w.MATERIAL, 1)
    prp.put(w.PEAS, 1e-9)
    app.addProperty(prp)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress3DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.push(groups['Clamped'])
    load.addProperty(prp2)
    iset.add(load)

    parm['interaction_M'] = load
    parm['polytope'] = load.getElementSet()
    
    # Boundary conditions
    
    loadset = domain.getLoadingSet()
    loadset.define(groups['Clamped'], w.Field1D(w.TX, w.RE))
    loadset.define(groups['Clamped'], w.Field1D(w.TY, w.RE))
    loadset.define(groups['Clamped'], w.Field1D(w.TZ, w.RE))

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

    # Nodal GMSH extractor

    ext = w.GmshNodalExtractor(metafor, 'metafor/output')
    ext.add(1, w.IFNodalValueExtractor(groups['Solid'], w.IF_P))
    ext.add(2, w.IFNodalValueExtractor(groups['Solid'], w.IF_EVMS))
    parm['extractor'] = ext

    # Build domain and folder

    domain.build()
    os.makedirs('metafor')
    return metafor