import os,gmsh
from gmsh import model as sh
gmsh.initialize()

import math 
# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L = 0.0125
Z = 0.008 
R = 0.0125 
f = 2*R
t1 = 0.0010
t2 = 0.000324

rho = (math.sqrt(R**2 - Z**2 + 0.25*(R-Z)**2))
phi = math.atan(R-Z)/(2*math.sqrt(R**2-Z**2))
theta = L/rho

# Characteristic size
# to be adjusted 
N = 200
M = 15

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0,0,0)) # 0

x1=-f
y1=-Z
p.append(sh.occ.addPoint(x1,y1,0)) # 1

x2=-math.sqrt(R**2 - Z**2)
y2=-Z
p.append(sh.occ.addPoint(x2,y2,0)) # 2

x3=-rho*math.cos(theta+phi)
y3=rho*math.sin(theta+phi)-(R+Z)/2

p.append(sh.occ.addPoint(x3,y3,0)) # 3

x4=-(rho-t2)*math.cos(theta+phi)
y4=(rho-t2)*math.sin(theta+phi)-(R+Z)/2

p.append(sh.occ.addPoint(x4,y4,0)) # 4

y5=-(-(rho-t2)**2+R**2+0.25*(R+Z)**2)/(R+Z)
x5=-math.sqrt(R**2-y5**2)

p.append(sh.occ.addPoint(x5,y5,0)) # 5

p.append(sh.occ.addPoint(-x2,y2,0)) # 6
p.append(sh.occ.addPoint(-x1,y1,0)) # 7

p.append(sh.occ.addPoint(-x1,y1-t1,0)) # 8

x9=math.sqrt((R+t1)**2-(Z+t1)**2)
y9=-(Z+t1)
p.append(sh.occ.addPoint(x9,y9,0)) # 9
p.append(sh.occ.addPoint(-x9,y9,0)) # 10
p.append(sh.occ.addPoint(x1,y9,0)) # 11

# Centre du petit cercle
p.append(sh.occ.addPoint(0,-(R+Z)/2,0)) # 12


# Autre moitié

p.append(sh.occ.addPoint(x1,-y1,0)) # 13
p.append(sh.occ.addPoint(x2,-y2,0)) # 14
p.append(sh.occ.addPoint(x3,-y3,0)) # 15
p.append(sh.occ.addPoint(x4,-y4,0)) # 16
p.append(sh.occ.addPoint(x5,-y5,0)) # 17
p.append(sh.occ.addPoint(-x2,-y2,0)) # 18
p.append(sh.occ.addPoint(-x1,-y1,0)) # 19
p.append(sh.occ.addPoint(-x1,-y1+t1,0)) # 20
p.append(sh.occ.addPoint(x9,-y9,0)) # 21
p.append(sh.occ.addPoint(-x9,-y9,0)) # 22
p.append(sh.occ.addPoint(x1,-y1+t1,0)) # 23

p.append(sh.occ.addPoint(0,+(R+Z)/2,0)) # 24

# Centers of tips
p.append(sh.occ.addPoint(0.5*(x3+x4),0.5*(y3+y4),0)) # 25
p.append(sh.occ.addPoint(0.5*(x3+x4),-0.5*(y3+y4),0)) # 26



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

l2 = list()

l2.append(sh.occ.addCircleArc(p[5],p[12],p[4]))
l2.append(sh.occ.addCircleArc(p[3],p[25],p[4])) # 2
l2.append(sh.occ.addCircleArc(p[3],p[12],p[2])) # 1
l2.append(sh.occ.addLine(p[2],p[5])) # 0



h2 = list()

h2.append(sh.occ.addCircleArc(p[14],p[24],p[15])) # 9
h2.append(sh.occ.addCircleArc(p[16],p[26],p[15])) # 8
h2.append(sh.occ.addCircleArc(p[16],p[24],p[17])) # 7
h2.append(sh.occ.addLine(p[17],p[14])) # 8

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

# Comment fait-on quand on a plusieurs surfaces? 

k = list()
s = list()

k.append(sh.occ.addCurveLoop(l2))
k.append(sh.occ.addCurveLoop(h2))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()

# Je sais pas trop à quoi correspondent les lignes qui suivent et leur pertinence - tiré de l'example FlowContact  

#sh.mesh.setAlgorithm(2,s[0],8)
#sh.mesh.setAlgorithm(2,s[1],8)
#sh.occ.synchronize()

# On est obligé de faire un transfinite curve mesh en fait??  --> Jsp du tout comment faire en fait mdr. 

sh.mesh.setTransfiniteCurve(l2[0],N)
sh.mesh.setTransfiniteCurve(l2[2],N)
sh.mesh.setTransfiniteCurve(l2[1],M)
sh.mesh.setTransfiniteCurve(l2[3],M)
sh.mesh.setTransfiniteCurve(h2[0],N)
sh.mesh.setTransfiniteCurve(h2[2],N)
sh.mesh.setTransfiniteCurve(h2[1],M)
sh.mesh.setTransfiniteCurve(h2[3],M)

sh.occ.synchronize()

sh.mesh.setRecombine(2,s[0])
sh.mesh.setRecombine(2,s[1])
sh.occ.synchronize()


# Physical Boundary
# Jsp quel groupe de curve il faut grouper en fait 

sh.addPhysicalGroup(2,[s[0]],name='SolidBottom')
sh.addPhysicalGroup(2,[s[1]],name='SolidUp')

sh.addPhysicalGroup(1,l2[0:3] + h2[0:3],name='FSInterface')

sh.addPhysicalGroup(1,l2[1:3],name='LeafletBottom')
sh.addPhysicalGroup(1,h2[0:2],name='LeafletUp')


sh.addPhysicalGroup(1,l2[3:4] + h2[3:4],name='Sides')

# sh.addPhysicalGroup(1,l[1:5] + h[6:10],name='Ext')

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



