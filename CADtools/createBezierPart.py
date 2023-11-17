#creates a component with a bezier top surface
#meant to be copied and pasted into FreeCAD python console

#edits bezier control points below as necessary
points = [FreeCAD.Vector(-26.0, 0.0, 0.0), 
          FreeCAD.Vector(-26.0, 6.0, 0.0), 
          FreeCAD.Vector(-20.0, 6.0, 0.0), 
          FreeCAD.Vector( 0.0,  6.0, 0.0), 
          FreeCAD.Vector( 20.0, 6.0, 0.0), 
          FreeCAD.Vector( 26.0, 6.0, 0.0), 
          FreeCAD.Vector( 26.0, 0.0, 0.0)]


bez = Draft.make_bezcurve(points, closed=False, support=None, degree=None)


#line (edit points)
pl = FreeCAD.Placement()
pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
pl.Base = FreeCAD.Vector(-26.0, 0.0, 0.0)
linePoints = [FreeCAD.Vector(-26.0, 0.0, 0.0), FreeCAD.Vector(26.0, 0.0, 0.0)]
line = Draft.make_wire(linePoints, placement=pl, closed=False, face=True, support=None)
Draft.autogroup(line)
FreeCAD.ActiveDocument.recompute()


#add to sketch
sk = Draft.make_sketch([bez, line], autoconstraints=True)


# Add coincident constraints
import Sketcher
sk.addConstraint(Sketcher.Constraint('Coincident',10,2,0,2))
sk.addConstraint(Sketcher.Constraint('Coincident',10,1,0,1))

#extrude
App.getDocument('Unnamed').addObject('Part::Extrusion','Extrude')
f = App.getDocument('Unnamed').getObject('Extrude')
f.Base = App.getDocument('Unnamed').getObject('Sketch')
f.DirMode = "Normal"
f.DirLink = None
f.LengthFwd = 96.5 #edit this to match length of part
f.LengthRev = 0.000000000000000
f.Solid = True
f.Reversed = False
f.Symmetric = False
f.TaperAngle = 0.000000000000000
f.TaperAngleRev = 0.000000000000000

App.getDocument('Unnamed').getObject('Sketch').Visibility = False
App.ActiveDocument.recompute()