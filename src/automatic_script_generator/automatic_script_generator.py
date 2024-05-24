"""
This module defines relevant functions for the package:

excel_to_script() - Creates the required script by
parsing the excel sheet and replacing appropriate
keywords in the base script.

all_files_generator() - Analyzes the excel sheet
for variables containing multiple values and
creates a meshgrid to loop over. Calls
excel_to_script() function to generate the
individual scripts.
"""

# pylint: disable=consider-using-enumerate,too-many-locals,broad-except,unidiomatic-typecheck,consider-using-with,unused-variable,too-many-branches,too-many-statements

import os
from datetime import datetime
import numpy as np
import pandas as pd


# flake8: noqa W191, E101, F841, E501


def all_files_generator(path_excel_file, base_script_path, results_dir):

    """
	Input: Path to the excel file, path to base script, results directory

	Output: Creates an 'all-user-files' directory which contains
	the sub-directories (<base_script_name>_*) with the following:
		- Base script for a parameter combination (.in file).
		- Excel file corresponding to the base file
	"""

    slash_use = "/"

    try:
        os.mkdir(results_dir + slash_use + "all_user_files")
    except Exception as script_error:
        old_datetime = str(datetime.now()).replace(" ", "_").replace(":", "--")
        os.rename(
            results_dir + slash_use + "all_user_files",
            results_dir + slash_use + "all_user_files_old_" + old_datetime,
        )
        os.mkdir(results_dir + slash_use + "all_user_files")

    # Reads the excel configuration file
    values_file = pd.read_excel(path_excel_file)
    property_names = values_file[values_file.columns[0]]
    property_vals = values_file[values_file.columns[1]]

    # Extract base script name from path
    base_script_name = base_script_path.split(slash_use)[-1]
    base_script_name, base_script_ext = (
        base_script_name.split(".")[0],
        base_script_name.split(".")[-1],
    )

    property_lengths = np.ones(len(property_names), dtype=int)

    # Check for length
    for i in range(len(property_vals)):
        temp_property_val = property_vals[i]

        if type(temp_property_val) == str:
            try:
                a_var = [
                    float(y_var)
                    for y_var in [
                        x_var.replace(" ", "") for x_var in temp_property_val.split(",")
                    ]
                ]
            except Exception as script_error:
                a_var = [
                    x_var.replace(" ", "") for x_var in temp_property_val.split(",")
                ]
            property_lengths[i] = len(a_var)

        if type(temp_property_val) == list:
            a_var = [
                float(y_var)
                for y_var in [
                    x_var.replace(" ", "") for x_var in temp_property_val.split(",")
                ]
            ]
            property_lengths[i] = len(a_var)

        if (type(temp_property_val) == float) | (type(temp_property_val) == int):
            a_var = temp_property_val
            property_lengths[i] = 1

    # Extract values for which length > 1
    loop_names = property_names[property_lengths > 1].values

    # Check for length > 1 parameters.
    # If only single run is to be executed generate excel file directly.
    if len(loop_names) > 0:
        print(
            "Generating " + str(np.prod(property_lengths)) + " folders. Looping over: ",
            loop_names,
        )
        parameter_loop_vals = []
        for i in range(len(loop_names)):
            temp_property_val = property_vals[
                property_names.values == loop_names[i]
            ].values[0]

            try:
                a_var = [
                    float(y_var)
                    for y_var in [
                        x_var.replace(" ", "") for x_var in temp_property_val.split(",")
                    ]
                ]
            except Exception as script_error:
                a_var = [
                    x_var.replace(" ", "") for x_var in temp_property_val.split(",")
                ]
            parameter_loop_vals.append(a_var)

        # Create mesh grid to loop over
        counter_vals = [
            list(range(property_lengths[property_names == i][0])) for i in loop_names
        ]
        counter_loops = np.meshgrid(*counter_vals)
        counter_list = []
        for index, x_var in np.ndenumerate(counter_loops[0]):
            # counter_list[i][j] corresponds to loop_name[i] and parameter_loop_vals[i][j]
            counter_list.append(
                [counter_loops[i][index] for i in range(np.shape(counter_loops)[0])]
            )

        # We have built the meshgrid array which stores positions of
        # all the variable values array.
        # Now looping over each of the values in the meshgrid to
        # create respective scripts.
        for i in range(len(counter_list)):
            curr_counter_list = counter_list[i]
            new_dir_name = (
                results_dir
                + slash_use
                + "all_user_files"
                + slash_use
                + base_script_name
                + "_"
                + str(i)
            )
            new_excel_file = (
                new_dir_name + slash_use + base_script_name + "_" + str(i) + ".xlsx"
            )
            new_script_name = (
                new_dir_name
                + slash_use
                + base_script_name
                + "_"
                + str(i)
                + "."
                + base_script_ext
            )
            os.mkdir(new_dir_name)

            values_file_new = values_file.copy()
            property_names_new = values_file_new[values_file_new.columns[0]]
            property_vals_new = values_file_new[values_file_new.columns[1]]

            for j, jval in enumerate(curr_counter_list):
                property_vals_new[
                    property_names_new.values == loop_names[j]
                ] = parameter_loop_vals[j][jval]

            values_file_new.to_excel(new_excel_file, index=False)
            # print(values_file_new)
            excel_to_script(new_excel_file, base_script_path, new_script_name)

    else:
        values_file_new = values_file.copy()
        property_names_new = values_file_new[values_file_new.columns[0]]
        property_vals_new = values_file_new[values_file_new.columns[1]]

        new_dir_name = (
            results_dir
            + slash_use
            + "all_user_files"
            + slash_use
            + base_script_name
            + "_0"
        )
        new_excel_file = new_dir_name + slash_use + base_script_name + "_0.xlsx"
        new_script_name = (
            new_dir_name
            + slash_use
            + base_script_name
            + "_"
            + "0"
            + "."
            + base_script_ext
        )
        try:
            os.mkdir(new_dir_name)
        except Exception as script_error:
            pass
        values_file_new.to_excel(new_excel_file, index=False)
        excel_to_script(new_excel_file, base_script_path, new_script_name)


def excel_to_script(path_excel_file, base_script_path, save_gen_script):
    """
	Input: Path to excel sheet, path to base script, new script to save code in
	Output: High-throughput scripts created in the results directory

	"""

    values_file_new = pd.read_excel(path_excel_file)
    property_names_new = values_file_new[values_file_new.columns[0]]
    property_vals_new = values_file_new[values_file_new.columns[1]]

    # Initialize the base script
    base_script = open(base_script_path, "r")
    temp_content = base_script.read()
    base_script.close()

    # Replace temporary variables with actual values
    for i in range(len(property_names_new)):
        temp_name = property_names_new[i] + "_valpy"
        temp_content = temp_content.replace(temp_name, str(property_vals_new[i]))

    # Save to the original file
    save_script = open(save_gen_script, "wt")
    save_script.write(temp_content)
    save_script.close()
