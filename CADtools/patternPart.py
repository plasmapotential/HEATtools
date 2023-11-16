#script to pattern a part object toroidally
#meant to be used as a macro in FreeCAD python console



# User-defined variables
partName = "torBez30mm_2mmCham"  # Replace with the name of your part
N_tor = 3  # number of copies in toroidal direction
N_pol = 2  # number of copies in poloidal direction
translationZ = 106.5  # Translation increment for z-axis [mm]
rotationAngle = 2.5  # Rotation increment about z-axis [degrees]


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
            translation = App.Vector(0, 0, translationZ * (i + 1))
            rotation = App.Rotation(App.Vector(0, 0, 1), rotationAngle * (j + 1))

            # Apply transformation
            newObjs[-1].Placement = App.Placement(translation, rotation)

            idx +=1

doc.recompute()