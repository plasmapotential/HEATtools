#converts an elmer .vtu output file to an xyz csv.  
#also copies a field from the elmer file (ie temperature)
import vtk
from vtk.util.numpy_support import vtk_to_numpy

# Path to the VTU file
vtu_file_path = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stress/IDEA_run/sweepMEQ_elmer/case_t0142.vtu'

# Create a reader for the VTU file
reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(vtu_file_path)
reader.Update()

# Get the 'vtkUnstructuredGrid' object from the reader
unstructuredGrid = reader.GetOutput()

# Extract node coordinates
points = unstructuredGrid.GetPoints()
coordinates = vtk_to_numpy(points.GetData())

# Extract temperature data
temperatureArray = unstructuredGrid.GetPointData().GetArray("temperature")  # Assuming the temperature field is named 'T'
temperatures = vtk_to_numpy(temperatureArray)

# Check if coordinates and temperatures have the same length
assert len(coordinates) == len(temperatures), "Mismatch in length of coordinates and temperature data"

# Output X, Y, Z, T data
output_file_path = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stress/IDEA_run/sweepMEQ_elmer/Elmer_Temperature_715ms.csv'
with open(output_file_path, 'w') as file:
    file.write("X,Y,Z,T[degC]\n")  # Header
    for coord, temp in zip(coordinates, temperatures):
        file.write(f"{coord[0]},{coord[1]},{coord[2]},{temp}\n")

print(f"Data extracted to {output_file_path}")
