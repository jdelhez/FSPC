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

export SCRIPT=${PWD}/R1_StraightArtery/main.py
mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt
cp -r ${PWD}/workspace ${PWD}/R1_workspace
cd ..
rm -rf workspace
mkdir workspace
cd workspace

export SCRIPT=${PWD}/R2_StraightArtery/main.py
mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt
cp -r ${PWD}/workspace ${PWD}/R2_workspace
cd ..
rm -rf workspace
mkdir workspace
cd workspace

export SCRIPT=${PWD}/R3_StraightArtery/main.py
mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt
cp -r ${PWD}/workspace ${PWD}/R3_workspace
cd ..
rm -rf workspace
mkdir workspace
cd workspace

export SCRIPT=${PWD}/R4_StraightArtery/main.py
mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt
cp -r ${PWD}/workspace ${PWD}/R4_workspace
cd ..
rm -rf workspace
mkdir workspace
cd workspace

export SCRIPT=${PWD}/R5_StraightArtery/main.py
mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt
cp -r ${PWD}/workspace ${PWD}/R5_workspace
cd ..
rm -rf workspace
mkdir workspace
cd workspace

export SCRIPT=${PWD}/R6_StraightArtery/main.py
mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt
cp -r ${PWD}/workspace ${PWD}/R6_workspace
cd ..
rm -rf workspace
mkdir workspace
cd workspace

export SCRIPT=${PWD}/R7_StraightArtery/main.py
mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt
cp -r ${PWD}/workspace ${PWD}/R7_workspace
cd ..
rm -rf workspace
mkdir workspace
cd workspace

export SCRIPT=${PWD}/R8_StraightArtery/main.py
mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt
cp -r ${PWD}/workspace ${PWD}/R8_workspace
cd ..
rm -rf workspace
mkdir workspace
cd workspace





