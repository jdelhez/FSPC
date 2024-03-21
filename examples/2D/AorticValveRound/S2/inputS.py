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
    domain.getGeometry().setDimPlaneStrain(1)  # Pour du 2D
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
    app1.push(groups['SolidUp'])
    iset.add(app1)

    app2 = w.FieldApplicator(2)
    app2.push(groups['SolidBottom'])
    iset.add(app2)

    # Material parameters
    # Matériau appliqué au physical group "Solid"
    # Pas moyen de définir un matériau unique et de l'appliquer aux deux surfaces? 

    materset = domain.getMaterialSet()
    materset.define(1,w.ElastHypoMaterial) # Le "1" pour FieldApplicator(1)
    materset(1).put(w.ELASTIC_MODULUS, 5e6) #750e3
    materset(1).put(w.MASS_DENSITY,1100)
    materset(1).put(w.POISSON_RATIO,0.45)

    materset.define(2,w.ElastHypoMaterial)
    materset(2).put(w.ELASTIC_MODULUS,5e6)#750e3
    materset(2).put(w.MASS_DENSITY,1100)
    materset(2).put(w.POISSON_RATIO,0.45)
    



    # Proprietes d'un vaisseau sanguin a check ailleurs ! 
    
    # Pas de "contact parameter" (voir FlowContact !)

    # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement) # Quadrangles 2D
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC) # Calcul analytique de la matrice de raideur tangente
     #prp1.put(w.GRAVITY_Y,-9.81)  #Bouger la gravité ou non?? 
    prp1.put(w.MATERIAL,1) # Le "1" pour materset(1)
    app1.addProperty(prp1)

    prp2 = w.ElementProperties(w.Volume2DElement)
    prp2.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp2.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp2.put(w.MATERIAL,2)
    app2.addProperty(prp2)

    # Elements for surface traction
    # Interface qui va reçevoir les contraintes de PFEM3D
    # Je comprends pas en fait la suite; j'essaie de recopier Flow Contact mais bof !!!! HELP 


    prp3 = w.ElementProperties(w.NodStress2DElement) # Contraintes nodales
    load1 = w.NodInteraction(3)
    load1.push(groups['FSInterface']) # Le physical group de l'interface fluide-structure
    #load.push(groups['Base']) # [*] Inutile, ne sert qu'à avoir un contour fermé pour le polytope? --> Je peux commenter du coup? 
    load1.addProperty(prp3)
    iset.add(load1)
    
     # Contact parameters

    penalty = 1e8               #  1e7
    friction = 0.35

    materset.define(3,w.CoulombContactMaterial)
    materset(3).put(w.PEN_TANGENT,friction*penalty)
    materset(3).put(w.COEF_FROT_DYN,friction)
    materset(3).put(w.COEF_FROT_STA,friction)
    materset(3).put(w.PEN_NORMALE,penalty)
    materset(3).put(w.PROF_CONT,0.0005)      # 0.001?

    #Maybe je dois separer en deux groupes? En haut et en bas? I don't know ??  

    prp4 = w.ElementProperties(w.Contact2DElement)
    prp4.put(w.AREAINCONTACT,w.AIC_ONCE)
    prp4.put(w.MATERIAL,3)

    # Defines the contact entities

    ci = w.DdContactInteraction(4)
    ci.setTool(groups['LeafletUp'])
    ci.setSmoothNormals(False)
    ci.push(groups['LeafletBottom'])
    ci.setSinglePass()
    ci.addProperty(prp4)
    iset.add(ci)

    # Boundary conditions 
    # On bloque la base du solide --> Je dois bloquer quoi moi du coup? Les côtés "side" non? 
    
    loadingset = domain.getLoadingSet()
    loadingset.define(groups['Sides'],w.Field1D(w.TX,w.RE)) # Pas de déplacement selon X
    loadingset.define(groups['Sides'],w.Field1D(w.TY,w.RE)) # Pas de déplacement selon Y

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor) # Intégration temporelle : Alpha généralisé
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim = metafor.getMechanicalIterationManager()
    mim.setResidualTolerance(1e-8) # Tolérance pour l'équilibre mécanique (= minRes dans PFEM3D)
    mim.setMaxNbOfIterations(25) # 25 itérations max, sinon stop et réduit le pas de temps

    # Time step iterations

    tsm = metafor.getTimeStepManager()
    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2) # d_next dt = dt/2 si fail

    # Metafor vaquand même réduire le pas de temps même sans atteindre etMaxNbOfIterations
    # s'il est au-dessus de setNbOptiIte = "optimal number of iterations"
    tscm.setNbOptiIte(25)

    # Parameters for FSPC

    parm['interacM'] = load1 # Le NodInteraction(2) pour FSPC
    # parm['interacM'] = [load1,load2] si jamais j'ai du définir plusieurs param. 
    parm['FSInterface'] = groups['FSInterface'] # Le groupe de l'interface fluide-structure

    # Un exporteur du résultat Metafor courant en Gmsh à donner à FSPC
    # Note : ça va changer à la prochaine mise à jour de Metafor
    
    parm['exporter'] = gmsh.NodalGmshExport('metafor/output.msh',metafor)
    
    #  Contrainte de Von Mises (0) 
    extr = w.IFNodalValueExtractor(groups['SolidUp'],w.IF_EVMS)
    parm['exporter'].addExtractor(extr)
    extr = w.IFNodalValueExtractor(groups['SolidBottom'],w.IF_EVMS)
    parm['exporter'].addExtractor(extr)
    
    parm['polytope'] = None # Mettre parm['polytope'] = None quand pas besoin

    domain.build() # Toujours copier/coller ça
    return metafor