# Path to the external library

. /etc/profile.d/setup_env.sh

export PYTHONPATH=${PWD}:${PYTHONPATH}
export PYTHONPATH=${PWD}/pyStream/build:${PYTHONPATH}
export PYTHONPATH=${PWD}/../Metafor/oo_meta:${PYTHONPATH}
export PYTHONPATH=${PWD}/../Metafor/oo_metaB/bin:${PYTHONPATH}
export PYTHONPATH=${PWD}/../PFEM3D/build/bin:${PYTHONPATH}

# Path to the Python script

#export SCRIPT=${PWD}/examples/2D/damBreak/main.py
# export SCRIPT=${PWD}/AneurismAxisym_20_3/main.py
# export SCRIPT=${PWD}/R7_StraightArtery/main.py
# export SCRIPT=${PWD}/V1_AorticValve/main.py
# export SCRIPT=${PWD}/C3_StraightArtery/main.py

# export SCRIPT=${PWD}/R1_Aneurism/main.py
# export SCRIPT=${PWD}/examples/2D/carsherWall/main.py
# export SCRIPT=${PWD}/examples/2D/coolingDisk/main.py
# export SCRIPT=${PWD}/examples/2D/elasticFunnel/main.py
# export SCRIPT=${PWD}/examples/2D/flowContact/main.py
# export SCRIPT=${PWD}/examples/2D/hydroStatic/main.py
# export SCRIPT=${PWD}/examples/2D/rubberGate/main.py
# export SCRIPT=${PWD}/examples/2D/staticAxisym/main.py
# export SCRIPT=${PWD}/examples/2D/thermoSquare/main.py
# export SCRIPT=${PWD}/examples/2D/vonKarman/main.py

# export SCRIPT=${PWD}/examples/3D/carsherWall/main.py
# export SCRIPT=${PWD}/examples/3D/coolingDisk/main.py
# export SCRIPT=${PWD}/examples/3D/crossFlow/main.py
# export SCRIPT=${PWD}/examples/3D/damBreak/main.py
# export SCRIPT=${PWD}/examples/3D/hydroStatic/main.py

# export SCRIPT=${PWD}/AneurismAxisym_20_3/main.py

export SCRIPT1=${PWD}/R1_StraightArtery/main.py
export SCRIPT2=${PWD}/R2_StraightArtery/main.py
export SCRIPT3=${PWD}/R3_StraightArtery/main.py
export SCRIPT4=${PWD}/R4_StraightArtery/main.py
export SCRIPT5=${PWD}/R5_StraightArtery/main.py
export SCRIPT6=${PWD}/R6_StraightArtery/main.py
export SCRIPT7=${PWD}/R7_StraightArtery/main.py
export SCRIPT8=${PWD}/R8_StraightArtery/main.py


# Clean output folder

rm -rf workspace
mkdir workspace
cd workspace

# Run the code

export CPU_PER_PROC=2
export THR_PER_PROC=4
export MKL_NUM_THREADS=${THR_PER_PROC}
export OMP_NUM_THREADS=${THR_PER_PROC}
export OPTION="-map-by node:PE=${CPU_PER_PROC}"


# mpiexec ${OPTION} -n 2 python3 ${SCRIPT1} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt

# cd ..
# python3 myresults.py
# mv workspace R1_workspace
# mkdir workspace
# cd workspace

mpiexec ${OPTION} -n 2 python3 ${SCRIPT2} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt

cd ..
python3 myresults.py
mv workspace R2_workspace
mkdir workspace
cd workspace


mpiexec ${OPTION} -n 2 python3 ${SCRIPT3} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt

cd ..
python3 myresults.py
mv workspace R3_workspace
mkdir workspace
cd workspace


mpiexec ${OPTION} -n 2 python3 ${SCRIPT4} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt


cd ..
python3 myresults.py
mv workspace R4_workspace
mkdir workspace
cd workspace



# mpiexec ${OPTION} -n 2 python3 ${SCRIPT7} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt

# cd ..
# python3 myresults.py
# mv workspace R7_workspace
# mkdir workspace
# cd workspace


# mpiexec ${OPTION} -n 2 python3 ${SCRIPT8} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt
# 
# cd ..
# python3 myresults.py
# mv workspace R8_workspace
# mkdir workspace
# cd workspace

# mpiexec ${OPTION} -n 2 python3 ${SCRIPT5} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt

# cd ..
# python3 myresults.py
# mv workspace R5_workspace
# mkdir workspace
# cd workspace

mpiexec ${OPTION} -n 2 python3 ${SCRIPT6} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt

cd ..
python3 myresults.py
mv workspace R6_workspace
