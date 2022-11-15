#!/usr/bin/env python
#creates VTP from points and triangles.  From kitware pythone examples page
#  https://kitware.github.io/vtk-examples/site/Python/PolyData/ColoredTriangle/

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints,vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray,vtkPolyData,vtkTriangle
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter


def get_program_parameters():
    import argparse
    description = 'Generate a colored triangle, then write a .vtp file.'
    epilogue = '''
   '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue)
    parser.add_argument('filename', help='A required vtp filename.', nargs='?',
                        const='TestColoredTriangle.vtp',
                        type=str, default='/home/tom/source/dummyOutput/TestColoredTriangle.vtp')
    args = parser.parse_args()
    return args.filename


def main():
    colors = vtkNamedColors()

    filename = get_program_parameters()

    # setup points and vertices
    Points = vtkPoints()
    Points.InsertNextPoint(1.0, 0.0, 0.0)
    Points.InsertNextPoint(0.0, 0.0, 0.0)
    Points.InsertNextPoint(0.0, 1.0, 0.0)
    Points.InsertNextPoint(0.0, 0.0, 0.0)
    Points.InsertNextPoint(0.0, 1.0, 0.0)
    Points.InsertNextPoint(0.0, 0.0, 1.0)


    Triangles = vtkCellArray()
    Triangle = vtkTriangle()
    Triangle.GetPointIds().SetId(0, 0)
    Triangle.GetPointIds().SetId(1, 1)
    Triangle.GetPointIds().SetId(2, 2)
    Triangles.InsertNextCell(Triangle)
    Triangle = vtkTriangle()
    Triangle.GetPointIds().SetId(0, 3) #1st number is triangle vertex, 2nd number is location in points
    Triangle.GetPointIds().SetId(1, 4)
    Triangle.GetPointIds().SetId(2, 5)
    Triangles.InsertNextCell(Triangle)

    # setup colors
    Colors = vtkUnsignedCharArray()
    Colors.SetNumberOfComponents(3)
    Colors.SetNumberOfTuples(Triangles.GetNumberOfCells())
    Colors.SetName('Colors')
    c = (60,150,200)
    Colors.InsertTuple(0,c)
    Colors.InsertTuple(1,c)
    Colors.InsertTuple(2,c)
    Colors.InsertTuple(3,c)
    Colors.InsertTuple(4,c)
    Colors.InsertTuple(5,c)


    polydata = vtkPolyData()
    polydata.SetPoints(Points)
    polydata.SetPolys(Triangles)

    polydata.GetPointData().SetScalars(Colors)
    polydata.Modified()

    writer = vtkXMLPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(polydata)
    writer.Write()


if __name__ == '__main__':
    main()
