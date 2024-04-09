import os,gmsh
from gmsh import model as sh
gmsh.initialize()

import math
# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|


micron =1e-6
r = 15*micron
R = r # R = 2*r
L1 = 1*r
L2 = 1*r
e = 6*micron

# Characteristic size

Nx = 8
Ny = 300

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(r,-L1-3*r,0)) # 0
p.append(sh.occ.addPoint(r+e,-L1-3*r,0)) # 1 
p.append(sh.occ.addPoint(r+e,-3*r,0)) #2
p.append(sh.occ.addPoint(r,-3*r,0)) #3




p.append(sh.occ.addPoint(r,+3*r,0)) #4
p.append(sh.occ.addPoint(r+e,+3*r,0)) #5
p.append(sh.occ.addPoint(r+e,+L2+3*r,0)) #6 
p.append(sh.occ.addPoint(r,+L2+3*r,0)) #7


n = 10
np = 2*n-1
for i in range(-n+1,n):
    y = i*r*3/n
    x = e+r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0)) # 3 Centre

for i in range(n-1,-n,-1):
    y = i*r*3/n
    x = r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0)) # 3 Centre


# Lines List


l3 = list()

l3.append(sh.occ.addLine(p[3],p[2])) 


lp=list()
lp.append(p[2])
for i in range(8,np+8):
    lp.append(p[i])
lp.append(p[5])
l3.append(sh.occ.add_spline(lp))

l3.append(sh.occ.addLine(p[5],p[4]))
lp=list()
lp.append(p[4])
for i in range(np+8,2*np+8):
    lp.append(p[i])
lp.append(p[3])
l3.append(sh.occ.add_spline(lp))

sh.occ.synchronize()



#h = list()

#h.append(sh.occ.addLine(p[2],p[4])) # 0
#h.append(sh.occ.addLine(p[4],p[5])) # 1
#h.append(sh.occ.addLine(p[5],p[3])) # 2 
#h.append(sh.occ.addLine(p[3],p[2])) # 3

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

# Comment fait-on quand on a plusieurs surfaces? 

k = list()
s = list()

k.append(sh.occ.addCurveLoop(l3))
#k.append(sh.occ.addCurveLoop(l2))
#k.append(sh.occ.addCurveLoop(l3))

# k.append(sh.occ.addCurveLoop(h))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()

#sh.mesh.setAlgorithm(2,s[0],8)
#sh.mesh.setAlgorithm(2,s[1],8)
#sh.mesh.setAlgorithm(2,s[2],8)

#for a in range(1,np+2): sh.mesh.setTransfiniteCurve(l3[a],5)
#for a in range(np+3,2*np+4): sh.mesh.setTransfiniteCurve(l3[a],5)


# On est obligé de faire un transfinite curve mesh en fait?? 


sh.mesh.setTransfiniteCurve(l3[0],Nx)
sh.mesh.setTransfiniteCurve(l3[1],Ny)
sh.mesh.setTransfiniteCurve(l3[2],Nx)
sh.mesh.setTransfiniteCurve(l3[3],Ny)

sh.mesh.setTransfiniteSurface(s[0]) 
#sh.mesh.setTransfiniteSurface(s[1]) 

#sh.occ.synchronize()

sh.mesh.setRecombine(2,s[0])
#sh.mesh.setRecombine(2,s[1])
#sh.mesh.setRecombine(2,s[2])
sh.occ.synchronize()


# Physical Boundary


sh.addPhysicalGroup(2,[s[0]],name='Solid')
sh.addPhysicalGroup(1,l3[3:4], name='FSInterface')
sh.addPhysicalGroup(1,l3[0:1] + l3[2:3],name='Sides')
sh.addPhysicalGroup(1,l3[1:2],name='Ext')


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



