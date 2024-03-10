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

    
    app2 = w.FieldApplicator(2)
    app2.push(groups['Solid2'])
    iset.add(app2)

    # Material parameters
    # Matériau appliqué au physical group "Solid"
    # Pas moyen de définir un matériau unique et de l'appliquer aux deux surfaces? 

     # Solid material parameters

    materset = domain.getMaterialSet()
    materset.define(1,w.ElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS,100e3) #### 675e3
    materset(1).put(w.MASS_DENSITY,1100)
    materset(1).put(w.POISSON_RATIO,0.49)

    materset.define(2,w.ElastHypoMaterial)
    materset(2).put(w.ELASTIC_MODULUS,100e3) #### 675e3
    materset(2).put(w.MASS_DENSITY,1100)
    materset(2).put(w.POISSON_RATIO,0.49)

    # materset.define (2, EvpIsoHHypoMaterial)
    # materset(2).put(MASS_DENSITY, 1100)
    # materset(2).put(ELASTIC_MODULUS, 10e3)
    # materset(2).put(POISSON_RATIO, 0.3)
    # materset(2).put(YIELD_NUM, 1)

    # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL,1)
    app1.addProperty(prp1)

    
    prp2 = w.ElementProperties(w.Volume2DElement)
    prp2.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp2.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp2.put(w.MATERIAL,2)
    app2.addProperty(prp2)

        
   
    # Elements for surface traction
    # Interface qui va reçevoir les contraintes de PFEM3D
    # Je comprends pas en fait la suite; j'essaie de recopier Flow Contact mais bof !!!! HELP 

    prp3 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(3)
    load.push(groups['FSInterface'])
    load.addProperty(prp3)
    iset.add(load)

    #Maybe je dois separer en deux groupes? En haut et en bas? I don't knowww ; genre faire comme ça:  ??? 


    # Boundary conditions 
    # On bloque la base du solide --> Je dois bloquer quoi moi du coup? Les côtés "side" non? 
    
    loadingset = domain.getLoadingSet()
    loadingset.define(groups['Sides'],w.Field1D(w.TX,w.RE)) # Pas de déplacement selon X
    loadingset.define(groups['Sides'],w.Field1D(w.TY,w.RE)) # Pas de déplacement selon Y
    # loadingset.define(groups['Axis'],w.Field1D(w.TX,w.RE)) --> Le axis ne fait pas partie du solide... comment imposer la symetrie pour le solide?? Rien à imposer.



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
    #parm['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    parm['polytope'] = None
    #parm['polytope'] = load.getElementSet() ?? 

    #  Contrainte de Von Mises (0) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_EVMS)
    parm['exporter'].addExtractor(extr)

    #  Contrainte SigmaYY (1) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_SIG_YY)
    parm['exporter'].addExtractor(extr)

    #  Contrainte SigmaZZ (2) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_SIG_ZZ)
    parm['exporter'].addExtractor(extr)

    #  Contrainte SigmaXY (3) 
    extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_SIG_XY)
    parm['exporter'].addExtractor(extr)





    #parm['exporter'] = gmsh.NodalGmshExport('metafor/output.msh',metafor)
    
    # parm['exporter'] = gmsh.GmshExport('metafor/output.msh',metafor)
    # parm['exporter'].addInternalField([w.IF_EVMS,w.IF_P,w.IF_SIG_XX])

    
    #extr = w.IFNodalValueExtractor(groups['Solid'],w.IF_EVMS)
    #parm['exporter'].addExtractor(extr)

    #extr = w.DbNodalValueExtractor(groups['Solid'],w.Field1D(w.TX,w.GF1))
    #parm['exporter'].addExtractor(extr)

    #extr = w.DbNodalValueExtractor(groups['Solid'],w.Field1D(w.TY,w.GF1))
    #parm['exporter'].addExtractor(extr)
    
    domain.build()

    return metafor




