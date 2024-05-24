import numpy as np
import os
import pandas as pd
import sys

def copy_data_file(source_data_file, dest_data_file):
	if sys.platform == 'win32':
		os.system('copy '+ source_data_file+' '+dest_data_file)
	else:
		os.system('cp '+ source_data_file+' '+dest_data_file)