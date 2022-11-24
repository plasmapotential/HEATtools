#vtp2csv.py
#Description:  creates .csv file from a .vtp mesh file
#              user supplies vtp file with scalar defined on mesh points
#              algorithm returns mesh centers with scalar in (x,y,z,scalar) csv
#Engineer:      T Looby
#Date:          20221115
import vtk
from vtk.util import numpy_support
import sys
import numpy as np

#outfile
csvOut = '/home/tom/source/dummyOutput/vtpConverted.csv'
#vtp file we want to cut
VTPin = '/home/tom/work/CFS/projects/ASCOT/ascot_59382525_59382525.vtp'

#definition of filter bounding box
boxFilter = True #filter only points inside box defined below
xMin = -0.01
xMax = 0.2
yMin = -2.460
yMax = 2.42
zMin = -0.00612
zMax = 0.0061

#read vtp data
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName(VTPin)
reader.Update()
polyData1 = reader.GetOutput()
coordObj = polyData1.GetPoints().GetData()
coords = numpy_support.vtk_to_numpy(coordObj)

#here array 1 corresponds to "wall load", which was checked via inspection
scalarData = polyData1.GetCellData().GetArray(1)

#calculate cell centers
ctrsFilter = vtk.vtkCellCenters()
ctrsFilter.SetInputData(polyData1)
ctrsFilter.Update()
ctrs = []
scalars = []
#slow loop but whatever...
for i in range(ctrsFilter.GetOutput().GetNumberOfPoints()):
    ctrs.append(list(ctrsFilter.GetOutput().GetPoint(i)))
    scalars.append(scalarData.GetTuple(i)[0])

ctrNp = np.array(ctrs)
scalarNp = np.array(scalars)

#box filter if switch is on
if boxFilter == True:
    testX = np.logical_and(ctrNp[:,0] > xMin, ctrNp[:,0] < xMax)
    testY = np.logical_and(ctrNp[:,1] > yMin, ctrNp[:,1] < yMax)
    testZ = np.logical_and(ctrNp[:,2] > zMin, ctrNp[:,2] < zMax)
    test = np.logical_and(np.logical_and(testX,testY), testZ)
    use = np.where(test==True)[0]
else:
    use = np.arange(len(ctrs))

arr = np.vstack([1000*ctrNp[use].T, scalarNp[use]]).T
#write data out to CSV file
header = "X,Y,Z,$MW/m^2$"
np.savetxt(csvOut, arr, delimiter=',',fmt='%.10f', header=header)
