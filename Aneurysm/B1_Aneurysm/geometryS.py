import os,gmsh
from gmsh import model as sh
gmsh.initialize()

import math
# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|


cm =1e-2
r = 1*cm
R = 2*r
L1 = 2*r
L2 = 2*r
e = 0.15*cm

# Characteristic size

N1x = 10
N1y = 20 

Nx = 10
Ny = 300

N2x= 10
N2y = 20

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(r,-L1-6*r,0)) # 0
p.append(sh.occ.addPoint(r+e,-L1-6*r,0)) # 1 
p.append(sh.occ.addPoint(r+e,-6*r,0)) #2
p.append(sh.occ.addPoint(r,-6*r,0)) #3




p.append(sh.occ.addPoint(r,+6*r,0)) #4
p.append(sh.occ.addPoint(r+e,+6*r,0)) #5
p.append(sh.occ.addPoint(r+e,+L2+6*r,0)) #6 
p.append(sh.occ.addPoint(r,+L2+6*r,0)) #7


n = 10
np = 2*n-1
for i in range(-n+1,n):
    y = i*r*6/n
    x = e+r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0)) # 3 Centre

for i in range(n-1,-n,-1):
    y = i*r*6/n
    x = r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0)) # 3 Centre


# Lines List

l1 = list()
l1.append(sh.occ.addLine(p[0],p[1])) 
l1.append(sh.occ.addLine(p[1],p[2])) 
l1.append(sh.occ.addLine(p[2],p[3])) 
l1.append(sh.occ.addLine(p[3],p[0])) 

l2 = list()

l2.append(sh.occ.addLine(p[3],p[2])) 


lp=list()
lp.append(p[2])
for i in range(8,np+8):
    lp.append(p[i])
lp.append(p[5])
l2.append(sh.occ.add_spline(lp))

l2.append(sh.occ.addLine(p[5],p[4]))
lp=list()
lp.append(p[4])
for i in range(np+8,2*np+8):
    lp.append(p[i])
lp.append(p[3])
l2.append(sh.occ.add_spline(lp))

sh.occ.synchronize()


l3 = list()
l3.append(sh.occ.addLine(p[4],p[5])) 
l3.append(sh.occ.addLine(p[5],p[6])) 
l3.append(sh.occ.addLine(p[6],p[7])) 
l3.append(sh.occ.addLine(p[7],p[4])) 



# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

# Comment fait-on quand on a plusieurs surfaces? 

k = list()
s = list()

k.append(sh.occ.addCurveLoop(l1))
k.append(sh.occ.addCurveLoop(l2))
k.append(sh.occ.addCurveLoop(l3))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()

#sh.mesh.setAlgorithm(2,s[0],8)
#sh.mesh.setAlgorithm(2,s[1],8)
#sh.mesh.setAlgorithm(2,s[2],8)

#for a in range(1,np+2): sh.mesh.setTransfiniteCurve(l3[a],5)
#for a in range(np+3,2*np+4): sh.mesh.setTransfiniteCurve(l3[a],5)


# On est obligé de faire un transfinite curve mesh en fait?? 

sh.mesh.setTransfiniteCurve(l1[0],N1x)
sh.mesh.setTransfiniteCurve(l1[1],N1y)
sh.mesh.setTransfiniteCurve(l1[2],N1x)
sh.mesh.setTransfiniteCurve(l1[3],N1y)


sh.mesh.setTransfiniteCurve(l2[0],Nx)
sh.mesh.setTransfiniteCurve(l2[1],Ny)
sh.mesh.setTransfiniteCurve(l2[2],Nx)
sh.mesh.setTransfiniteCurve(l2[3],Ny)

sh.mesh.setTransfiniteCurve(l3[0],N2x)
sh.mesh.setTransfiniteCurve(l3[1],N2y)
sh.mesh.setTransfiniteCurve(l3[2],N2x)
sh.mesh.setTransfiniteCurve(l3[3],N2y)

sh.mesh.setTransfiniteSurface(s[0]) 
sh.mesh.setTransfiniteSurface(s[1]) 
sh.mesh.setTransfiniteSurface(s[2]) 

#sh.occ.synchronize()

sh.mesh.setRecombine(2,s[0])
sh.mesh.setRecombine(2,s[1])
sh.mesh.setRecombine(2,s[2])

sh.occ.synchronize()


# Physical Boundary


sh.addPhysicalGroup(2,s[0:3],name='Solid')
sh.addPhysicalGroup(1,l2[3:4], name='FSInterface')
sh.addPhysicalGroup(1,l1[0:1] + l1[3:4] + l3[2:4],name='Sides')
sh.addPhysicalGroup(1,l1[1:2] + l3[1:2],name='Ext')


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



