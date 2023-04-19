#createGEQDSKsweep.py
#Description:   calculates distance of mesh object from separatrix, saves VTP file
#Engineer:      T Looby
#Date:          20220420

import numpy as np
import sys
import os
import shutil

#rocinante
EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
FreeCADPath = '/usr/lib/freecad-daily/lib'
VDEPath = '/home/tom/source/cfsTools/VDEs'
sys.path.append(FreeCADPath)
sys.path.append(EFITPath)
sys.path.append(HEATPath)
sys.path.append(VDEPath)
import MHDClass
import ioClass
import CADClass
import matlabVDEclass


gFile = '/home/tom/source/dummyOutput/VSCdistance/g000001.01210'
meshFile = '/home/tom/source/dummyOutput/VSCdistance/BOX___2.00mm.stl'
outPath = '/home/tom/source/dummyOutput/VSCdistance/'
prefix = "REMCbox_distance2LCFS_121.0ms"


#get LCFS
MHD = MHDClass.setupForTerminalUse(gFile=gFile)
ep = MHD.ep
lcfsOrig = MHD.ep.g['lcfs']*1000.0
#use this matlab class to interpolate lcfs
mat = matlabVDEclass.matVDE()
lcfs = mat.interpolateWall(lcfsOrig, 1000.0)


#get mesh object
CAD = CADClass.CAD()
mesh = CAD.load1Mesh(meshFile)
norms, ctrs, areas = CAD.normsCentersAreas([mesh])
ctrsRZ = np.zeros((len(ctrs[0]), 2))
ctrsRZ[:,0] = np.sqrt(ctrs[0][:,0]**2 + ctrs[0][:,1]**2)
ctrsRZ[:,1] = ctrs[0][:,2]

#calculate distance between mesh object and LCFS
#looping for clarity
print("Calculating distances")
d = np.zeros((len(ctrsRZ), len(lcfs)))
for i,ctr in enumerate(ctrsRZ):
    for j,sep in enumerate(lcfs):
        dR = ctr[0] - sep[0]
        dZ = ctr[1] - sep[1]
        d[i,j] = np.sqrt(dR**2 + dZ**2)

dMin = np.amin(d, axis=1)
print("Closest Distance = {:f} [mm]".format(min(dMin)))
idx = np.argmin(dMin)
print("Closest PFC point:")
print(ctrsRZ[idx])
idx = np.argmin(d[idx,:])
print("Closest LCFS point:")
print(lcfs[idx])


#save VTP
IO_HEAT = ioClass.IO_HEAT()
label = "Distance to LCFS $[mm]$"
IO_HEAT.writeMeshVTP(mesh, dMin, label, prefix, outPath)



