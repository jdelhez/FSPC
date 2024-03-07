import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

cm =1e-2
L = 6.0*cm
w = 0.5*cm

# Characteristic size

d = 0.05*cm

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0,0,0,d)) # 0
p.append(sh.occ.addPoint(w,0,0,d)) # 1 
p.append(sh.occ.addPoint(w,L,0,d)) # 2 
p.append(sh.occ.addPoint(0,L,0,d)) # 3

# Lines List

l = list()
# h = list()

l.append(sh.occ.addLine(p[0],p[1])) # 0
l.append(sh.occ.addLine(p[1],p[2])) # 1
l.append(sh.occ.addLine(p[2],p[3])) # 2
l.append(sh.occ.addLine(p[3],p[0])) # 3

#h.append(sh.occ.addLine(p[7],p[8])) Je dois faire ca ou pas?? JSP si c'est utile ! Jsp a quoi correspondent ces points en fait. 
#h.append(sh.occ.addLine(p[8],p[9]))
#h.append(sh.occ.addLine(p[9],p[10]))

# OU BIEN QQCH COMME... (car h = partie en commun avec le solide??)
# l = list()
# l.append(sh.occ.addLine(p[1],p[2]))  # 0
# l.append(sh.occ.addLine(p[3],p[0])) # 1
#h.append(sh.occ.addLine(p[1],p[1])) # 0

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l) # Je crois? 
# k = sh.occ.addCurveLoop(l[0:1]) # Je crois? 
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()


# A mettre si on garde l'option 2... 

# sh.mesh.setTransfiniteCurve(l[0],N)
# sh.mesh.setTransfiniteCurve(l[1],M)
# sh.mesh.setTransfiniteCurve(l[2],N)
# sh.mesh.setTransfiniteCurve(l[3],M)

#sh.mesh.setTransfiniteSurface(s) MAYBE A REMETTRE

#sh.occ.synchronize() MAYBE A REMETTRE !!

#sh.mesh.setTransfiniteCurve(l[2],N)

# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,l[1:2],name='FSInterface') # Mettre ca a la place de Boundary? Ou mettre les deux? COMMENT qu'on fait 
#sh.addPhysicalGroup(1,l[0]+l[2],name='Boundary')
sh.addPhysicalGroup(1,l[0:1],name='Inlet')
sh.addPhysicalGroup(1,l[2:3],name='Outlet')
#sh.addPhysicalGroup(1,l[3:4],name='Free')



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