#csv2vtpVectorField.py
#Description:  creates .vtk file from a .csv file
#              user supplies csv file with x,y,z,Vx,VyV, z columns
#Engineer:      T Looby
#Date:          20221108
import vtk
from vtk.util.numpy_support import vtk_to_numpy as vtk2np
import sys
import numpy as np

#load vtp file
csvIn = '/home/tom/source/dummyOutput/Bfield.csv'
outVTK = '/home/tom/source/dummyOutput/Bfield.vtp'

#read csv file
data = np.genfromtxt(csvIn, comments="#", delimiter=',', autostrip=True)
N = len(data)

vtkPts = vtk.vtkPoints()
cells = vtk.vtkCellArray()


vec = vtk.vtkDoubleArray()
vec.SetName("vec")
vec.SetNumberOfComponents(3)
vec.SetNumberOfTuples(N)

mag = vtk.vtkDoubleArray()
mag.SetNumberOfValues(N)
mag.SetName("mag")

v = data[:,3:]
m = np.linalg.norm(v, axis=1)

for i in range(N):
    vec.SetTuple(i, v[i])
    mag.SetValue(i, m[i])
    id = vtkPts.InsertNextPoint(data[i,0],data[i,1],data[i,2])
    cells.InsertNextCell(1)
    cells.InsertCellPoint(id)

# Add to point data array.
poly = vtk.vtkPolyData()
poly.SetPoints(vtkPts)
poly.SetVerts(cells)
poly.GetPointData().AddArray(vec)
poly.GetPointData().AddArray(mag)
poly.GetPointData().SetActiveScalars("mag")
poly.GetPointData().SetActiveVectors("vec")
poly.Modified()

# Create glyph
arrow = vtk.vtkArrowSource()
arrow.Update()
glyph = vtk.vtkGlyph3D()
glyph.SetInputData(poly)
glyph.SetSourceConnection(arrow.GetOutputPort())
glyph.SetScaleFactor(0.1)
glyph.OrientOn()
glyph.SetVectorModeToUseVector()
glyph.SetColorModeToColorByScalar()
glyph.Update()

writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(outVTK)
writer.SetInputData(glyph.GetOutput())
#writer.SetDataModeToBinary()
writer.Write()
