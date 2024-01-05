import os
import csv
import numpy as np

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.TimeDirectory import TimeDirectory
from PyFoam.RunDictionary.ParsedBlockMeshDict import ParsedBlockMeshDict

# Constants (replace with actual values)
E = 3.0  # Activation energy in [eV/atom]
kB = 8.617333e-5 #eV/K
k0 = 1553034867.0328593 #Avrami coefficient
n = 2.0 #Avrami exponent
T_ref = 1473 #[K] reference temperature
# Total number of cells in the mesh (this needs to be set correctly)
total_cells = 458031


# OF case directory
case_directory = '/home/tlooby/HEAT/data/sparc_000001_ILIM_NX_ellipse1mm_1782_lq0.9_S0.45_temperature/openFoam/heatFoam/T001'

#output csv directory
output_directory = case_directory + '/temperatures'

# Get all time directories
time_dirs = [d for d in os.listdir(case_directory) if d.replace('.', '', 1).isdigit()]
time_dirs.sort(key=float)  # Sorting numerically

integralData = np.zeros((total_cells))
ReXData = np.zeros((total_cells))

# Previous timestep temperature for trapezoidal integration
prev_temp = None


c1 = np.exp(-E / (kB*T_ref))
c2 = np.exp(E / (kB*T_ref))


def calculateTrapz(Tprev, Tnew, dt):
    return dt * (np.exp(-E / (kB * Tprev)) + np.exp(-E / (kB * Tnew))) / 2

# Loop through each time directory
for i,time_dir in enumerate(time_dirs):
    # Path to the temperature file for this timestep
    temp_file_path = os.path.join(case_directory, time_dir, 'T')

    # Check if the temperature file exists
    if os.path.isfile(temp_file_path):
        # Read the temperature field data
        temp_data = ParsedParameterFile(temp_file_path)
        csv_file_path = os.path.join(output_directory, f"integral_{time_dir}.csv")

        # Determine current temperature data
        if temp_data.content['internalField'].isUniform() == True:
            current_temp = float(str(temp_data.content['internalField']).split(' ')[1])
            current_temp = np.ones(total_cells) * current_temp
        else:
            current_temp = np.array(temp_data.content['internalField'])

        # Calculate timestep (assuming uniform timestep)
        # Adjust this if you have variable timesteps
        if i > 0:
            delta_t = float(time_dirs[i]) - float(time_dirs[i - 1])

            # Trapezoidal integration
            if prev_temp is not None:
                c3 = calculateTrapz(prev_temp, current_temp, delta_t)
                ReXData += 1 - np.exp(-k0*c1 * (c2 * c3)**n )
                

        prev_temp = current_temp
        np.savetxt(csv_file_path, ReXData)

        print("Wrote timestep: "+time_dir)

    else:
        print(f"Temperature file not found for time {time_dir}")