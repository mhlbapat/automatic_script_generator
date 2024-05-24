import os

def test_examplespresent():
	print(os.getcwd())
	assert os.path.exists('automatic_script_generator/data/excel-sheets/value-file-lammps-polymer.xlsx')
	assert os.path.exists('automatic_script_generator/data/lammps-files/slip-flow-scratch.in')


# def test_createfiles():
# 	# os.system('pip install -e .')
# 	os.system('create_files.py tests/excel_file_check.xlsx tests/lammps_script.in tests/check_results/')
# 	assert 24 == len(os.listdir('tests/check_results/all_user_files/'))

