import numpy as np
import os
import pandas as pd

import platform
if platform.system()=='Windows':
	slash_use = r'\\'
else:
	slash_use = '/'


def generate_batch_script(n_nodes, n_cores, n_threads, new_dir_name, lammps_file_name, path_generic_script='bash_script_files'+slash_use):



	lammps_script_number = new_dir_name.replace('all_user_files'+slash_use,'')
	lammps_file_name = lammps_file_name.replace(new_dir_name+slash_use,'')
	batch_script_cluster_name = new_dir_name + slash_use + 'batch_' + lammps_script_number + '.sh'

	batch_script_cluster = open(batch_script_cluster_name,'w+')
	generic_batch_script_cluster = open(path_generic_script+'generic_batch_script_cluster.sh','r')

	valpy_names = ['nodes', 'cores', 'threads', 'LAMMPS_file_name','LAMMPS_job_name','LAMMPS_output']
	valpy_vals = [n_nodes, n_cores, n_threads, lammps_file_name, lammps_script_number, lammps_script_number+'.stdout']

	temp_batch_script = generic_batch_script_cluster.read()

	for i in range(len(valpy_names)):
		curr_valpy_names = valpy_names[i] + '_valpy'
		temp_batch_script = temp_batch_script.replace(curr_valpy_names, str(valpy_vals[i]))

	batch_script_cluster.write(temp_batch_script)
	batch_script_cluster.close()


	batch_script_local_name = new_dir_name + slash_use +'batch_' + lammps_script_number + '_local.sh'

	batch_script_local = open(batch_script_local_name,'w+')
	generic_batch_script_local = open(path_generic_script+'generic_batch_script_local.sh','r')

	valpy_names = ['nodes', 'cores', 'threads', 'LAMMPS_file_name','LAMMPS_job_name','LAMMPS_output']
	valpy_vals = [n_nodes, n_cores, n_threads, lammps_file_name, lammps_script_number, lammps_script_number+'.stdout']

	temp_batch_script = generic_batch_script_local.read()

	for i in range(len(valpy_names)):
		curr_valpy_names = valpy_names[i] + '_valpy'
		temp_batch_script = temp_batch_script.replace(curr_valpy_names, str(valpy_vals[i]))

	batch_script_local.write(temp_batch_script)
	batch_script_local.close()
