# stlvtk2vtp.py
#Description:  creates .vtp file from a .vtk file and a .stl file
#              user needs to supply an STL file and a VTK file with scalars
#              that are indexed to match the STL mesh.  Outputs a triangular mesh
#              that is colored to match the scalar value
#Engineer:      T Looby
#Date:          20221108
import vtk
from vtk.util.numpy_support import vtk_to_numpy as vtk2np
import sys
import numpy as np

#load HEAT environment
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(HEATPath)
import launchHEAT
launchHEAT.loadEnviron()
import CADClass

#load mesh file
f = '/home/tom/HEAT/data/NSTX/STLs/SOLID843___5.00mm.stl'
CAD = CADClass.CAD()
mesh = CAD.load1Mesh(f)
norms,ctrs,areas = CAD.normsCentersAreas(mesh)

#load vtk file
vtkF = '/home/tom/source/dummyOutput/HF_optical_all.vtk'
outVTP = '/home/tom/source/dummyOutput/test.vtp'
reader = vtk.vtkPolyDataReader()
reader.SetFileName(vtkF)
reader.Update()
scalarData = reader.GetOutput()

# Extract the points from the point cloud
points = vtk2np(scalarData.GetPoints().GetData())
arr = vtk2np(scalarData.GetPointData().GetArray("Scalar"))
N = scalarData.GetPointData().GetArray("Scalar").GetNumberOfValues()
vtkPts = vtk.vtkPoints()

# setup colors
Colors = vtk.vtkUnsignedCharArray()
#Colors.SetNumberOfComponents(3)
Colors.SetNumberOfTuples(N)
Colors.SetName('Scalar') #can change to any string

#build points and colors
for i,facet in enumerate(mesh.Facets):
    for j in range(3):
        x = facet.Points[j][0]
        y = facet.Points[j][1]
        z = facet.Points[j][2]
        vtkPts.InsertNextPoint(x,y,z)
#        Colors.InsertTuple( i*3+j, (arr[i],arr[i],arr[i]) )
        Colors.InsertTuple( i*3+j, [arr[i]] )

#build vtp triangular mesh
Triangles = vtk.vtkCellArray()
for i in range(N):
    Triangle = vtk.vtkTriangle()
    Triangle.GetPointIds().SetId(0, i*3+0)
    Triangle.GetPointIds().SetId(1, i*3+1)
    Triangle.GetPointIds().SetId(2, i*3+2)
    Triangles.InsertNextCell(Triangle)

#build final vtp object for writing
polydata = vtk.vtkPolyData()
polydata.SetPoints(vtkPts)
polydata.SetPolys(Triangles)
polydata.GetPointData().SetScalars(Colors)
polydata.Modified()
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(outVTP)
writer.SetInputData(polydata)
#writer.SetDataModeToBinary()
writer.Write()
