# Submission script for LAMMPS_file_name_valpy
# This file will be run locally with:
# nodes_valpy nodes
# cores_valpy cores
# threads_valpy threads
mpiexec -localonly cores_valpy lmp_mpi -in LAMMPS_file_name_valpy -pk omp threads_valpy -sf omp