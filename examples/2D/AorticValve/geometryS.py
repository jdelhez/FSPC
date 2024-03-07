import os,gmsh
from gmsh import model as sh
gmsh.initialize()

import math 
# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L = 0.016
Z = 0.0125 
R = 0.0215 
f = 2*R
t1 = 0.0010
t2 = 0.0005

rho = (math.sqrt(R**2 - Z**2 + 0.25*(R-Z)**2))
phi = math.atan(R-Z)/(2*math.sqrt(R**2-Z**2))
theta = L/rho

# Characteristic size
# to be adjusted 
d = 0.0002
N = 11
M = 41

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0,0,0,d)) # 0

x1=-f
y1=-Z
p.append(sh.occ.addPoint(x1,y1,0,d)) # 1

x2=-math.sqrt(R**2 - Z**2)
y2=-Z
p.append(sh.occ.addPoint(x2,y2,0,d)) # 2

x3=-rho*math.cos(theta+phi)
y3=rho*math.sin(theta+phi)-(R+Z)/2

p.append(sh.occ.addPoint(x3,y3,0,d)) # 3

x4=-(rho-t2)*math.cos(theta+phi)
y4=(rho-t2)*math.sin(theta+phi)-(R+Z)/2

p.append(sh.occ.addPoint(x4,y4,0,d)) # 4

y5=-(-(rho-t2)**2+R**2+0.25*(R+Z)**2)/(R+Z)
x5=-math.sqrt(R**2-y5**2)

p.append(sh.occ.addPoint(x5,y5,0,d)) # 5

p.append(sh.occ.addPoint(-x2,y2,0,d)) # 6
p.append(sh.occ.addPoint(-x1,y1,0,d)) # 7

p.append(sh.occ.addPoint(-x1,y1-t1,0,d)) # 8

x9=math.sqrt((R+t1)**2-(Z+t1)**2)
y9=-(Z+t1)
p.append(sh.occ.addPoint(x9,y9,0,d)) # 9
p.append(sh.occ.addPoint(-x9,y9,0,d)) # 10
p.append(sh.occ.addPoint(x1,y9,0,d)) # 11

# Centre du petit cercle
p.append(sh.occ.addPoint(0,-(R+Z)/2,0,d)) # 12


# Autre moitié

p.append(sh.occ.addPoint(x1,-y1,0,d)) # 13
p.append(sh.occ.addPoint(x2,-y2,0,d)) # 14
p.append(sh.occ.addPoint(x3,-y3,0,d)) # 15
p.append(sh.occ.addPoint(x4,-y4,0,d)) # 16
p.append(sh.occ.addPoint(x5,-y5,0,d)) # 17
p.append(sh.occ.addPoint(-x2,-y2,0,d)) # 18
p.append(sh.occ.addPoint(-x1,-y1,0,d)) # 19
p.append(sh.occ.addPoint(-x1,-y1+t1,0,d)) # 20
p.append(sh.occ.addPoint(x9,-y9,0,d)) # 21
p.append(sh.occ.addPoint(-x9,-y9,0,d)) # 22
p.append(sh.occ.addPoint(x1,-y1+t1,0,d)) # 23

p.append(sh.occ.addPoint(0,+(R+Z)/2,0,d)) # 24



# Lines List

l = list()
h = list()


l.append(sh.occ.addLine(p[1],p[2])) # 0
l.append(sh.occ.addCircleArc(p[2],p[12],p[3])) # 1
l.append(sh.occ.addLine(p[3],p[4])) # 2
l.append(sh.occ.addCircleArc(p[4],p[12],p[5])) # 3
l.append(sh.occ.addCircleArc(p[5],p[0],p[6])) # 4
l.append(sh.occ.addLine(p[6],p[7])) # 5
l.append(sh.occ.addLine(p[7],p[8])) # 6
l.append(sh.occ.addLine(p[8],p[9])) # 7
l.append(sh.occ.addCircleArc(p[9],p[0],p[10])) # 8
l.append(sh.occ.addLine(p[10],p[11])) # 9
l.append(sh.occ.addLine(p[11],p[1])) # 10


h.append(sh.occ.addLine(p[13],p[23])) # 0
h.append(sh.occ.addLine(p[23],p[22])) # 1
h.append(sh.occ.addCircleArc(p[22],p[0],p[21])) # 2
h.append(sh.occ.addLine(p[21],p[20])) # 3
h.append(sh.occ.addLine(p[20],p[19])) # 4
h.append(sh.occ.addLine(p[19],p[18])) # 5
h.append(sh.occ.addCircleArc(p[18],p[0],p[17])) # 6
h.append(sh.occ.addCircleArc(p[17],p[24],p[16])) # 7
h.append(sh.occ.addLine(p[16],p[15])) # 8
h.append(sh.occ.addCircleArc(p[15],p[24],p[14])) # 9
h.append(sh.occ.addLine(p[14],p[13])) # 10



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

sh.mesh.setAlgorithm(2,s[0],8)
sh.mesh.setAlgorithm(2,s[1],8)
sh.occ.synchronize()

# On est obligé de faire un transfinite curve mesh en fait??  --> Jsp du tout comment faire en fait mdr. 

#sh.mesh.setTransfiniteCurve(l[1],N)
#sh.mesh.setTransfiniteCurve(h[1],N)

#sh.mesh.setTransfiniteCurve(l[9],N)
#sh.mesh.setTransfiniteCurve(h[9],N)

#sh.mesh.setTransfiniteCurve(l[2],M)
#sh.mesh.setTransfiniteCurve(l[3],N)

#sh.mesh.setTransfiniteCurve(h[0],M)
#sh.mesh.setTransfiniteCurve(h[1],N)
#sh.mesh.setTransfiniteCurve(h[2],M)
#sh.mesh.setTransfiniteCurve(h[3],N)

#sh.mesh.setTransfiniteSurface(s[0]) 
#sh.mesh.setTransfiniteSurface(s[1]) 
# sh.occ.synchronize()

sh.mesh.setRecombine(2,s[0])
sh.mesh.setRecombine(2,s[1])
sh.occ.synchronize()


# Physical Boundary
# Jsp quel groupe de curve il faut grouper en fait 

sh.addPhysicalGroup(2,[s[0]],name='SolidBottom')
sh.addPhysicalGroup(2,[s[1]],name='SolidUp')

sh.addPhysicalGroup(1,l[0:6] +h[17:23] , name='FSInterface')
# Changer si jamais on met le solide rigide et juste les valves qui sont flex
# sh.addPhysicalGroup(1,l[0:1] + l[5:6] +h[17:18] +h[12:23], name='RigidSide')
# sh.addPhysicalGroup(1,l[1:4] +h[17:23] +h[19:22], name='FSInterface')


sh.addPhysicalGroup(1,l[11:12] + l[7:8] + h[5:6] + h[0:1],name='Sides')

sh.addPhysicalGroup(1,l[1:5] + h[6:10],name='Ext')

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



