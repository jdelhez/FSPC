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

e1 = e * 20/(20+47+33)
e2 = e * 47/(20+47+33)
e3 = e * 33/(20+47+33)

# Characteristic size

Nx1 = 3
Nx2 = 6
Nx3 = 4

Nx = Nx1+Nx2+Nx3

N1y = 20
Ny  = 300
N2y = 20

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(r,-L1-6*r,0)) # 0
p.append(sh.occ.addPoint(r+e1,-L1-6*r,0)) # 1
p.append(sh.occ.addPoint(r+e2,-L1-6*r,0)) # 2
p.append(sh.occ.addPoint(r+e,-L1-6*r,0)) # 3 
p.append(sh.occ.addPoint(r+e,-6*r,0)) #4
p.append(sh.occ.addPoint(r+e1+e2,-6*r,0)) #5
p.append(sh.occ.addPoint(r+e1,-6*r,0)) #6
p.append(sh.occ.addPoint(r,-6*r,0)) #7

p.append(sh.occ.addPoint(r,+6*r,0)) #8
p.append(sh.occ.addPoint(r+e1,+6*r,0)) #9
p.append(sh.occ.addPoint(r+e1+e2,+6*r,0)) #10
p.append(sh.occ.addPoint(r+e,+6*r,0)) #11
p.append(sh.occ.addPoint(r+e,+L2+6*r,0)) #12 
p.append(sh.occ.addPoint(r+e1+e2,+L2+6*r,0)) #13
p.append(sh.occ.addPoint(r+e1,+L2+6*r,0)) #14
p.append(sh.occ.addPoint(r,+L2+6*r,0)) #15


n = 10
np = 2*n-1
for i in range(-n+1,n):
    y = i*r*6/n
    x = e+r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0))

for i in range(-n+1,n):
    y = i*r*6/n
    x = e1+e2+r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0))

for i in range(-n+1,n):
    y = i*r*6/n
    x = e1+r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0))

for i in range(-n+1,n):
    y = i*r*6/n
    x = r+(R-r)*(1+math.cos(math.pi*i/n))/2
    p.append(sh.occ.addPoint(x,y,0))


# Lines List

l11 = list()
l11.append(sh.occ.addLine(p[0],p[1])) 
l11.append(sh.occ.addLine(p[1],p[6])) 
l11.append(sh.occ.addLine(p[6],p[7])) 
l11.append(sh.occ.addLine(p[7],p[0])) 

l12 = list()
l12.append(sh.occ.addLine(p[1],p[2])) 
l12.append(sh.occ.addLine(p[2],p[5])) 
l12.append(sh.occ.addLine(p[5],p[6])) 
l12.append(sh.occ.addLine(p[6],p[1])) 

l13 = list()
l13.append(sh.occ.addLine(p[2],p[3])) 
l13.append(sh.occ.addLine(p[3],p[4])) 
l13.append(sh.occ.addLine(p[4],p[5])) 
l13.append(sh.occ.addLine(p[5],p[2])) 

l23 = list()

l23.append(sh.occ.addLine(p[5],p[4])) 

ls=list()
ls.append(p[4])
for i in range(16,np+16):
    ls.append(p[i])
ls.append(p[11])
l23.append(sh.occ.add_spline(ls))

l23.append(sh.occ.addLine(p[11],p[10]))

ls=list()
ls.append(p[5])
for i in range(np+16,2*np+16):
    ls.append(p[i])
ls.append(p[10])
l23.append(sh.occ.add_spline(ls))


l22 = list()

l22.append(sh.occ.addLine(p[6],p[5])) 
l22.append(sh.occ.add_spline(ls))
l22.append(sh.occ.addLine(p[10],p[9]))

ls=list()
ls.append(p[6])
for i in range(2*np+16,3*np+16):
    ls.append(p[i])
ls.append(p[9])
l22.append(sh.occ.add_spline(ls))

l21 = list()

l21.append(sh.occ.addLine(p[7],p[6])) 
l21.append(sh.occ.add_spline(ls))
l21.append(sh.occ.addLine(p[9],p[8]))

ls=list()
ls.append(p[7])
for i in range(3*np+16,4*np+16):
    ls.append(p[i])
ls.append(p[8])
l21.append(sh.occ.add_spline(ls))


sh.occ.synchronize()


l31 = list()
l31.append(sh.occ.addLine(p[8],p[9])) 
l31.append(sh.occ.addLine(p[9],p[14])) 
l31.append(sh.occ.addLine(p[14],p[15])) 
l31.append(sh.occ.addLine(p[15],p[8])) 


