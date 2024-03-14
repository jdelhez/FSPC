import os, sys
sys.path.append('examples')
import toolbox as tb
import gmsh

# |-------------------------------|
# |   Data From the Literature    |
# |-------------------------------|

data = list()

# Onate results

data.append(
[[0.00000, 180.00000],
[0.393873, 180.00000],
[0.752735, 181.11111],
[1.120350, 185.18518],
[1.435449, 190.74074],
[1.829322, 200.37037],
[2.223195, 211.11111],
[2.625821, 222.59259],
[3.080963, 234.81481],
[3.571116, 247.77778],
[4.201313, 262.22222],
[4.761488, 272.96296],
[5.312910, 282.59259],
[5.986871, 291.48148],
[6.538293, 298.14814],
[7.291028, 305.92592],
[7.982495, 311.48148]])

data.append(
[[0.00000, 200.00000],
[0.385120, 200.00000],
[0.735230, 200.37037],
[1.102845, 203.70370],
[1.531729, 210.37037],
[1.881838, 217.40740],
[2.223195, 225.55555],
[2.582057, 234.44444],
[2.932166, 242.22222],
[3.308534, 251.11111],
[3.711160, 260.00000],
[4.280088, 271.11111],
[4.822757, 280.37037],
[5.391685, 288.51851],
[5.916849, 295.18518],
[6.555799, 301.48148],
[7.212254, 307.40740],
[7.991247, 313.70370]])

data.append(
[[0.00000, 220.00000],
[0.411379, 220.00000],
[0.700219, 220.37037],
[0.989059, 222.59259],
[1.330416, 227.03703],
[1.680525, 233.33333],
[2.118162, 241.85185],
[2.564551, 252.22222],
[3.045952, 262.59259],
[3.501094, 270.74074],
[3.991247, 279.25925],
[4.472648, 287.03703],
[4.989059, 293.70370],
[5.496718, 299.62963],
[6.214442, 307.03703],
[6.940919, 312.96296],
[7.982495, 318.88889]])

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

T = [list() for _ in range(3)]
position = [[0.2, 0.28, 0], [0.45, 0.28, 0], [0.7, 0.28, 0]]
os.chdir('workspace/metafor')

time, directory = tb.read_files()
tag = [tb.find_node(directory[0], P) for P in position]

for i, file in enumerate(directory):

    gmsh.open(file)
    D = gmsh.view.getModelData(0, i)[2]
    for i, R in enumerate(T): R.append(D[tag[i] - 1][0])

tb.plot_ref(time, T, data)