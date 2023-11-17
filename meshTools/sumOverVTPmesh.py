import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np

#meshFile = '/home/tlooby/HEAT/data/sparc_000001_portPlug_Plane_180deg_OMP_v2/000001/paraview/HF_rad_all_mesh.vtp'
#meshFile = '/home/tlooby/HEAT/data/sparc_000001_portPlug_Plane_180deg_OMP_v2/000001/T033/paraview/HF_rad_mesh.vtp'
meshFile = '/home/tlooby/HEAT/data/sparc_000001_portPlug_Plane_180deg_Uniform_shifted110mm/000001/paraview/HF_rad_all_mesh.vtp'
#meshFile = '/home/tlooby/Downloads/HF_rad_all_mesh.vtp'


def compute_triangle_area(v1, v2, v3):
    """Compute the area of a triangle from its vertices using Heron's formula."""
    a = np.linalg.norm(v1 - v2)
    b = np.linalg.norm(v2 - v3)
    c = np.linalg.norm(v3 - v1)
    s = (a + b + c) / 2
    return np.sqrt(s * (s - a) * (s - b) * (s - c))


def compute_triangle_area2(v1, v2, v3):
    """Compute the area of a triangle from its vertices using Heron's formula."""
    A = v2-v1
    B = v3-v1
    area = np.linalg.norm(np.cross(A,B)) / 2.0
    return area

# Create a reader for your VTP file
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName(meshFile)  # replace with your file name
reader.Update()

# Get the mesh data
mesh = reader.GetOutput()

# Get the point data
points = vtk_to_numpy(mesh.GetPoints().GetData())

# Get the color data
colors = vtk_to_numpy(mesh.GetPointData().GetScalars())

# Check the data integrity
assert len(colors) == len(points)

# Calculate the total deposited energy
total_power = 0.0

# Get polygons (triangular faces)
polygons = mesh.GetPolys().GetData()
polygons = vtk_to_numpy(polygons).reshape(-1, 4)[:, 1:]

flux = []
# Loop over each polygon
for polygon in polygons:
    vertices = points[polygon] * 1e-3
    # Area of the triangle
    area = compute_triangle_area2(*vertices)
    # Mean color value of the vertices (assuming linear color mapping)
    color = colors[polygon].mean()
    flux.append(colors[polygon].mean())
    # Accumulate the energy
    total_power += area * color

print(max(flux))

print(f'The total deposited power is: {total_power} [MW]')
Etot = total_power*10.4*10.0
print("Time integrated energy: {:f} [MJ]".format(Etot))