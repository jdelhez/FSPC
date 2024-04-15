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
    app1.push(groups['Intima'])
    iset.add(app1)
    app2 = w.FieldApplicator(2)
    app2.push(groups['Media'])
    iset.add(app2)
    app3 = w.FieldApplicator(3)
    app3.push(groups['Adventitia'])
    iset.add(app3)
  

    # Material parameters


    materset = domain.getMaterialSet()

    E = 1.174e6
    rho = 1200
    nu = 0.45
    G = E/(2*(1+nu))
    K = E/(3*(1-2*nu)) 
    C1 = 584e3*1.174/2.7
    C2 = G/2.0-C1


    materset.define(1, w.MooneyRivlinHyperMaterial)
    materset(1).put(w.MASS_DENSITY, rho)
    materset(1).put(w.RUBBER_PENAL, K)
    materset(1).put(w.RUBBER_C1, C1)
    materset(1).put(w.RUBBER_C2, C2)

    E = 3.522e6
    rho = 1200
    nu = 0.45
    G = E/(2*(1+nu))
    K = E/(3*(1-2*nu)) 
    C1 = 584e3*3.522/2.7
    C2 = G/2.0-C1

    materset.define(2, w.MooneyRivlinHyperMaterial)
    materset(2).put(w.MASS_DENSITY, rho)
    materset(2).put(w.RUBBER_PENAL, K)
    materset(2).put(w.RUBBER_C1, C1)
    materset(2).put(w.RUBBER_C2, C2)

    E = 2.348e6
    rho = 1200
    nu = 0.45
    G = E/(2*(1+nu))
    K = E/(3*(1-2*nu)) 
    C1 = 584e3*2.348/2.7
    C2 = G/2.0-C1

    materset.define(3, w.MooneyRivlinHyperMaterial)
    materset(3).put(w.MASS_DENSITY, rho)
    materset(3).put(w.RUBBER_PENAL, K)
    materset(3).put(w.RUBBER_C1, C1)
    materset(3).put(w.RUBBER_C2, C2)
  # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_NUMERIC)
    prp1.put(w.MATERIAL,1)
    app1.addProperty(prp1)

    prp2 = w.ElementProperties(w.Volume2DElement)
    prp2.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp2.put(w.STIFFMETHOD,w.STIFF_NUMERIC)
    prp2.put(w.MATERIAL,2)
    app2.addProperty(prp2)

    prp3 = w.ElementProperties(w.Volume2DElement)
    prp3.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp3.put(w.STIFFMETHOD,w.STIFF_NUMERIC)
    prp3.put(w.MATERIAL,3)
    app3.addProperty(prp3)
                 
    # Elements for surface traction
    # Interface qui va reçevoir les contraintes de PFEM3D
    # Je comprends pas en fait la suite; j'essaie de recopier Flow Contact mais bof !!!! HELP 

    prp4 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(4)
    load.push(groups['FSInterface'])
    load.addProperty(prp4)
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
    extr = w.IFNodalValueExtractor(groups['Intima'],w.IF_EVMS) 
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Media'],w.IF_EVMS) 
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Adventitia'],w.IF_EVMS) 
    parm['extractor'].add(extr)

    #  Contrainte SigmaYY (1) 
    extr = w.IFNodalValueExtractor(groups['Intima'],w.IF_SIG_YY)
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Media'],w.IF_SIG_YY)
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Adventitia'],w.IF_SIG_YY)
    parm['extractor'].add(extr)

    #  Contrainte SigmaZZ (1) 
    extr = w.IFNodalValueExtractor(groups['Intima'],w.IF_SIG_ZZ)
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Media'],w.IF_SIG_ZZ)
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Adventitia'],w.IF_SIG_ZZ)
    parm['extractor'].add(extr)

    #  Contrainte SigmaXY (3) 
    extr = w.IFNodalValueExtractor(groups['Intima'],w.IF_SIG_XY)
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Media'],w.IF_SIG_XY)
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Adventitia'],w.IF_SIG_XY)
    parm['extractor'].add(extr)

    #  Contrainte SigmaXX (4) 
    extr = w.IFNodalValueExtractor(groups['Intima'],w.IF_SIG_XX)
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Media'],w.IF_SIG_XX)
    parm['extractor'].add(extr)
    extr = w.IFNodalValueExtractor(groups['Adventitia'],w.IF_SIG_XX)
    parm['extractor'].add(extr)
    
    domain.build()
    os.makedirs('metafor')
    return metafor




