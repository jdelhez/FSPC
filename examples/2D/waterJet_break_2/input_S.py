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

    mshFile = os.path.join(os.path.dirname(__file__), 'geometry_S.msh')
    importer = gmsh.GmshImport(mshFile, domain)
    groups = importer.groups
    importer.execute()

    parm['FSInterface'] = groups['FSInterface']

    # Defines the ball domain

    iset = domain.getInteractionSet()
    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    iset.add(app)

    # Solid material parameters

    materset = domain.getMaterialSet()
    materset.define(1, w.EvpIsoHHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS, 210e9)
    materset(1).put(w.POISSON_RATIO, 0.284)
    materset(1).put(w.MASS_DENSITY, 7860)
    materset(1).put(w.YIELD_NUM, 1)

    # Visco-plastic hardening of C1010 Steel
    
    lawset = domain.getMaterialLawSet()
    lawset.define(1, w.JohnsonCookMecYieldStress)
    lawset(1).put(w.JC_A, 367e6)
    lawset(1).put(w.JC_B, 275e6)
    lawset(1).put(w.JC_C, 0.022)
    lawset(1).put(w.JC_EPSP0, 1)
    lawset(1).put(w.JC_N, 0.36)
    lawset(1).put(w.JC_C2, 0)

    # Select a rupture criterion

    rc = w.IFRuptureCriterion()
    rc.setInternalField(w.IF_EPL)
    rc.put(w.RUPT_CRIT_VALUE, 0.33)
    rc.put(w.RUPT_TYPE_CRIT, w.MEANBROKEN)
    app.addRuptureCriterion(rc)
    app.setAutoRupture(False)

    parm['rupture'] = app

    # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp1.put(w.GRAVITY_Y, -9.81)
    prp1.put(w.MATERIAL, 1)
    app.addProperty(prp1)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(2)
    load.push(groups['Solid'])
    load.addProperty(prp2)
    iset.add(load)

    parm['interaction_M'] = load
    parm['polytope'] = load.getElementSet()

    # Boundary conditions

    loadingset = domain.getLoadingSet()
    loadingset.define(groups['Side'], w.Field1D(w.TX, w.RE))
    loadingset.define(groups['Side'], w.Field1D(w.TY, w.RE))

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor)
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim = metafor.getMechanicalIterationManager()
    mim.setMaxNbOfIterations(25)
    mim.setResidualTolerance(1e-3)

    # Time step iterations
    
    tsm = metafor.getTimeStepManager()
    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Nodal GMSH extractor

    ext = w.GmshNodalExtractor(metafor, 'metafor/output')
    ext.add(1, w.IFNodalValueExtractor(groups['Solid'], w.IF_EPL))
    ext.add(2, w.IFNodalValueExtractor(groups['Solid'], w.IF_EVMS))
    ext.add(3, w.DbNodalValueExtractor(groups['Solid'], w.Field1D(w.TY, w.GF1)))
    ext.add(4, w.DbNodalValueExtractor(groups['Solid'], w.Field1D(w.TY, w.GF2)))
    parm['extractor'] = ext

    # Build domain and folder

    domain.build()
    load.getElementSet().activateBoundaryElements()
    os.makedirs('metafor')
    return metafor
