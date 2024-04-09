import os,sys
sys.path.append('examples')
import toolbox as tb
import gmsh
import numpy as np

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|


os.chdir('./R2_workspace/metafor')

time,directory = tb.read_files()

imin = 200
imax = 400
di = 5

x1 = 0.01
y1 = -0.005
x2 = 0.01
y2 = 0.005

# gmsh.open(file)
p1 = [x1, y1, 0]
p2 = [x2, y2, 0]
tag1=tb.find_node(directory[0],p1)
tag2=tb.find_node(directory[0],p2)

tagmin = np.min([tag1, tag2])
tagmax = np.max([tag1, tag2])

WSS_array = list()

for idt,file in enumerate(directory):
    if (imin <= idt < imax) and ((idt-imin) %  di)==0 :

        gmsh.open(file)
        print(file)
        flag = 0
        WSS_lst = list()

        for i in range(tagmin,tagmax+1):
            XNew = gmsh.model.mesh.getNode(i)[0][0]
            YNew = gmsh.model.mesh.getNode(i)[0][1]

            # VMSNew = gmsh.view.getModelData(0,idt)[2][i-1][0]
            SYYNew = gmsh.view.getModelData(1,idt)[2][i-1][0]
            # SZZNew = gmsh.view.getModelData(2,idt)[2][i-1][0]
            SXYNew = gmsh.view.getModelData(3,idt)[2][i-1][0]
            SXXNew = gmsh.view.getModelData(4,idt)[2][i-1][0]

            if (flag>0):
                DX = (XNew-XOld)
                DY = (YNew-YOld)
                norm=np.sqrt(DX*DX+DY*DY)
                NX = DY / norm
                NY = -DX / norm
                SXX = (SXXNew + SXXOld)/2
                SXY = (SXYNew + SXYOld)/2
                SYY = (SYYNew + SYYOld)/2
                TX = SXX*NX + SXY*NY
                TY = SXY*NX + SYY*NY
                WSS =+ TX * NY - TY * NX
                WSS_lst.append(WSS)

            flag = 1
            XOld = XNew
            YOld = YNew
            SXXOld = SXXNew
            SXYOld = SXYNew
            SYYOld = SYYNew
        
        WSS_array.append(WSS_lst)

Data = np.asarray(WSS_array)

np.savetxt("../WWSResu.txt",Data)
