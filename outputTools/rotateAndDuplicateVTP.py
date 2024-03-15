#copies a VTP file and then patterns it for 360degrees
#using the N in the loop below.  must be run in an environment with 
#pvpython (ie in the HEAT docker container), or call the pvpython <filename>.py
#from terminal
#example path to pvpython:
#/home/tlooby/opt/paraview/ParaView-5.11.0-RC1-MPI-Linux-Python3.9-x86_64/bin/pvpython

import paraview.simple as pvs

rootPath = '/home/tlooby/HEAT/data/sparc_000001_innerDivertorTest/0.010000000/paraview/'
f = rootPath + 'HF_optical_all_mesh.vtp'
print("Reading file")
d1 = pvs.OpenDataFile(f)
print("Done reading")

transformed_datasets = []  # List to store transformed datasets

N = 9
offset = -172.5
for i in range(N):
    # Create a transform filter
    transformFilter = pvs.Transform(Input=d1)
    transformFilter.Transform.Rotate = [0, 0, 10.0*(i+1) + offset]
    # Update the filter to apply the transformation
    pvs.UpdatePipeline(proxy=transformFilter)
    # Append the transformed data for later combination
    transformed_datasets.append(transformFilter)

# Group all the transformed datasets using GroupDatasets
grouped_data = pvs.GroupDatasets(*transformed_datasets)  # Unpack the list of datasets

# Merge the grouped data blocks into a single block
merged_data = pvs.MergeBlocks(grouped_data)

# Extract the surface to get vtkPolyData
extracted_surface = pvs.ExtractSurface(Input=merged_data)

# Save the combined VTP file
combined_file_path = rootPath + 'combined_data.vtp'
pvs.SaveData(combined_file_path, extracted_surface)
