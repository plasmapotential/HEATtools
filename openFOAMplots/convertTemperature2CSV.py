# reads through and openfoam case dir and outputs the temperatures into 
# csv files.  each row in the csv is a new cell
import os
import csv
import numpy as np

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.TimeDirectory import TimeDirectory
from PyFoam.RunDictionary.ParsedBlockMeshDict import ParsedBlockMeshDict

# OF case directory
case_directory = '/home/tlooby/HEAT/data/sparc_000001_ILIM_NX_ellipse1mm_1782_lq0.9_S0.45_temperature/openFoam/heatFoam/T001'

#output csv directory
output_directory = case_directory + '/temperatures'

# Get all time directories
time_dirs = [d for d in os.listdir(case_directory) if d.replace('.', '', 1).isdigit()]
time_dirs.sort(key=float)  # Sorting numerically


# Total number of cells in the mesh (this needs to be set correctly)
total_cells = 458031

# Loop through each time directory
for time_dir in time_dirs:
    # Path to the temperature file for this timestep
    temp_file_path = os.path.join(case_directory, time_dir, 'T')

    # Check if the temperature file exists
    if os.path.isfile(temp_file_path):
        # Read the temperature field data
        temp_data = ParsedParameterFile(temp_file_path)
        csv_file_path = os.path.join(output_directory, f"temperature_{time_dir}.csv")

        # Check if the data is uniform or non-uniform
        if temp_data.content['internalField'].isUniform() == True:
            # Uniform data
            uniform_temp = float(str(temp_data.content['internalField']).split(' ')[1])
            data = np.ones((total_cells)) * uniform_temp   
        else:
            # Non-uniform data
            data = np.array(temp_data.content['internalField'])
            #for temp in temp_data.content['internalField']:
            #    csv_writer.writerow([temp])
        np.savetxt(csv_file_path, data)
        print("Wrote timestep: "+time_dir)

    else:
        print(f"Temperature file not found for time {time_dir}")