l32 = list()
l32.append(sh.occ.addLine(p[9],p[10])) 
l32.append(sh.occ.addLine(p[10],p[13])) 
l32.append(sh.occ.addLine(p[13],p[14])) 
l32.append(sh.occ.addLine(p[14],p[9])) 


l33 = list()
l33.append(sh.occ.addLine(p[10],p[11])) 
l33.append(sh.occ.addLine(p[11],p[12])) 
l33.append(sh.occ.addLine(p[12],p[13])) 
l33.append(sh.occ.addLine(p[13],p[10])) 

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

# Comment fait-on quand on a plusieurs surfaces? 

k = list()
s = list()

k.append(sh.occ.addCurveLoop(l11))
k.append(sh.occ.addCurveLoop(l12))
k.append(sh.occ.addCurveLoop(l13))

k.append(sh.occ.addCurveLoop(l21))
k.append(sh.occ.addCurveLoop(l22))
k.append(sh.occ.addCurveLoop(l23))

k.append(sh.occ.addCurveLoop(l31))
k.append(sh.occ.addCurveLoop(l32))
k.append(sh.occ.addCurveLoop(l33))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()


sh.mesh.setTransfiniteCurve(l11[0],Nx1)
sh.mesh.setTransfiniteCurve(l11[1],N1y)
sh.mesh.setTransfiniteCurve(l11[2],Nx1)
sh.mesh.setTransfiniteCurve(l11[3],N1y)
sh.mesh.setTransfiniteCurve(l12[0],Nx2)
sh.mesh.setTransfiniteCurve(l12[1],N1y)
sh.mesh.setTransfiniteCurve(l12[2],Nx2)
sh.mesh.setTransfiniteCurve(l12[3],N1y)
sh.mesh.setTransfiniteCurve(l13[0],Nx3)
sh.mesh.setTransfiniteCurve(l13[1],N1y)
sh.mesh.setTransfiniteCurve(l13[2],Nx3)
sh.mesh.setTransfiniteCurve(l13[3],N1y)

sh.mesh.setTransfiniteCurve(l21[0],Nx1)
sh.mesh.setTransfiniteCurve(l21[1],Ny)
sh.mesh.setTransfiniteCurve(l21[2],Nx1)
sh.mesh.setTransfiniteCurve(l21[3],Ny)
sh.mesh.setTransfiniteCurve(l22[0],Nx2)
sh.mesh.setTransfiniteCurve(l22[1],Ny)
sh.mesh.setTransfiniteCurve(l22[2],Nx2)
sh.mesh.setTransfiniteCurve(l22[3],Ny)
sh.mesh.setTransfiniteCurve(l23[0],Nx3)
sh.mesh.setTransfiniteCurve(l23[1],Ny)
sh.mesh.setTransfiniteCurve(l23[2],Nx3)
sh.mesh.setTransfiniteCurve(l23[3],Ny)


sh.mesh.setTransfiniteCurve(l31[0],Nx1)
sh.mesh.setTransfiniteCurve(l31[1],N2y)
sh.mesh.setTransfiniteCurve(l31[2],Nx1)
sh.mesh.setTransfiniteCurve(l31[3],N2y)
sh.mesh.setTransfiniteCurve(l32[0],Nx2)
sh.mesh.setTransfiniteCurve(l32[1],N2y)
sh.mesh.setTransfiniteCurve(l32[2],Nx2)
sh.mesh.setTransfiniteCurve(l32[3],N2y)
sh.mesh.setTransfiniteCurve(l33[0],Nx3)
sh.mesh.setTransfiniteCurve(l33[1],N2y)
sh.mesh.setTransfiniteCurve(l33[2],Nx3)
sh.mesh.setTransfiniteCurve(l33[3],N2y)

for j in range(0,9): sh.mesh.setTransfiniteSurface(s[j]) 
for j in range(0,9): sh.mesh.setRecombine(2,s[j])

sh.occ.synchronize()


# Physical Boundary


sh.addPhysicalGroup(2,s[0:1]+ s[3:4] + s[6:7] ,name='Intima')
sh.addPhysicalGroup(2,s[1:2]+ s[4:5] + s[7:8] ,name='Media')
sh.addPhysicalGroup(2,s[2:3]+ s[5:6] + s[8:9] ,name='Adventitia')
sh.addPhysicalGroup(1,l21[3:4], name='FSInterface')
sh.addPhysicalGroup(1,l11[0:1] + l11[3:4] + l12[0:1] + l13[0:1] + l31[2:4] + l32[2:3] + l33[2:3],name='Sides')
sh.addPhysicalGroup(1,l13[1:2] + l33[1:2],name='Ext')


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



