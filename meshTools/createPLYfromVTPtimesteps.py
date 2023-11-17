import os
import vtk

# Set the directories containing your VTP files and where to save the PLY files
vtp_directory = "/home/tom/HEAT/data/sparc_000001_filament_sbox_10_10_50_1_vr1000/paraview"
output_directory = "/home/tom/source/dummyOutput/filaments/blenderFils"

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Get the list of VTP files
vtp_files = [f for f in os.listdir(vtp_directory) if f.endswith(".vtp")]

# Function to convert a VTP file to a PLY file
def convert_vtp_to_ply(vtp_file, ply_file):
    # Read the VTP file
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(vtp_file)
    reader.Update()

    # Create a vertex filter to convert the input polydata to a point cloud
    vertex_filter = vtk.vtkVertexGlyphFilter()
    vertex_filter.SetInputConnection(reader.GetOutputPort())
    vertex_filter.Update()

    # Write the PLY file
    writer = vtk.vtkPLYWriter()
    writer.SetFileName(ply_file)
    writer.SetInputConnection(vertex_filter.GetOutputPort())
    writer.SetArrayName("Filament Trace")  # Replace "Scalars_" with the name of the scalar data array in your VTP files
    writer.SetColorModeToDefault()
    writer.Update()

# Iterate through the VTP files and convert them to PLY files
for vtp_file in vtp_files:
    input_path = os.path.join(vtp_directory, vtp_file)
    output_path = os.path.join(output_directory, os.path.splitext(vtp_file)[0] + ".ply")
    
    convert_vtp_to_ply(input_path, output_path)
    print(f"Converted {input_path} to {output_path}")