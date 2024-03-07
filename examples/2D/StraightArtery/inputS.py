import toolbox.gmsh as gmsh
import wrap as w
import os
import gmsh

from gmsh import model as sh
gmsh.initialize()

p = list()

L = 0.06
w = 0.01

p.append(sh.occ.addPoint(0,0,0)) # 0
p.append(sh.occ.addPoint(L,0,0)) # 1 
p.append(sh.occ.addPoint(L,w,0)) # 2 
p.append(sh.occ.addPoint(0,w,0)) # 3


class Extractor(object):
   def __init__(self):
       self.metafor = metafor
   def write(self,extractor): # (**)
       file = open(extractor.buildName()+'.txt', 'a') # Le fichier dans lequel on écrit    
       file.write('{0:12.6f}\t'.format(self.metafor.getCurrentTime())) # Le temps actuel
       file.write('{0:12.6f}\n'.format(extractor.extract()[0])) # Le résultat de l'extracteur Metafor
       file.close()
   def execute(self):
        extractor = w.DbNodalValueExtractor(p, w.Field1D(w.TY,w.RE))
        self.write(extractor)


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
    materset(1).put(w.ELASTIC_MODULUS,975e3) # Attention
    materset(1).put(w.MASS_DENSITY,1100)
    materset(1).put(w.POISSON_RATIO,0.49)
  
    materset.define(2,w.ElastHypoMaterial)
    materset(2).put(w.ELASTIC_MODULUS,975e3) # Attention
    materset(2).put(w.MASS_DENSITY,1100)
    materset(2).put(w.POISSON_RATIO,0.49)

    

    # nu = 0.49 
    # E = 675e3 

    # G = E/(2*(1+nu))
    # K = E/(3*(1-2*nu))
    # C1 = 174000
    # C2 = 1880000

    #materset = domain.getMaterialSet()
    #materset.define(1,w.MooneyRivlinHyperMaterial)
    #materset(1).put(w.MASS_DENSITY,1100)
    #materset(1).put(w.RUBBER_PENAL,K)
    #materset(1).put(w.RUBBER_C1,C1)
    #materset(1).put(w.RUBBER_C2,C2)
    
    # materset.define(2,w.MooneyRivlinHyperMaterial)
    # materset(2).put(w.MASS_DENSITY,1100)
    # materset(2).put(w.RUBBER_PENAL,K)
    # materset(2).put(w.RUBBER_C1,C1)
    # materset(2).put(w.RUBBER_C2,C2)


     #materset = domain.getMaterialSet()
     #materset.define(1,w.NeoHookeanHyperPk2Material) # Le "1" pour FieldApplicator(1)
     #materset(1).put(w.HYPER_K0,K)
     #materset(1).put(w.MASS_DENSITY,1100)
     #materset(1).put(w.HYPER_G0,G)
    

     #materset.define(2,w.NeoHookeanHyperPk2Material)
     #materset(2).put(w.HYPER_K0,K)
     #materset(2).put(w.MASS_DENSITY,1100)
     #materset(2).put(w.HYPER_G0,G)


    
    # Proprietes d'un vaisseau sanguin a check ailleurs ! 
    
    # Pas de "contact parameter" (voir FlowContact !)

    # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement) # Quadrangles 2D
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC) # Calcul analytique de la matrice de raideur tangente
    # prp1.put(w.STIFFMETHOD,w.STIFF_NUMERIC)
    # prp1.put(w.GRAVITY_Y,-9.81)  #Bouger la gravité ou non?? 
    prp1.put(w.MATERIAL,1) # Le "1" pour materset(1)
    app1.addProperty(prp1)

    prp2 = w.ElementProperties(w.Volume2DElement)
    prp2.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp2.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    # prp2.put(w.STIFFMETHOD,w.STIFF_NUMERIC) # Calcul numérique de la matrice de raideur tangente
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
    
    #Maybe je dois separer en deux groupes? En haut et en bas? I don't knowww ; genre faire comme ça:  ??? 

    #prp3 = w.ElementProperties(w.NodStress2DElement)
    #load1 = w.NodInteraction(3)
    #load1.push(groups['PeigneSide']) avec UpperSide 
    #load1.addProperty(prp3)
    #iset.add(load1)

    #prp4 = w.ElementProperties(w.NodStress2DElement)
    #load2 = w.NodInteraction(4)
    #load2.push(groups['DiskSide']) avec BottomSide 
    #load2.addProperty(prp4)
    #iset.add(load2)

    # Boundary conditions 
    # On bloque la base du solide --> Je dois bloquer quoi moi du coup? Les côtés "side" non? 
    
    loadingset = domain.getLoadingSet()
    loadingset.define(groups['Ext'],w.Field1D(w.TX,w.RE)) # Pas de déplacement selon X
    loadingset.define(groups['Ext'],w.Field1D(w.TY,w.RE)) # Pas de déplacement selon Y

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
    parm['exporter'] = gmsh.GmshExport('metafor/output.msh',metafor)
    parm['exporter'].addInternalField([w.IF_EVMS,w.IF_P]) # Von Mises et Pression
    
    parm['exporter'] = Extractor()
    
    # Les éléments contenus dans l'interaction "load" pour former le polytope
    # C'est pour ça qu'on a [*]
    # parm['polytope'] = load1.getElementSet() # Mettre parm['polytope'] = None quand pas besoin
    parm['polytope'] = None # Mettre parm['polytope'] = None quand pas besoin

    domain.build() # Toujours copier/coller ça
    return metafor

