import os
import sys

os.chdir('..')
sys.path.insert(0,os.getcwd())
print(os.getcwd())

from python_functions.all_files_generator import all_files_generator
from python_functions.copy_data_file import copy_data_file
import pandas as pd
import numpy as np
import time
import datetime
from datetime import datetime

'''
Click in the excel file to perform:
- Create an 'all_user_files' directory
  If 'all_user_files' is already present it will be renamed as 'all_user_files_old' + old date and old time (separated with hyphens)
- Create LAMMPS (.in) , batch_cluster, batch_local (.sh) files in respective directories of the lammps scripts.
- Perform initial parameter check. This creates a file "initial_warnings.txt" with suggested changes.

'''

# datafile_to_run_simulations = np.loadtxt('simulation_files_to_run.csv',dtype='str', delimiter=',')

excel_sheet_to_read = 'script_parameters.xlsx'
lammps_folder_containing_scripts = 'lammps_base'

old_datetime = str(datetime.now()).replace(' ','_').replace(':','--')

already_present = os.listdir()
if 'all_user_files' in already_present:
	os.rename('all_user_files','all_user_files_old_'+old_datetime)

# all_files_generator(excel_sheet_to_read, lammps_folder_containing_scripts)

# try:
all_files_generator(excel_sheet_to_read, lammps_folder_containing_scripts)
print('Done...')
	
# except Exception as script_error:
	# sys.stdout = open("script_error.txt",'a')
	# print(script_error)
	# sys.stdout.close()


# For reading from data file - Files to run 1-May-2022
#datafile_to_run_simulations[datafile_to_run_simulations[:,0]=='excel_sheet_to_read',1][0]
#datafile_to_run_simulations[datafile_to_run_simulations[:,0]=='lammps_folder_containing_scripts',1][0]


# Perform parameter checks using funtions stored in "parameter_flags" folder
# sys.stdout = open("initial_warnings.txt",'a')




# Perform your parameter checks here. They will be stored in "initial_warnings.txt"
# from parameter_flags.read_data_file_initial_pcheck import read_data_file_initial_pcheck
# try:
# 	read_data_file_initial_pcheck(excel_sheet_to_read)
# except Exception as read_pcheck_error:
# 	pass

# from parameter_flags.


sys.stdout.close()