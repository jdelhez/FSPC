import toolbox.gmsh as gmsh
import wrap as w
import os


# |------------------------------------------|
# |   Initialization and Input Parameters    |
# |------------------------------------------|

metafor = None  # Toujours copier/coller ça
def getMetafor(parm):

    global metafor # Toujours copier/coller ça
    if metafor: return metafor
    metafor = w.Metafor()

    w.StrVectorBase.useTBB() # Active la paralélisation de certaisn conteneurs
    w.StrMatrixBase.useTBB()
    w.ContactInteraction.useTBB()

    # Dimension and DSS solver

    domain = metafor.getDomain()
    domain.getGeometry().setDimAxisymmetric()# Pour du 2D Axisymmetric
    metafor.getSolverManager().setSolver(w.DSSolver()) # Active le solveur MKL (le plus rapide)

    # Imports the mesh

    # mshFile = le chemin vers geometryS.msh
    # C'est une façon de récupérer automatiquement le chemin vers
    # le dossier courrant, puisque geometryS.msh est dedans

    mshFile = os.path.join(os.path.dirname(__file__),'geometryS.msh')
    importer = gmsh.GmshImport(mshFile,domain)
    groups = importer.groups # Contient tous les physical groups de Gmsh
    importer.execute() # Importation du maillage Gmsh dans Metafor

    # Defines the solid domain

    # Il faut y placer le physical group du volume (ou de la surface en 2D)
    # Voir exemple dans 2D/flowContact avec plusieurs matériaux
    # Un FieldApplicator pour chaque matériau différent

    # Que faire si on a deux surfaces solides? 

    iset = domain.getInteractionSet()
    app1 = w.FieldApplicator(1)
    app1.push(groups['Solid'])
    iset.add(app1)
  

    # Material parameters

    E = 2.7e6
    rho = 1200
    nu = 0.45

    G = E/(2*(1+nu))
    K = E/(3*(1-2*nu)) 

    materset = domain.getMaterialSet()
   
    C1 = 584e3
    C2 = G/2.0-C1

    materset.define(1, w.MooneyRivlinHyperMaterial)
    materset(1).put(w.MASS_DENSITY, rho)
    materset(1).put(w.RUBBER_PENAL, K)
    materset(1).put(w.RUBBER_C1, C1)
    materset(1).put(w.RUBBER_C2, C2)

    # materset = domain.getMaterialSet()
    # materset.define(1,w.ElastHypoMaterial)
    # materset(1).put(w.ELASTIC_MODULUS,E)
    # materset(1).put(w.MASS_DENSITY,rho)
    # materset(1).put(w.POISSON_RATIO,nu)

  # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    # prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.STIFFMETHOD,w.STIFF_NUMERIC)
    prp1.put(w.MATERIAL,1)
    app1.addProperty(prp1)
                 
    # Elements for surface traction
    # Interface qui va reçevoir les contraintes de PFEM3D

    prp2 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.addProperty(prp2)
    iset.add(load)

    
    # Boundary conditions 
    # On bloque la base du solide --> Je dois bloquer quoi moi du coup? Les côtés "side" non? 
    
    loadingset = domain.getLoadingSet()
    loadingset.define(groups['Sides'],w.Field1D(w.TX,w.RE)) # Pas de déplacement selon X
    loadingset.define(groups['Sides'],w.Field1D(w.TY,w.RE)) # Pas de déplacement selon Y
    

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

    #parm['interacM'] = load
    parm['interaction_M'] = load
    
    parm['FSInterface'] = groups['FSInterface']
    parm['extractor'] = gmsh.GmshNodalExtractor(metafor,'metafor/output.msh',)
    
    #parm['polytope'] = load.getElementSet() ?? 

    #  Contrainte de Von Mises (0) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_EVMS)
    parm['extractor'].add(extr)

    #  Contrainte SigmaYY (1) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_SIG_YY)
    parm['extractor'].add(extr)

    #  Contrainte SigmaZZ (2) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_SIG_ZZ)
    parm['extractor'].add(extr)

    #  Contrainte SigmaXY (3) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_SIG_XY)
    parm['extractor'].add(extr)

    #  Contrainte SigmaXX (4) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_SIG_XX)
    parm['extractor'].add(extr)
    
    #  Contrainte SigmaXX (5) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_SIG_ORTHO_XY)
    parm['extractor'].add(extr)
    
    domain.build()
    os.makedirs('metafor')
    return metafor




