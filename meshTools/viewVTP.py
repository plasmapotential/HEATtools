#example render window.  probably will need to adjust.  can also
#import vtp files directly into paraview
import sys
import numpy
import vtkmodules.all as vtk
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

#f = '/home/tom/source/dummyOutput/TestColoredTriangle.vtp'
f = '/home/tom/source/dummyOutput/test.vtp'
ascotVTP = '/home/tom/work/CFS/projects/ASCOT/ascot_59382525_59382525.vtp'
binary=True

reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName(f)
reader.Update()

# Visualize
colors = vtkNamedColors()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)
#actor.GetProperty().SetColor(colors.GetColor3d('NavajoWhite'))
renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor)
renderer.SetBackground(colors.GetColor3d('DarkOliveGreen'))
renderer.GetActiveCamera().Pitch(90)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
#crashing
#renderer.ResetCamera()
renderWindow.SetSize(600, 600)
renderWindow.Render()
renderWindow.SetWindowName('ReadPolyData')
renderWindowInteractor.Start()
