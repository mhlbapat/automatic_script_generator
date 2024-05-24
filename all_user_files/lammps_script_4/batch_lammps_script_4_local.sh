# Submission script for slip-flow_temp-350_1e5half-shear_50.in
# This file will be run locally with:
# 1 nodes
# 4 cores
# 1 threads
mpiexec -localonly 4 lmp_mpi -in slip-flow_temp-350_1e5half-shear_50.in -pk omp 1 -sf omp