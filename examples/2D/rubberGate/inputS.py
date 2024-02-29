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

    # Dimension and DSS solver

    domain = metafor.getDomain()
    domain.getGeometry().setDimPlaneStrain(1)
    metafor.getSolverManager().setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__),'geometryS.msh')
    importer = gmsh.GmshImport(mshFile,domain)
    groups = importer.groups
    importer.execute()

    # Defines the solid domain

    iset = domain.getInteractionSet()
    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    iset.add(app)
    
    # Material parameters

    K = 1.3e6
    G = 2.4e6
    C1 = -1.2e6
    C2 = G/2.0-C1

    materset = domain.getMaterialSet()
    materset.define(1,w.MooneyRivlinHyperMaterial)
    materset(1).put(w.MASS_DENSITY,1100)
    materset(1).put(w.RUBBER_PENAL,K)
    materset(1).put(w.RUBBER_C1,C1)
    materset(1).put(w.RUBBER_C2,C2)
    
    # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_NUMERIC)
    prp1.put(w.GRAVITY_Y,-9.81)
    prp1.put(w.MATERIAL,1)
    app.addProperty(prp1)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.addProperty(prp2)
    iset.add(load)
    
    # Boundary conditions
    
    loadingset = domain.getLoadingSet()
    loadingset.define(groups['Base'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['Base'],w.Field1D(w.TY,w.RE))

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor)
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim = metafor.getMechanicalIterationManager()
    mim.setResidualTolerance(1e-8)
    mim.setMaxNbOfIterations(25)

    # Time step iterations

    tsm = metafor.getTimeStepManager()
    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Parameters for FSPC

    parm['interacM'] = load
    parm['FSInterface'] = groups['FSInterface']
    parm['exporter'] = gmsh.NodalGmshExport('metafor/output.msh',metafor)
    parm['polytope'] = None

    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_P)
    parm['exporter'].addExtractor(extr)

    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_EVMS)
    parm['exporter'].addExtractor(extr)

    domain.build()
    return metafor