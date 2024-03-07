import os,gmsh
from gmsh import model as sh
gmsh.initialize()

import math 
from scipy.optimize import fsolve

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|


# Characteristic size


N = 5
M = 41

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

mm = 1e-3
Z = 6*mm 
R = 18*mm 
H = 3*mm 
W = 12*mm 
Ro = 60*mm
theta = math.pi*0.25
t = 1*mm 

# Characteristic size
# to be adjusted 
d = 0.0003
N = 11
M = 41

def syst1(var): # définition du système
        x, y = var[0], var[1] # définition des variables
        eq1 = x**2 + y**2 - (Ro-Z)**2 
        eq2 = (x - (Ro+H)*math.cos(theta))**2 + (y - (Ro+H)*math.cos(theta))**2  - R**2
        res1 = [eq1, eq2]
        return res1

x0, y0= 0, 0 # Initialisation de la recherche des solutions numériques
sol_ini = [x0, y0]

sol1 = fsolve(syst1, sol_ini)

#print("Numerical Solution (x, y):", sol1)

if sol1[1] > sol1[0]: 
    x8 = sol1[0]
    y8 = sol1[1]

def syst1bis(var): # définition du système
        x, y = var[0], var[1] # définition des variables
        eq1 = x**2 + y**2 - (Ro-Z-t)**2 
        eq2 = (x - (Ro+H)*math.cos(theta))**2 + (y - (Ro+H)*math.cos(theta))**2  - (R+t)**2
        resbis = [eq1, eq2]
        return resbis

x0, y0= 0, 0 # Initialisation de la recherche des solutions numériques
sol_ini = [x0, y0]

sol1bis = fsolve(syst1bis, sol_ini)

if sol1bis[1] > sol1bis[0]: 
    x3 = sol1bis[0]
    y3 = sol1bis[1]


def syst2(var): # définition du système
        x, y = var[0], var[1] # définition des variables
        eq1 = x**2 + y**2 - (Ro+Z)**2 
        eq2 = (x - (Ro+H)*math.cos(theta))**2 + (y - (Ro+H)*math.cos(theta))**2  - R**2
        res2 = [eq1, eq2]
        return res2

x0, y0= 0, 0 # Initialisation de la recherche des solutions numériques
sol_ini = [x0, y0]

sol2 = fsolve(syst2, sol_ini)

if sol2[1] > sol2[0]: 
    x15= sol2[0]
    y15 = sol2[1]


def syst2bis(var): # définition du système
        x, y = var[0], var[1] # définition des variables
        eq1 = x**2 + y**2 - (Ro+Z+t)**2 
        eq2 = (x - (Ro+H)*math.cos(theta))**2 + (y - (Ro+H)*math.cos(theta))**2  - (R+t)**2
        res2bis = [eq1, eq2]
        return res2bis

x0, y0= 0, 0 # Initialisation de la recherche des solutions numériques
sol_ini = [x0, y0]

sol2bis = fsolve(syst2bis, sol_ini)

if sol2bis[1] > sol2bis[0]: 
    x20= sol2bis[0]
    y20 = sol2bis[1]

print("Numerical Solution (x, y):", sol2bis)


# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|


p = list()

# Adapter en mettant des equations au lieu des coordonnees des points en vrai !! 

p.append(sh.occ.addPoint(-W,Ro-Z,0,d)) # 0
p.append(sh.occ.addPoint(-W,Ro-Z-t,0,d)) # 1
p.append(sh.occ.addPoint(0,Ro-Z-t,0,d)) # 2
p.append(sh.occ.addPoint(x3,y3,0,d)) # 3 
p.append(sh.occ.addPoint(y3,x3,0,d)) # 4 
p.append(sh.occ.addPoint(Ro-Z-t, 0, 0, d)) # 5 
p.append(sh.occ.addPoint(Ro-Z, 0, 0, d)) # 6
p.append(sh.occ.addPoint(y8,x8,0,d)) # 7
p.append(sh.occ.addPoint(x8,y8,0,d)) # 8
p.append(sh.occ.addPoint(0,Ro-Z,0,d)) # 9

p.append(sh.occ.addPoint(0,0,0,d)) #10
p.append(sh.occ.addPoint(math.cos(theta)*(Ro + H), math.sin(theta)*(Ro+H), 0, d)) # 11


p.append(sh.occ.addPoint(-W,Ro+Z+t,0,d)) # 12
p.append(sh.occ.addPoint(-W,Ro+Z,0,d)) # 13
p.append(sh.occ.addPoint(0,Ro+Z,0,d)) # 14
p.append(sh.occ.addPoint(x15, y15, 0, d)) # 15
p.append(sh.occ.addPoint(y15, x15, 0, d)) # 16
p.append(sh.occ.addPoint(Ro+Z, 0, 0, d)) # 17
p.append(sh.occ.addPoint(Ro+Z+t, 0, 0, d)) # 18
p.append(sh.occ.addPoint(y20,x20,0,d)) # 19
p.append(sh.occ.addPoint(x20,y20,0,d)) # 20
p.append(sh.occ.addPoint(0,Ro+Z+t,0,d)) # 21

# Lines List

l = list()

l.append(sh.occ.addLine(p[0],p[1])) # 0
l.append(sh.occ.addLine(p[1],p[2])) # 1
l.append(sh.occ.addCircleArc(p[2],p[10],p[3])) # 2
l.append(sh.occ.addCircleArc(p[3],p[11],p[4])) # 3
l.append(sh.occ.addCircleArc(p[4],p[10],p[5])) # 4
l.append(sh.occ.addLine(p[5],p[6])) # 5
l.append(sh.occ.addCircleArc(p[6],p[10],p[7])) # 6
l.append(sh.occ.addCircleArc(p[7],p[11],p[8])) # 7
l.append(sh.occ.addCircleArc(p[8],p[10],p[9])) # 8
l.append(sh.occ.addLine(p[9],p[0])) # 9

h = list()

h.append(sh.occ.addLine(p[12],p[13])) # 0
h.append(sh.occ.addLine(p[13],p[14])) # 1
h.append(sh.occ.addCircleArc(p[14],p[10],p[15])) # 2
h.append(sh.occ.addCircleArc(p[15],p[11],p[16])) # 3
h.append(sh.occ.addCircleArc(p[16],p[10],p[17])) # 4
h.append(sh.occ.addLine(p[17],p[18])) # 5
h.append(sh.occ.addCircleArc(p[18],p[10],p[19])) # 6
h.append(sh.occ.addCircleArc(p[19],p[11],p[20])) # 7
h.append(sh.occ.addCircleArc(p[20],p[10],p[21])) # 8
h.append(sh.occ.addLine(p[21],p[12])) # 9


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

#sh.mesh.setAlgorithm(2,s[0],8)
#sh.mesh.setAlgorithm(2,s[1],8)
#sh.occ.synchronize()

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

sh.addPhysicalGroup(1,l[6:10] +h[1:5] , name='FSInterface')

sh.addPhysicalGroup(1,l[0:1] + l[5:6] + h[5:6] + h[0:1],name='Sides')

# sh.addPhysicalGroup(1,l[1:5] + h[6:10],name='Ext')

sh.addPhysicalGroup(1,l[1:3] + l[4:5] + h[6:7] + h[8:10],name='Ext')

# sh.addPhysicalGroup(1,l[1:3] + l[4:5],name='Ext')


# sh.addPhysicalGroup(1,l[3:4] + h[7:8],name='Aneurysm')








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



