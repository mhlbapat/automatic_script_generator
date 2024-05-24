import numpy as np
import os
import pandas as pd

#%matplotlib inline
from python_functions.excel_to_lammps_generator import excel_to_lammps_generator
from python_functions.copy_data_file import copy_data_file
from python_functions.generate_batch_script import generate_batch_script

import platform
if platform.system()=='Windows':
	slash_use = r'\\'
else:
	slash_use = '/'

def all_files_generator(path_excel_file, path_lammps_files):

	'''
	Input: Path to the excel file with all the data.
	
	Output: Creates an 'all-scripts-files' directory which contains
	the sub-directories (lammps_script_*) with the following:
		- LAMMPS script for a parameter combination (.in file).
		- Batch script to  run the particular LAMMPS file on cluster.
		- Excel file corresponding to '.in file'
		- Data file for solid wall

	'''

	# To be provided by the user for cluster computing
	print('\n Enter the following: \n')
	n_nodes = int(1) #int(input('Number of nodes \n') or "1")
	n_cores = int(4) #int(input('Number of cores \n') or "1")
	n_threads = int(1) #int(input('Number of threads \n') or "1")


	# Reads the default LAMMPS files and combine them into one
	lammps_filenames = os.listdir(path_lammps_files)

	# Reads the excel configuration file
	values_file = pd.read_excel(path_excel_file)


	property_names = values_file[values_file.columns[0]]
	property_vals = values_file[values_file.columns[1]]

	property_lengths = np.ones(len(property_names), dtype = int)
	
	# Check for length
	for i in range(len(property_vals)):
		temp_property_val = property_vals[i]

		if type(temp_property_val) == str:
			try:
				a = [float(y) for y in [x.replace(' ', '') for x in temp_property_val.split(',')]]
			except:
				a = [x.replace(' ', '') for x in temp_property_val.split(',')]
			property_lengths[i] = len(a)
			

		if type(temp_property_val) == list:
			a = [float(y) for y in [x.replace(' ', '') for x in temp_property_val.split(',')]]
			property_lengths[i] =  len(a)
			
		if (type(temp_property_val) == float) | (type(temp_property_val) == int) :
			a = temp_property_val
			property_lengths[i] =  1
			
	# Extract values for which length > 1
	loop_names = property_names[property_lengths>1].values

	############## Check for length > 1 parameters.
	############## If only single run is to be executed generate excel file directly.
	if len(loop_names)>0:
		print('Generating '+str(np.prod(property_lengths))+' folders. Looping over: ', loop_names)
		parameter_loop_vals = []
		for i in range(len(loop_names)):
			temp_property_val = property_vals[property_names.values==loop_names[i]].values[0]

			try:
				a = [float(y) for y in [x.replace(' ', '') for x in temp_property_val.split(',')]]
			except:
				a = [x.replace(' ', '') for x in temp_property_val.split(',')]
			parameter_loop_vals.append(a)
		

		# Create mesh grid to loop over
		counter_vals = [list(range(property_lengths[property_names==i][0])) for i in loop_names]
		counter_loops = np.meshgrid(*counter_vals)
		counter_list = []
		for index,x in np.ndenumerate(counter_loops[0]):
			# counter_list[i][j] corresponds to loop_name[i] and parameter_loop_vals[i][j]
			counter_list.append([counter_loops[i][index] for i in range(np.shape(counter_loops)[0])])


		for i in range(len(counter_list)):
			curr_counter_list = counter_list[i]
			try:
				os.mkdir('all_user_files')
			except:
				pass
			
			new_dir_name = 'all_user_files'+ slash_use +'lammps_script_'+str(i)
			new_excel_file = new_dir_name+'/value-file-lammps_'+str(i)+'.xlsx'
			
			try:
				os.mkdir(new_dir_name)
			except:
				pass
			
			values_file_new = values_file.copy()
			property_names_new = values_file_new[values_file_new.columns[0]]
			property_vals_new  = values_file_new[values_file_new.columns[1]]

			for j, jval in enumerate(curr_counter_list):
				property_vals_new[property_names_new.values==loop_names[j]] = parameter_loop_vals[j][jval]

			values_file_new.to_excel(new_excel_file, index=False)
			source_data_file_liquid = property_vals_new.values[property_names_new.values=='read_data_liquid'][0]
			source_data_file_solid = property_vals_new.values[property_names_new.values=='read_data_solid'][0]

			lammps_script_name = excel_to_lammps_generator(new_excel_file, new_dir_name, path_lammps_files)
			copy_data_file(source_data_file_liquid, new_dir_name+slash_use)
			copy_data_file(source_data_file_solid, new_dir_name+slash_use)
			generate_batch_script(n_nodes, n_cores, n_threads, new_dir_name, lammps_script_name)


	else:
		values_file_new = values_file.copy()
		try:
				os.mkdir('all_user_files')
		except:
				pass
		property_names_new = values_file_new[values_file_new.columns[0]]
		property_vals_new  = values_file_new[values_file_new.columns[1]]

		new_dir_name = 'all_user_files'+ slash_use + 'lammps_script_0'
		source_data_file = property_vals_new.values[property_names_new.values=='read_data'][0]

		new_excel_file = new_dir_name+slash_use+'value-file-lammps_0.xlsx'

		try:
				os.mkdir(new_dir_name)
		except:
				pass
		values_file_new.to_excel(new_excel_file, index=False)
		lammps_script_name = excel_to_lammps_generator(new_excel_file, new_dir_name)
		copy_data_file(source_data_file, new_dir_name+slash_use)
		generate_batch_script(n_nodes, n_cores, n_threads, new_dir_name, lammps_script_name)