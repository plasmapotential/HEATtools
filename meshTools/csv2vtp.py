# csv2vtk.py
#Description:  creates .vtk file from a .csv file
#              user supplies csv file with x,y,z,Scalar columns
#Engineer:      T Looby
#Date:          20221108
import vtk
from vtk.util.numpy_support import vtk_to_numpy as vtk2np
import sys
import numpy as np

#load vtk file
csvIn = '/home/tom/source/dummyOutput/HF_optical_all.csv'
outVTK = '/home/tom/source/dummyOutput/test.vtk'

#read csv file
data = np.genfromtxt(csvIn, comments="#", delimiter=',', autostrip=True)
N = len(data)

vtkPts = vtk.vtkPoints()
cells = vtk.vtkCellArray()

# setup colors
Colors = vtk.vtkFloatArray()
#Colors.SetNumberOfComponents(3)
Colors.SetNumberOfTuples(N)
Colors.SetName('$MW/m^2$') #can change to any string

for i in range(N):
    id = vtkPts.InsertNextPoint(data[i,0],data[i,1],data[i,2])
    cells.InsertNextCell(1)
    cells.InsertCellPoint(id)
    Colors.InsertTuple( i, [data[i,3]] )

#    cells.InsertNextCell()
#    cells.InsertCellPoint(ptId)


polydata = vtk.vtkPolyData()
polydata.SetPoints(vtkPts)
polydata.SetVerts(cells)
polydata.GetPointData().SetScalars(Colors)
polydata.Modified()

writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(outVTK)
writer.SetInputData(polydata)
#writer.SetDataModeToBinary()
writer.Write()
