#opens an openFOAM thermal analysis directory, takes the T and calculates the
#recrystallization fraction [K], then saves result on the mesh to a 
#new openfoam field, ReX, for each mesh element

import os
import csv
import numpy as np

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.TimeDirectory import TimeDirectory
from PyFoam.RunDictionary.ParsedBlockMeshDict import ParsedBlockMeshDict

# Constants (replace with actual values)
#E = 3.0  # Activation energy in [eV/atom]
#k0 = 1553034867.0328593 #Avrami coefficient
#n = 2.0 #Avrami exponent

k0 = 4446601449.779298
E = 3.0
n = 1.0

kB = 8.617333e-5 #eV/K
T_ref = 1200 + 273.15 #[K] reference temperature
# Total number of cells in the mesh (this needs to be set correctly)
total_cells = 69801


# OF case directory
case_directory = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_20231206_nominal_fRadDiv70_lq0.6_S0.6/openFoam/heatFoam/T032'

#output csv directory
output_directory = case_directory + '/ReX'

# Get all time directories
time_dirs = [d for d in os.listdir(case_directory) if d.replace('.', '', 1).isdigit()]
time_dirs.sort(key=float)  # Sorting numerically

integralData = np.zeros((total_cells))
ReXData = np.zeros((total_cells))
ReXDataPeak = 0

# Previous timestep temperature for trapezoidal integration
prev_temp = None
prev_temp_max = None


c1 = np.exp(-E / (kB*T_ref))
c2 = np.exp(E / (kB*T_ref))


def calculateTrapz(Tprev, Tnew, dt):
    return dt * ( np.exp(-E / (kB * Tprev)) + np.exp(-E / (kB * Tnew)) ) / 2.0

# Function to write the OpenFOAM field file
def write_field_file(time_dir, data, case_directory, field_name):
    field_file_path = os.path.join(case_directory, time_dir, field_name)
    with open(field_file_path, 'w') as file:
        file.write('/*--------------------------------*- C++ -*----------------------------------*\\\n')
        file.write('| =========                 |                                                 |\n')
        file.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n')
        file.write('|  \\    /   O peration     | Version:  2112                                  |\n')
        file.write('|   \\  /    A nd           | Website:  www.openfoam.com                      |\n')
        file.write('|    \\/     M anipulation  |                                                 |\n')
        file.write('\*---------------------------------------------------------------------------*/\n')
        file.write("FoamFile\n")
        file.write("{\n")
        file.write("    version     2.0;\n")
        file.write("    format      ascii;\n")
        file.write("    arch        \"LSB;label=32;scalar=64\";\n")
        file.write("    class       volScalarField;\n")
        file.write("    location    "+time_dir+";\n")
        file.write("    object      \""+field_name+"\";\n")
        file.write("}\n")
        file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n\n")
        file.write("dimensions      [0 0 0 1 0 0 0];\n\n")
        file.write("internalField   nonuniform List<scalar>\n")
        file.write(f"{len(data)}\n(\n")
        for value in data:
            file.write(f"{value}\n")
        file.write(")\n;\n")
        file.write("boundaryField\n{\n    type calculated;\n}\n")
        file.write("    }\n")
        file.write("}\n\n\n")
        file.write("// ************************************************************************* //\n")

Tdata = []
# Loop through each time directory
for i,time_dir in enumerate(time_dirs):
    # Path to the temperature file for this timestep
    temp_file_path = os.path.join(case_directory, time_dir, 'T')

    # Check if the temperature file exists
    if os.path.isfile(temp_file_path):
        # Read the temperature field data
        temp_data = ParsedParameterFile(temp_file_path)
        #csv_file_path = os.path.join(output_directory, f"integral_{time_dir}.csv")

        # Determine current temperature data
        if temp_data.content['internalField'].isUniform() == True:
            current_temp = float(str(temp_data.content['internalField']).split(' ')[1])
            current_temp = np.ones(total_cells) * current_temp
        else:
            current_temp = np.array(temp_data.content['internalField'])

        current_temp_max = np.max(current_temp)
        Tdata.append(current_temp_max)

        # Calculate timestep (assuming uniform timestep)
        # Adjust this if you have variable timesteps
        if i > 0:
            delta_t = float(time_dirs[i]) - float(time_dirs[i - 1])
            dt_hrs = delta_t / 3600.0

            # Trapezoidal integration
            if prev_temp is not None:
                c3 = calculateTrapz(prev_temp, current_temp, dt_hrs)
                ReXData += 1 - np.exp(-k0*c1 * (c2 * c3)**n )
                c3Peak = calculateTrapz(prev_temp_max, current_temp_max, dt_hrs)
                ReXDataPeak += 1 - np.exp(-k0*c1 * (c2 * c3Peak)**n )
                

        prev_temp = current_temp
        prev_temp_max = current_temp_max

        #write a csv file
        #np.savetxt(csv_file_path, ReXData)

        # Write the field file for this timestep
        field_name = "ReX"
        write_field_file(time_dir, ReXData, case_directory, field_name)


        print("Wrote timestep: "+time_dir+"   Max Mesh ReX: {:f}   ReX Peak: {:f}".format(max(ReXData), ReXDataPeak))

    else:
        print(f"Temperature file not found for time {time_dir}")

    np.savetxt(case_directory + '/TpeakCell_fromReXcalc.csv', np.array(Tdata), delimiter=',')