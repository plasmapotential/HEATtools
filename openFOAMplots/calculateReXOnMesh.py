import os


from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.TimeDirectory import TimeDirectory
from PyFoam.RunDictionary.ParsedBlockMeshDict import ParsedBlockMeshDict

# Set the path to your case directory
case_directory = '/home/tlooby/HEAT/data/sparc_000001_ILIM_NX_ellipse1mm_1782_lq0.9_S0.45_temperature/openFoam/heatFoam/T001'

# Get all time directories
time_dirs = [d for d in os.listdir(case_directory) if d.replace('.', '', 1).isdigit()]
time_dirs.sort(key=float)  # Sorting numerically


# Loop through each time directory
for time_dir in time_dirs:
    print(time_dir)
    # Path to the temperature file for this timestep
    temp_file_path = os.path.join(case_directory, time_dir, 'T')

    # Check if the temperature file exists
    if os.path.isfile(temp_file_path):
        # Read the temperature field data
        temp_data = ParsedParameterFile(temp_file_path)

        #calculation on internalField
        if 'internalField' in temp_data.content:
            if temp_data.content['internalField'].isUniform() == True:
                print("uniform")
            else:
                print(f"Time: {time_dir}, Average Temperature: {sum(temp_data.content['internalField']) / len(temp_data.content['internalField'])}")
        else:
            print(f"Time: {time_dir}, Temperature data not found in internalField")
    else:
        print(f"Temperature file not found for time {time_dir}")