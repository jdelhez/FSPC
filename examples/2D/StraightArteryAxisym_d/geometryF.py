import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

cm =1e-2
L  = 6.0*cm
L2 = 3.0*cm
w = 0.5*cm

# Characteristic size

d = 0.05*cm

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0,0,0,d)) # 0
p.append(sh.occ.addPoint(w,0,0,d)) # 1 

p.append(sh.occ.addPoint(w,L+L2,0,d)) # 2 
p.append(sh.occ.addPoint(0,L+L2,0,d)) # 3
# Lines List

l = list()

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
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()


sh.occ.synchronize()


# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,l[1:2],name='FSInterface')  
sh.addPhysicalGroup(1,l[0:1],name='Inlet')
sh.addPhysicalGroup(1,l[2:3],name='Outlet')






# Write the Mesh File

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()