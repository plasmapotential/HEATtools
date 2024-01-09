#paraview macro that loads ReX data from calculateReXOnMesh.py and
#assigns it to a .foam mesh
#
#csv file is ReX data.  .foam file is openfoam data (with polymesh)
import csv
import paraview.simple as pvs

case_directory = '/home/tlooby/HEAT/data/sparc_000001_ILIM_NX_ellipse1mm_1782_lq0.9_S0.45_temperature/openFoam/heatFoam/T001'

# Load your mesh data
foam_data = pvs.FindSource(case_directory + '/T001.foam')

# Path to your CSV file
csv_file_path = case_directory + '/integral_0.023.csv'

# Read CSV data
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    scalar_data = [float(row[0]) for row in reader]

# Create a new point data array
from vtk.numpy_interface import dataset_adapter as dsa
vtk_mesh = dsa.WrapDataObject(foam_data)
vtk_mesh.CellData.append(scalar_data, 'ReX')

# Update the view
pvs.GetActiveView().Update()
