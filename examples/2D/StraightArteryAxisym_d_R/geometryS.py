import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

cm = 1e-2
L  = 3.0 * cm
L2 = 0.25 * cm
w  = 0.5 * cm
t  = 0.1 * cm

# Characteristic size


N = 5
M  = 41
M2 = 5

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(w,0,0))        # 0
p.append(sh.occ.addPoint(w+t,0,0))      # 1
p.append(sh.occ.addPoint(w+t,L,0))      # 2 
p.append(sh.occ.addPoint(w,L,0))        # 3
p.append(sh.occ.addPoint(w+t,L+L2,0)) # 4 
p.append(sh.occ.addPoint(w,L+L2,0))   # 5


# Lines List

l = list()

l.append(sh.occ.addLine(p[0],p[1])) # 0
l.append(sh.occ.addLine(p[1],p[2])) # 1
l.append(sh.occ.addLine(p[2],p[3])) # 2 
l.append(sh.occ.addLine(p[3],p[0])) # 3

h = list()

h.append(sh.occ.addLine(p[2],p[4])) # 0
h.append(sh.occ.addLine(p[4],p[5])) # 1
h.append(sh.occ.addLine(p[5],p[3])) # 2 
h.append(sh.occ.addLine(p[3],p[2])) # 3

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

# Comment fait-on quand on a plusieurs surfaces? 

k = list()
s = list()

k.append(sh.occ.addCurveLoop(l))
k.append(sh.occ.addCurveLoop(h))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()


# Je sais pas trop à quoi correspondent les lignes qui suivent et leur pertinence - tiré de l'example FlowContact  

#sh.mesh.setAlgorithm(2,s[0],8)
#sh.mesh.setAlgorithm(2,s[1],8)
#sh.occ.synchronize()

# On est obligé de faire un transfinite curve mesh en fait?? 

sh.mesh.setTransfiniteCurve(l[0],N)
sh.mesh.setTransfiniteCurve(l[1],M)
sh.mesh.setTransfiniteCurve(l[2],N)
sh.mesh.setTransfiniteCurve(l[3],M)

sh.mesh.setTransfiniteCurve(h[0],M2)
sh.mesh.setTransfiniteCurve(h[1],N)
sh.mesh.setTransfiniteCurve(h[2],M2)
sh.mesh.setTransfiniteCurve(h[3],N)

sh.mesh.setTransfiniteSurface(s[0]) 
sh.mesh.setTransfiniteSurface(s[1]) 
# sh.occ.synchronize()

sh.mesh.setRecombine(2,s[0])
sh.mesh.setRecombine(2,s[1])
sh.occ.synchronize()


# Physical Boundary


sh.addPhysicalGroup(2,[s[0]],name='Solid')
sh.addPhysicalGroup(2,[s[1]],name='Solid2')

sh.addPhysicalGroup(1,l[3:4] + h[2:3], name='FSInterface')

sh.addPhysicalGroup(1,l[0:1] + h[1:2],name='Sides')

sh.addPhysicalGroup(1,l[1:2] + h[0:1],name='Ext')


# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

# A quoi servent les deux lignes ci-dessous (presentes dans FlowContact mais pas dans Dam)

# gmsh.option.setNumber('Mesh.RecombineAll',1)
# gmsh.option.setNumber('Mesh.Algorithm',11)

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryS.msh')
gmsh.fltk.run()
gmsh.finalize()



