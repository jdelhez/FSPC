import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

DF = 3e-4
LF = 3.15e-3
HF = 5e-3
HS = 3e-3
LS = 0.15

d = 1e-4
M = 1501
N = 31

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(-DF/2,HF,0,d))
p.append(sh.occ.addPoint(DF/2,HF,0,d))
p.append(sh.occ.addPoint(DF/2,HF+LF,0,d))
p.append(sh.occ.addPoint(-DF/2,HF+LF,0,d))

p.append(sh.occ.addPoint(LS/2,HS,0,d))
p.append(sh.occ.addPoint(-LS/2,HS,0,d))
p.append(sh.occ.addPoint(-LS/2,0,0,d))
p.append(sh.occ.addPoint(LS/2,0,0,d))

# Lines List

l = list()
h = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))
l.append(sh.occ.addLine(p[2],p[3]))
l.append(sh.occ.addLine(p[3],p[0]))

h.append(sh.occ.addLine(p[4],p[5]))
h.append(sh.occ.addLine(p[5],p[6]))
h.append(sh.occ.addLine(p[6],p[7]))
h.append(sh.occ.addLine(p[7],p[4]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l)
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(h[0],M)
sh.mesh.setTransfiniteCurve(h[1],N)
sh.mesh.setTransfiniteCurve(h[2],M)
sh.mesh.setTransfiniteCurve(h[3],N)

# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,h,name='FSInterface')
sh.addPhysicalGroup(1,[l[0],l[1],l[3]],name='FreeSurface')
sh.addPhysicalGroup(1,[l[2]],name='Inlet')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()