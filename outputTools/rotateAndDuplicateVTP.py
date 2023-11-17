#copies a VTP file and then patterns it for 360degrees
#using the N in the loop below.  must be run in an environment with 
#pvpython (ie in the HEAT docker container)
import paraview.simple as pvs

rootPath = '/root/HEAT/data/sparc_000001_fishScale_T4_20230822/000001/paraview/'
f = rootPath + 'HF_optical_all_mesh.vtp'
d1 = pvs.OpenDataFile(f)

transformed_datasets = []  # List to store transformed datasets

for i in range(36):
    # Create a transform filter
    transformFilter = pvs.Transform(Input=d1)
    transformFilter.Transform.Rotate = [0, 0, 10.0*(i+1)]
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
