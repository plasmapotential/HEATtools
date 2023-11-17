#calculatePlasmaWettedArea.py
#takes as input a VTP shadowMask file and a user defined vector
#the vector describes the normal vector of the PFC top surface
#calculates the area of shadowed and loaded faces whose normals
#are close to the user defined vector.  User can also provide index
#of a face and the normal can be taken to be the faces normal

import vtk
from vtk.util import numpy_support
import numpy as np

#=== INPUTS ===
#VTP shadowMask file
#f = '/home/tlooby/HEAT/data/sparc_000001_fishScale_T4_20230915_nominal/000001/paraview/shadowMask_all_mesh.vtp'
f = '/home/tlooby/HEAT/data/sparc_000001_fishScale_T4_20230915_nominal/000001/S029_0221014_B_1-Tile 4 Layout Model094/paraview/shadowMask_mesh.vtp'

outF = '/home/tlooby/source/tomTest/valid_triangles.vtp'
#maximum angle between user vector and surface normal
angDev = 10.0 #degrees
# User-defined vector
#user_vector = [x, y, z]  # [mm]
#normalized_reference_normal = user_vector / np.linalg.norm(user_vector)
# Extract the reference normal using the provided index
reference_face_index = 77285
#save a vtp file afterwards with a mesh colored to reflect
#faces included in angDev filter
VTPout = True
#==============


# Load the VTP file
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName(f)
reader.Update()

polydata = reader.GetOutput()

# Calculate normals for the mesh
normals_calculator = vtk.vtkPolyDataNormals()
normals_calculator.SetInputData(polydata)
normals_calculator.ComputeCellNormalsOn()
normals_calculator.Update()

polydata_with_normals = normals_calculator.GetOutput()

# Convert normals to numpy array
vtk_normals = polydata_with_normals.GetCellData().GetNormals()
normals_array = np.array([vtk_normals.GetTuple(i) for i in range(vtk_normals.GetNumberOfTuples())])
normalized_normals = normals_array / np.linalg.norm(normals_array, axis=1)[:, np.newaxis]


normalized_reference_normal = normalized_normals[reference_face_index]

# Compute dot products and angles for all normals in a vectorized way
dot_products = np.dot(normalized_normals, normalized_reference_normal)
angles = np.arccos(dot_products) * 180.0 / np.pi

# Get the shadowMask values from point data and convert to numpy array
shadowMask = polydata_with_normals.GetPointData().GetArray("shadowMask")
shadowMask_array = np.array([shadowMask.GetValue(i) for i in range(shadowMask.GetNumberOfTuples())])

# Extract triangle vertex indices and their corresponding shadowMasks
triangles = np.array([[polydata_with_normals.GetCell(i).GetPointIds().GetId(j) for j in range(polydata_with_normals.GetCell(i).GetNumberOfPoints())] for i in range(polydata_with_normals.GetNumberOfCells())])
triangle_masks = shadowMask_array[triangles]
triangle_mask_values = np.where(np.any(triangle_masks == 0, axis=1), 0, 1)

# Filter triangles based on angle and calculate their areas
valid_triangles = np.where(angles < angDev)[0]
area_0 = 0
area_1 = 0


print("Total faces = {:f}".format(polydata_with_normals.GetNumberOfCells()))
print("Reference Normal:")
print(normalized_reference_normal)

area_0 = 0
area_1 = 0
for i in valid_triangles:
    triangle = polydata_with_normals.GetCell(i)
    p0 = np.array(triangle.GetPoints().GetPoint(0))
    p1 = np.array(triangle.GetPoints().GetPoint(1))
    p2 = np.array(triangle.GetPoints().GetPoint(2))
    area = 0.5 * np.linalg.norm(np.cross(p1 - p0, p2 - p0))

    if triangle_mask_values[i] == 0:
        area_0 += area
    else:
        area_1 += area


print("Total area for shadowMask = 0:", area_0)
print("Total area for shadowMask = 1:", area_1)
print("Wetted fraction = {:f}".format(area_0 / (area_0 + area_1)))
print("Total area of surface = {:f}".format(area_0 + area_1))

#cone area
r0 = 1587.2
z0 = -1321.4
r1 = 1720.0
z1 = -1510.0
l = np.sqrt((r1-r0)**2 + (z1-z0)**2)
conicA = np.pi*(r0+r1)*l
dPhi = 10.0
print("Corresponding cone area = {:f}".format(conicA * dPhi / 360.0))

#now save a new VTP file colored to show us what surfaces were included
#by the angDev filter
if VTPout == True:
    print("Saving new VTP file...")
    # Initialize an array with zeros
    binary_colorscale_array = np.zeros(polydata_with_normals.GetNumberOfCells(), dtype=np.int32)

    # Set the values for valid triangles to 1
    binary_colorscale_array[valid_triangles] = 1

    # Convert numpy array to vtkIntArray
    binary_colorscale = numpy_support.numpy_to_vtk(binary_colorscale_array)
    binary_colorscale.SetName("BinaryColorScale")

    # Add the binary colorscale to the polydata
    polydata_with_normals.GetCellData().AddArray(binary_colorscale)

    # Write the modified polydata to a new VTP file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(outF)
    writer.SetInputData(polydata_with_normals)
    writer.Write()

    print("Complete.")