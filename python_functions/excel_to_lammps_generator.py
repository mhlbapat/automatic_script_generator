import numpy as np
import os
import pandas as pd

import platform
if platform.system()=='Windows':
	slash_use = r'\\'
else:
	slash_use = '/'

def excel_to_lammps_generator(path_excel_file, new_dir_name, path_lammps_files):
	lammps_filenames = os.listdir(path_lammps_files)
	values_file_new = pd.read_excel(path_excel_file)

	property_names_new = values_file_new[values_file_new.columns[0]]
	property_vals_new = values_file_new[values_file_new.columns[1]]

	script_name = (new_dir_name +slash_use+ 'gcmc_fluid_flow_temp' + str(property_vals_new[property_names_new=='temperature'].values[0]) 
		+ '_num_mem_' + str(property_vals_new[property_names_new=='num_membranes'].values[0]) + '.in')


	# Initialize the base script
	lammps_script = open(script_name, "w+")

	for i in lammps_filenames:
		temp_file_name = open(path_lammps_files + slash_use + i, "r")
		temp_content = temp_file_name.read()
		lammps_script.write(temp_content)

	lammps_script.close()

	# Re-read the content
	lammps_script = open(script_name, "rt")
	temp_content = lammps_script.read()
	lammps_script.close()

	# Replace temporary variables with actual values
	for i in range(len(property_names_new)):
		temp_name = property_names_new[i] + '_valpy'
		temp_content = temp_content.replace(temp_name, str(property_vals_new[i]))

	# Change the output frequecy for lammps trajectory based on the gcmc_eqm_time, default multiplier: 0.02
	trajectory_times_defvalpy = str(int(0.02*property_vals_new[property_names_new=='gcmc_eqm_time'].values[0]))
	temp_content = temp_content.replace('trajectory_times_defvalpy',trajectory_times_defvalpy)

	# Change the output frequecy for velocity averaging based on the gcmc_eqm_time
	binvelavg_defvalpy = str(int(0.001*property_vals_new[property_names_new=='gcmc_eqm_time'].values[0]))
	temp_content = temp_content.replace('binvelavg_defvalpy',binvelavg_defvalpy)

	# Change the output frequecy for ncount averaging based on the gcmc_eqm_time
	force_on_membrane_defvalpy = str(int(0.02*property_vals_new[property_names_new=='gcmc_eqm_time'].values[0]))
	temp_content = temp_content.replace('force_on_membrane_defvalpy',force_on_membrane_defvalpy)

	# Change Nose-Hoover damp constant
	temp_content = temp_content.replace('nose_hoover_damp_defvalpy', '10000')

	# solid_wall_filename = property_vals_new[property_names_new=='read_data_solid'].values[0]

	# if solid_wall_filename == 'solid-walls-hcp.data':
	# 	temp_content = temp_content.replace('nose_hoover_damp_defvalpy', '20000')
	# if solid_wall_filename == 'solid-walls-replicated.data':
	# 	temp_content = temp_content.replace('nose_hoover_damp_defvalpy', '20000')
	# if solid_wall_filename == 'solid-walls-hcp-plus10.data':
	# 	temp_content = temp_content.replace('nose_hoover_damp_defvalpy', '20000')
	# if solid_wall_filename == 'solid-walls-hcp-minus10.data':
	# 	temp_content = temp_content.replace('nose_hoover_damp_defvalpy', '20000')
	# if solid_wall_filename == 'solid-walls-hcp-plus20.data':
	# 	temp_content = temp_content.replace('nose_hoover_damp_defvalpy', '20000')

# # 11 June 2021 - Fork here
# 	submega_half_shear = property_vals_new[property_names_new=='submega_half_shear'].values[0]
# 	mass_solid = property_vals_new[property_names_new=='mass_solid'].values[0]
# 	mass_fluid = property_vals_new[property_names_new=='mass_fluid'].values[0]
# 	sigma_FS = property_vals_new[property_names_new=='sigma_FS'].values[0]
# 	sigma_FF = property_vals_new[property_names_new=='sigma_FS'].values[0]
# 	epsilon_FS = property_vals_new[property_names_new=='epsilon_FS'].values[0]
# 	epsilon_FF = property_vals_new[property_names_new=='epsilon_FF'].values[0]
# 	fluid_fluid_time = np.sqrt(mass_fluid*(sigma_FF**2)/epsilon_FF)*1.55
# 	solid_fluid_time = 1.55*np.sqrt(mass_fluid*mass_solid*(sigma_FS**2)/epsilon_FS*(mass_fluid+mass_solid))
# 	z_value = property_vals_new[property_names_new=='z'].values[0]
# 	shear_rate_time = z_value/submega_half_shear

# 	tstep = np.round(np.min([fluid_fluid_time, solid_fluid_time, shear_rate_time])*0.1,3)
# 	temp_content = temp_content.replace('tstep_valpy', str(tstep))


	# Save to the original file
	lammps_script = open(script_name,"wt")
	lammps_script.write(temp_content)
	lammps_script.close()

	return script_name