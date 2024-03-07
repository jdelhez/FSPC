import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

#L = 0.2 
L = 0.06
w = 0.01

# Characteristic size

d = 0.001
N = 11
M = 71


# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0,0,0,d)) # 0
p.append(sh.occ.addPoint(L,0,0,d)) # 1 
p.append(sh.occ.addPoint(L,w,0,d)) # 2 
p.append(sh.occ.addPoint(0,w,0,d)) # 3

# Lines List

l = list()
# h = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))
l.append(sh.occ.addLine(p[2],p[3]))
l.append(sh.occ.addLine(p[3],p[0]))

#h.append(sh.occ.addLine(p[7],p[8])) Je dois faire ca ou pas?? JSP si c'est utile ! Jsp a quoi correspondent ces points en fait. 
#h.append(sh.occ.addLine(p[8],p[9]))
#h.append(sh.occ.addLine(p[9],p[10]))

# OU BIEN QQCH COMME... (car h = partie en commun avec le solide??)
# l = list()
h = list()
# l.append(sh.occ.addLine(p[1],p[2]))  # 0
# l.append(sh.occ.addLine(p[3],p[0])) # 1
h.append(sh.occ.addLine(p[0],p[1])) # 0
h.append(sh.occ.addLine(p[2],p[3])) # 1

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l[0:4]) # Je crois? 
# k = sh.occ.addCurveLoop(l[0:1]) # Je crois? 
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

# MAILLAGE STRUCTURE

#sh.mesh.setTransfiniteCurve(l[0],M)
#sh.mesh.setTransfiniteCurve(l[1],N)
#sh.mesh.setTransfiniteCurve(l[2],M)
#sh.mesh.setTransfiniteCurve(l[3],N)

#sh.mesh.setTransfiniteSurface(s) # Eviter le transfinite en Fluide surtout en 3D (Martin)
#sh.occ.synchronize()

# MAILLAGE 2: LAISSER CA 

sh.mesh.setTransfiniteCurve(l[2],M)

# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,l[0:1]+l[2:3],name='FSInterface') # Mettre ca a la place de Boundary? Ou mettre les deux? COMMENT qu'on fait 
# Oui ca détermine la frontière Fluide Structure, si on met Boundary, l'interaction ne se fera pas (Martin)
#sh.addPhysicalGroup(1,l[0]+l[2],name='Boundary')
sh.addPhysicalGroup(1,l[3:4],name='Inlet')
sh.addPhysicalGroup(1,l[1:2],name='Outlet') # On peut aussi mettre FreeSurface si on veut laisser les noeuds sortir, c'est plus "stable" mais ça peut créer des trous dans le fluide, il faut tuner les paramètres de remesh pour compenser.

# |----------------------------------------|
# |   Mesh Characteristic Size Function    |
# |----------------------------------------|

# MAILLAGE 2: LAISSER CA 

fun = str(d)+'+0.2*F1'
sh.mesh.field.add('Distance',1)
sh.mesh.field.setNumber(1,'Sampling',1e4)
sh.mesh.field.setNumbers(1,'CurvesList',l)

sh.mesh.field.add('MathEval',2)
sh.mesh.field.setString(2,'F',fun)

sh.mesh.field.setAsBackgroundMesh(2)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints',0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary',0)

# Write the Mesh File

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()