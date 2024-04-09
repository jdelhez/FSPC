import os,gmsh
from gmsh import model as sh
gmsh.initialize()

import math
# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

cm =1e-2
r = 1*cm
R = r 
# R =  2*r
L1 = 1*r
L2 = 1*r


# Characteristic size

d  = 0.09*cm
d0 = 0.10*cm

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()


p.append(sh.occ.addPoint(0,-L1-3*r,0,d0)) # 0
p.append(sh.occ.addPoint(r,-L1-3*r,0,d0)) # 1 

p.append(sh.occ.addPoint(r,-3*r,0,d)) # 2 

#j=j+1

n = 10
np = 2*n-1
for i in range(-n+1,n):
    y = i*r*3/n
    x = r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0,d)) # 3 Centre

p.append(sh.occ.addPoint(r,3*r,0,d))
p.append(sh.occ.addPoint(r,L2+3*r,0,d0)) # 12 
p.append(sh.occ.addPoint(0,L2+3*r,0,d0)) # 13
# Lines List

l = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))

lp=list()
for i in range(2,np+4):
    lp.append(p[i])
l.append(sh.occ.add_spline(lp))
l.append(sh.occ.addLine(p[np+3],p[np+4]))
l.append(sh.occ.addLine(p[np+4],p[np+5]))
l.append(sh.occ.addLine(p[np+5],p[0])) # 7

sh.occ.synchronize()


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



# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,l[2:3],name='FSInterface')  
sh.addPhysicalGroup(1,l[0:1],name='Inlet')
sh.addPhysicalGroup(1,l[4:5],name='Outlet')
#sh.addPhysicalGroup(1,l[4:5],name='FreeSurface')
sh.addPhysicalGroup(1,l[1:2]+l[3:4],name='Fixed')
#sh.addPhysicalGroup(1,[l[5]],name='FreeSurface')





# Write the Mesh File

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()