#createRZsketch.py
#Description:   makes FreeCAD sketch from RZ limiter csv file
#Date:          20221219
#engineer:      T Looby
import os, sys
import numpy as np
from pathlib import Path
#FreeCADPath = '/usr/lib/freecad-daily/lib'
FreeCADPath = '/usr/lib/freecad-python3/lib'
sys.path.append(FreeCADPath)
import FreeCAD
import Sketcher

#RZ contour file to use for sketch
name = 'v3c'
path = '/home/tlooby/SPARC/RZcontours/'
rzFile = path+name+'.csv'
#freecad file to save
outFile = path + name +'.FCStd'

#create sketch
doc = FreeCAD.newDocument()
rzSketch = doc.addObject('Sketcher::SketchObject',name)
rzSketch.Placement = App.Placement(App.Vector(0.000000, 0.000000, 0.000000), App.Rotation(0.707107, 0.000000, 0.000000, 0.707107))
rzSketch.MapMode = "Deactivated"

#read RZ coordinates from file
rzPts = np.genfromtxt(rzFile, comments='#', delimiter=',')
xyz = np.zeros((len(rzPts),3))
xyz[:,0] = rzPts[:,0]*1000.0
xyz[:,1] = rzPts[:,1]*1000.0 #FreeCAD has a coordinate permutation bug, depending upon sketch axes

#define rz coordinates manually
#T4
#xyz = np.array(([[1587.2, -1321.4, 0.0],
#                 [1720, -1510.0, 0.0]]))
#T6
xyz = np.array(([[1658.5, -1217.7, 0.0],
                 [1695.0, -1380.0, 0.0]]))
outFile = path + name +'v3c_T6.FCStd'

#create sketch from RZ points
for i in range(len(xyz)-1):
    if i==0:
        rzSketch.addGeometry(Part.LineSegment(FreeCAD.Vector(xyz[i]),FreeCAD.Vector(xyz[i+1])),False)
        #rzSketch.addGeometry(Part.LineSegment(FreeCAD.Vector(10.0,10.0),FreeCAD.Vector(20.0,20.0)),False)
    else:
        rzSketch.addGeometry(Part.LineSegment(FreeCAD.Vector(xyz[i]),FreeCAD.Vector(xyz[i+1])),False)
        rzSketch.addConstraint(Sketcher.Constraint('Coincident',i-1,2,i,1))

doc.recompute()

#save file
Path(path).mkdir(parents=True, exist_ok=True)
doc.saveAs(outFile)
FreeCAD.closeDocument(doc.Name)
print("Complete...")
