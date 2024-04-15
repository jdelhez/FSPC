# Path to the external library

. /etc/profile.d/setup_env.sh

export PYTHONPATH=${PWD}:${PYTHONPATH}
export PYTHONPATH=${PWD}/pyStream/build:${PYTHONPATH}
export PYTHONPATH=${PWD}/../Metafor/oo_meta:${PYTHONPATH}
export PYTHONPATH=${PWD}/../Metafor/oo_metaB/bin:${PYTHONPATH}
export PYTHONPATH=${PWD}/../PFEM3D/build/bin:${PYTHONPATH}

# Path to the Python script

export SCRIPT1=${PWD}/Vein_Newton/main.py
export SCRIPT2=${PWD}/Vein_Casson/main.py


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


mpiexec ${OPTION} -n 2 python3 ${SCRIPT1} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt

cd ..
mv workspace /ws_Newton

mkdir workspace
cd workspace

mpiexec ${OPTION} -n 2 python3 ${SCRIPT2} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt


cd ..
mv workspace /ws_Casson

