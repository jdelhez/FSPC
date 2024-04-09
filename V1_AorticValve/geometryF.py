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
d = 1e-3
N = 41

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

p.append(sh.occ.addPoint(-x1,-y1,0,d)) # 8
p.append(sh.occ.addPoint(-x2,-y2,0,d)) # 9
p.append(sh.occ.addPoint(x5,-y5,0,d)) # 10
p.append(sh.occ.addPoint(x4,-y4,0,d)) # 11
p.append(sh.occ.addPoint(x3,-y3,0,d)) # 12
p.append(sh.occ.addPoint(x2,-y2,0,d)) # 13
p.append(sh.occ.addPoint(x1,-y1,0,d)) # 14

# Centre du petit cercle
p.append(sh.occ.addPoint(0,-(R+Z)/2,0,d)) # 15
p.append(sh.occ.addPoint(0,+(R+Z)/2,0,d)) # 16

# Centers of tips
p.append(sh.occ.addPoint(0.5*(x3+x4),0.5*(y3+y4),0)) # 17
p.append(sh.occ.addPoint(0.5*(x3+x4),-0.5*(y3+y4),0)) # 18

# x6=-math.sqrt((R+t1)^2-(Z+t1)^2)
# y6=-(Z+t1)

# p.append(sh.occ.addPoint(x6,y6,0,d)) # 6


# Lines List

l = list()
# h = list()

l.append(sh.occ.addLine(p[1],p[2])) # 0
l.append(sh.occ.addCircleArc(p[2],p[15],p[3])) # 1
#l.append(sh.occ.addLine(p[3],p[4])) # 2
l.append(sh.occ.addCircleArc(p[3],p[17],p[4])) # 2
l.append(sh.occ.addCircleArc(p[4],p[15],p[5])) # 3
l.append(sh.occ.addCircleArc(p[5],p[0],p[6])) # 4
l.append(sh.occ.addLine(p[6],p[7])) # 5
l.append(sh.occ.addLine(p[7],p[8])) # 6
l.append(sh.occ.addLine(p[8],p[9])) # 7
l.append(sh.occ.addCircleArc(p[9],p[0],p[10])) # 8
l.append(sh.occ.addCircleArc(p[10],p[16],p[11])) # 9
#l.append(sh.occ.addLine(p[11],p[12])) # 10
l.append(sh.occ.addCircleArc(p[11],p[18],p[12])) # 10
l.append(sh.occ.addCircleArc(p[12],p[16],p[13])) # 11
l.append(sh.occ.addLine(p[13],p[14])) # 12
l.append(sh.occ.addLine(p[14],p[1])) # 13



# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l[0:14]) 

s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[1],N)
sh.mesh.setTransfiniteCurve(l[3],N)
sh.mesh.setTransfiniteCurve(l[9],N)
sh.mesh.setTransfiniteCurve(l[11],N)

# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,l[1:4]+l[9:12],name='FSInterface')
sh.addPhysicalGroup(1,l[0:1]+l[4:6]+l[7:9]+l[12:13],name='Boundary')
sh.addPhysicalGroup(1,l[13:14],name='Inlet')
sh.addPhysicalGroup(1,l[6:7],name='Outlet')

# |----------------------------------------|
# |   Mesh Characteristic Size Function    |
# |----------------------------------------|

# fun = str(d)+'+0.1*F1'
# sh.mesh.field.add('Distance',1)
# sh.mesh.field.setNumber(1,'Sampling',1e4)
# sh.mesh.field.setNumbers(1,'CurvesList',l)

# sh.mesh.field.add('MathEval',2)
# sh.mesh.field.setString(2,'F',fun)

# sh.mesh.field.setAsBackgroundMesh(2)
# gmsh.option.setNumber('Mesh.MeshSizeFromPoints',0)
# gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary',0)

# Write the Mesh File

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()