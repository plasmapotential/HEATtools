#creates a component with a bezier top surface
#meant to be copied and pasted into FreeCAD python console

#=====TOROIDAL Bez Curve
import Draft
import Sketcher

#edits bezier control points below as necessary
points = [FreeCAD.Vector(-26.0, 0.0, 0.0), 
          FreeCAD.Vector(-26.0, 7.0, 0.0), 
          FreeCAD.Vector(-20.0, 7.0, 0.0), 
          FreeCAD.Vector( 0.0,  7.0, 0.0), 
          FreeCAD.Vector( 20.0, 7.0, 0.0), 
          FreeCAD.Vector( 26.0, 7.0, 0.0), 
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
sk.addConstraint(Sketcher.Constraint('Coincident',10,2,0,2))
sk.addConstraint(Sketcher.Constraint('Coincident',10,1,0,1))

#extrude
FreeCAD.ActiveDocument.addObject('Part::Extrusion','Extrude')
f = FreeCAD.ActiveDocument.getObject('Extrude')
f.Base = FreeCAD.ActiveDocument.getObject('Sketch')
f.DirMode = "Normal"
f.DirLink = None
f.LengthFwd = 96.5 #edit this to match length of part
f.LengthRev = 0.000000000000000
f.Solid = True
f.Reversed = False
f.Symmetric = False
f.TaperAngle = 0.000000000000000
f.TaperAngleRev = 0.000000000000000

FreeCAD.ActiveDocument.getObject('Sketch').Visibility = False
FreeCAD.ActiveDocument.recompute()




#=====POLOIDAL Bez Curve
import Draft
import Sketcher

#edits bezier control points below as necessary
points = [FreeCAD.Vector( 0.0, 0.0, 105.5), 
          FreeCAD.Vector( 0.0, 7.0, 105.5), 
          FreeCAD.Vector( 0.0, 7.0, 100.5), 
          FreeCAD.Vector( 0.0, 7.0, 52.75), 
          FreeCAD.Vector( 0.0, 7.0, 5.0), 
          FreeCAD.Vector( 0.0, 7.0, 0.0), 
          FreeCAD.Vector( 0.0, 0.0, 0.0)]


bez = Draft.make_bezcurve(points, closed=False, support=None, degree=None)


#line (edit points)
pl = FreeCAD.Placement()
pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
pl.Base = FreeCAD.Vector(0.0, 0.0, 96.5)
linePoints = [FreeCAD.Vector(0.0, 0.0, 0.0), FreeCAD.Vector(0.0, 0.0, 96.5)]
line = Draft.make_wire(linePoints, placement=pl, closed=False, face=True, support=None)
Draft.autogroup(line)
FreeCAD.ActiveDocument.recompute()


#add to sketch
sk = Draft.make_sketch([bez, line], autoconstraints=True)


# Add coincident constraints
sk.addConstraint(Sketcher.Constraint('Coincident',10,2,0,2))
sk.addConstraint(Sketcher.Constraint('Coincident',10,1,0,1))

#extrude
FreeCAD.ActiveDocument.addObject('Part::Extrusion','Extrude')
f = FreeCAD.ActiveDocument.getObject('Extrude')
f.Base = FreeCAD.ActiveDocument.getObject('Sketch')
f.DirMode = "Normal"
f.DirLink = None
f.LengthFwd = 52.0 #edit this to match length of part
f.LengthRev = 0.000000000000000
f.Solid = True
f.Reversed = False
f.Symmetric = False
f.TaperAngle = 0.000000000000000
f.TaperAngleRev = 0.000000000000000

FreeCAD.ActiveDocument.getObject('Sketch').Visibility = False
FreeCAD.ActiveDocument.recompute()

