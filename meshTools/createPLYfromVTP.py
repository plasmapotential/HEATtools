import vtk

f = '/home/tlooby/HEAT/data/sparc_000001_fishScale_T5B_178_602_1579/000001/paraview/HF_optical_all_mesh.vtp'
outF = '/home/tlooby/HEAT/data/sparc_000001_fishScale_T5B_178_602_1579/000001/paraview/HF_optical_all_mesh.ply'

def create_color_transfer_function(scalars):
    # Create a color transfer function
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToRGB()

    # Configure the black-body radiation color scale
    ctf.AddRGBPoint(scalars.GetRange()[0], 0.0, 0.0, 0.0)
    ctf.AddRGBPoint(scalars.GetRange()[1], 1.0, 1.0, 1.0)

    return ctf

# Read VTP file
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName(f)
reader.Update()

# Get scalar data
scalars = reader.GetOutput().GetPointData().GetScalars()

# Create a color transfer function for the scalar data
ctf = create_color_transfer_function(scalars)

# Convert scalar data to RGB colors
colors = vtk.vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)
colors.SetNumberOfTuples(scalars.GetNumberOfTuples())
colors.SetName("Colors")

for i in range(scalars.GetNumberOfTuples()):
    color = [0, 0, 0]
    ctf.GetColor(scalars.GetValue(i), color)
    colors.SetTuple3(i, int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

# Set RGB colors to polydata
polydata = reader.GetOutput()
polydata.GetPointData().SetScalars(colors)
polydata.Modified()

# Write PLY file
writer = vtk.vtkPLYWriter()
writer.SetInputData(polydata)
writer.SetFileName(outF)
writer.SetArrayName("Colors")
writer.SetFileTypeToBinary()
writer.Write()