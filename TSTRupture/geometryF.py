import os,gmsh
from gmsh import model as sh
gmsh.initialize()

import math
# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

cm =1e-2
r = 1*cm
# R = r 
R =  2*r
L1 = 2*r
L2 = 2*r
e = 0.15*cm

# Characteristic size

Nx= 10
Ny = 150
Ny1 = 20
Ny2 = 20

d  = 0.09*cm
d0 = 0.10*cm


# d  = 0.09*cm
# d0 = 0.10*cm


# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()


p.append(sh.occ.addPoint(0,-L1-6*r,0,d0)) # 0
p.append(sh.occ.addPoint(r,-L1-6*r,0,d0)) # 1 

p.append(sh.occ.addPoint(r,-6*r,0,d)) # 2 

#j=j+1

n = 10
np = 2*n-1
for i in range(-n+1,n):
    y = i*r*6/n
    x = r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0,d)) # 3 Centre

p.append(sh.occ.addPoint(r,6*r,0,d))
p.append(sh.occ.addPoint(r,L2+6*r,0,d0)) # 12 
p.append(sh.occ.addPoint(0,L2+6*r,0,d0)) # 13

n = 10
np = 2*n-1
p.append(sh.occ.addPoint(r+e,-6*r,0,d))
for i in range(-n+1,n):
    y = i*r*6/n
    x = e+r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0,d)) # 3 Centre
p.append(sh.occ.addPoint(r+e,6*r,0,d))

p.append(sh.occ.addPoint(r+e,-L1-6*r,0,d0)) # 46
p.append(sh.occ.addPoint(r+e,L2+6*r,0,d0)) # 47
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

lp2=list()
for i in range(25,np+25+2):
    lp2.append(p[i])

lFSI=list()

lFSI.append(sh.occ.addLine(p[1],p[46]))
lFSI.append(sh.occ.addLine(p[46],p[25]))
lFSI.append(sh.occ.add_spline(lp2))
lFSI.append(sh.occ.addLine(p[np+25+1],p[47]))
lFSI.append(sh.occ.addLine(p[47],p[23]))

sh.occ.synchronize()


# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l) # Je crois? 
s = sh.occ.addPlaneSurface([k])

sh.mesh.setTransfiniteCurve(lFSI[0],Nx)
sh.mesh.setTransfiniteCurve(lFSI[1],Ny)
sh.mesh.setTransfiniteCurve(lFSI[2],Nx)
sh.mesh.setTransfiniteCurve(l[1],Ny1)
sh.mesh.setTransfiniteCurve(l[2],Ny)
sh.mesh.setTransfiniteCurve(l[3],Ny2)

sh.occ.synchronize()



# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,lFSI+l[3:4]+l[2:3]+l[1:2],name='FSInterface')  
sh.addPhysicalGroup(1,l[0:1],name='Inlet')
sh.addPhysicalGroup(1,l[4:5],name='Outlet')

# Write the Mesh File

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()
