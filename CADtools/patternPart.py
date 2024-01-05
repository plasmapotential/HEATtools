#script to pattern a part object toroidally
#meant to be used as a macro in FreeCAD python console

N_tor = 1  # number of copies in toroidal direction
N_pol = 13  # number of copies in poloidal direction
translationZ = 106.5  # Translation increment for z-axis [mm]
tSign = -1.0 #translate in positive or negative z
rotationAngle = 2.5  # Rotation increment about z-axis [degrees]
aSign = 1.0 #translate in positive or negative angle

objs = FreeCADGui.Selection.getSelection() #only use first selected part

idx = 0
newObjs = []
for i in range(N_tor):
    for j in range(N_pol):
        for k,obj in enumerate(objs):
            newObjs.append(App.ActiveDocument.copyObject(obj))
            newObjs[-1].Label = 'T{:03d}'.format(idx)
            newObjs[-1].Placement = obj.getGlobalPlacement()
            # Calculate transformation
            translation = App.Vector(0, 0, tSign*translationZ * (i))
            rotation = App.Rotation(App.Vector(0, 0, 1), aSign*rotationAngle * (j))
            #rotation1 = App.Rotation(App.Vector(0, 0, 0), App.Vector(0, 0, 1), aSign*rotationAngle * (j+1))
            # Apply transformation
            newObjs[-1].Placement.translate(translation)
            newObjs[-1].Placement.rotate(App.Vector(0, 0, 1), App.Vector(0, 0, 0), aSign*rotationAngle * (j))
            idx +=1
 

FreeCAD.ActiveDocument.recompute()