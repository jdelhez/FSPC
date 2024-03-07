import os,gmsh
from gmsh import model as sh
gmsh.initialize()

import math 
from scipy.optimize import fsolve

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

mm = 1e-3
Z = 6*mm 
R = 18*mm 
H = 3*mm 
W = 12*mm 
Ro = 60*mm
theta = math.pi*0.25

# Characteristic size
# to be adjusted 
d = 0.001
N = 11
M = 41

def syst1(var): # définition du système
        x, y = var[0], var[1] # définition des variables
        eq1 = x**2 + y**2 - (Ro-Z)**2 
        eq2 = (x - (Ro+H)*math.cos(theta))**2 + (y - (Ro+H)*math.cos(theta))**2  - R**2
        res1 = [eq1, eq2]
        return res1

x0, y0= 0, 0 # Initialisation de la recherche des solutions numériques
sol_ini = [x0, y0]

sol1 = fsolve(syst1, sol_ini)

import math 
from scipy.optimize import fsolve

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

mm = 1e-3
Z = 6*mm 
R = 18*mm 
H = 3*mm 
W = 12*mm 
Ro = 60*mm
theta = math.pi*0.25

# Characteristic size
# to be adjusted 
d = 0.001
N = 11
M = 41

def syst1(var): # définition du système
        x, y = var[0], var[1] # définition des variables
        eq1 = x**2 + y**2 - (Ro-Z)**2 
        eq2 = (x - (Ro+H)*math.cos(theta))**2 + (y - (Ro+H)*math.cos(theta))**2  - R**2
        res1 = [eq1, eq2]
        return res1

x0, y0= 0, 0 # Initialisation de la recherche des solutions numériques
sol_ini = [x0, y0]

sol1 = fsolve(syst1, sol_ini)

#print("Numerical Solution (x, y):", sol1)

if sol1[1] > sol1[0]: 
    x2 = sol1[0]
    y2 = sol1[1]

def syst2(var): # définition du système
        x, y = var[0], var[1] # définition des variables
        eq1 = x**2 + y**2 - (Ro+Z)**2 
        eq2 = (x - (Ro+H)*math.cos(theta))**2 + (y - (Ro+H)*math.cos(theta))**2  - R**2
        res2 = [eq1, eq2]
        return res2

x0, y0= 0, 0 # Initialisation de la recherche des solutions numériques
sol_ini = [x0, y0]

sol2 = fsolve(syst2, sol_ini)

if sol2[1] > sol2[0]: 
    x9 = sol2[0]
    y9 = sol2[1]




# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(-W,Ro-Z,0,d)) # 0
p.append(sh.occ.addPoint(0,Ro-Z,0,d)) # 1 
#p.append(sh.occ.addPoint(26.7065*mm,46.9336*mm,0,d)) # 2 
p.append(sh.occ.addPoint(x2,y2,0,d)) # 2 
p.append(sh.occ.addPoint(0,0,0,d)) # 3 NB: to be changed in case we study the effect of the off-axis distance h 
#p.append(sh.occ.addPoint(46.9336*mm,26.7065*mm,0,d)) # 4
p.append(sh.occ.addPoint(y2,x2,0,d)) # 4
p.append(sh.occ.addPoint(math.cos(theta)*(Ro + H), math.sin(theta)*(Ro+H), 0, d)) # 5 
p.append(sh.occ.addPoint(Ro-Z, 0, 0, d)) # 6 
p.append(sh.occ.addPoint(Ro+Z, 0, 0, d)) # 7
#p.append(sh.occ.addPoint(57.6243*mm, 32.1783*mm, 0, d)) # 8
p.append(sh.occ.addPoint(y9, x9, 0, d)) # 8
#p.append(sh.occ.addPoint(32.1783*mm, 57.6243*mm, 0, d)) # 9 
p.append(sh.occ.addPoint(x9, y9, 0, d)) # 9
p.append(sh.occ.addPoint(0, Ro+Z, 0, d)) # 10 
p.append(sh.occ.addPoint(-W, Ro+Z, 0, d)) # 11


# Lines List

l = list()
# h = list()

l.append(sh.occ.addLine(p[0],p[1])) # 0
l.append(sh.occ.addCircleArc(p[1],p[3],p[2])) # 1
l.append(sh.occ.addCircleArc(p[2],p[5],p[4])) # 2
l.append(sh.occ.addCircleArc(p[4],p[3],p[6])) # 3
l.append(sh.occ.addLine(p[6],p[7])) # 4
l.append(sh.occ.addCircleArc(p[7],p[3],p[8])) # 5
l.append(sh.occ.addCircleArc(p[8],p[5],p[9])) # 6
l.append(sh.occ.addCircleArc(p[9],p[3],p[10])) # 7
l.append(sh.occ.addLine(p[10],p[11])) # 8
l.append(sh.occ.addLine(p[11],p[0])) # 9

# OU BIEN QQCH COMME... (car h = partie en commun avec le solide?? Oui, je vais faire comme ça.)

h = list()

h.append(sh.occ.addLine(p[0],p[1])) # 0
h.append(sh.occ.addCircleArc(p[1],p[3],p[2])) # 1
h.append(sh.occ.addCircleArc(p[2],p[5],p[4])) # 2
h.append(sh.occ.addCircleArc(p[4],p[3],p[6])) # 4
h.append(sh.occ.addCircleArc(p[7],p[3],p[8])) # 5
h.append(sh.occ.addCircleArc(p[8],p[5],p[9])) # 6
h.append(sh.occ.addCircleArc(p[9],p[3],p[10])) # 7
h.append(sh.occ.addLine(p[10],p[11])) # 8

# On l'utilise meme pas apres en vrai.



# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l[0:10]) # Je crois? 
# k = sh.occ.addCurveLoop(l[0:1]) # Je crois? 
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

# A mettre si on garde l'option 2...  Je ne sais pas trop comment gerer ca dans le cas de mon anevrisme en vrai de vraiii

#sh.mesh.setTransfiniteCurve(l[0],M)
#sh.mesh.setTransfiniteCurve(l[8],M)

#sh.mesh.setTransfiniteCurve(l[0],M)
#sh.mesh.setTransfiniteCurve(l[8],M)


#sh.mesh.setTransfiniteCurve(l[2],M)
#sh.mesh.setTransfiniteCurve(l[3],N)

#sh.mesh.setTransfiniteSurface(s)

#sh.occ.synchronize()

#sh.mesh.setTransfiniteCurve(l[2],N)

# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,l[0:4]+l[5:9],name='FSInterface') # Mettre ca a la place de Boundary? Ou mettre les deux? COMMENT qu'on fait 
#sh.addPhysicalGroup(1,l[0]+l[2],name='Boundary')
sh.addPhysicalGroup(1,l[9:10],name='Inlet')
sh.addPhysicalGroup(1,l[4:5],name='Outlet')
#sh.addPhysicalGroup(1,l[2:3]+l[6:7],name='Aneurysm')



# |----------------------------------------|
# |   Mesh Characteristic Size Function    |
# |----------------------------------------|

#fun = str(d)+'+0.1*F1'
#sh.mesh.field.add('Distance',1)
##sh.mesh.field.setNumber(1,'Sampling',1e4)
#sh.mesh.field.setNumbers(1,'CurvesList',l)

#sh.mesh.field.add('MathEval',2)
#sh.mesh.field.setString(2,'F',fun)

#sh.mesh.field.setAsBackgroundMesh(2)
#gmsh.option.setNumber('Mesh.MeshSizeFromPoints',0)
#gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary',0)

# Write the Mesh File

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()