#createGEQDSKsweep.py
#Description:   calculates distance of mesh object from separatrix, saves VTP file
#Engineer:      T Looby
#Date:          20220420

import numpy as np
import sys
import os
import shutil

#rocinante
#EFITPath = '/home/tom/source'
#HEATPath = '/home/tom/source/HEAT/github/source'
#CFS machine
EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'

sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass
import ioClass
import CADClass


gFile = '/home/tlooby/HEATruns/SPARC/vscShadows/sparc/g000001.01210'
meshFile = '/home/tlooby/HEAT/data/SPARC/STLs/VSC_OLIM_OOLIM_160deg1412___10.00mm.stl'
outFile = '/home/tlooby/source/tomTest/VSC_distance2LCFS.vtp'

#get LCFS
MHD = MHDClass.setupForTerminalUse(gFile=gFile)
ep = MHD.ep
lcfs = MHD.ep.g['lcfs']

#get mesh object
CAD = CADclass.CAD()
mesh = CAD.load1Mesh(meshFile)
norms, ctrs, areas = CAD.normsCentersAreas([mesh])
ctrsRZ = np.zeros((len(ctrs), 2))
ctrsRZ[:,0] = np.sqrt(ctrs[:,0]**2 + ctrs[:,1]**2)
ctrsRZ[:,1] = ctrs[:,2]

#calculate distance between mesh object and LCFS
#looping for clarity
d = np.zeros((len(ctrs), len(lcfs)))
for i,ctr in enumerate(ctrs):
    for j,sep in enumerate(lcfs):
        dR = ctrsRZ[i,0] - lcfs[j,0]
        dZ = ctrsRZ[i,1] - lcfs[j,1]
        d[i,j] = np.sqrt(dR**2 + dZ**2)

dMin = np.minimum(d, axis=1)
print(dMin.shape)

#save VTP
#IO_HEAT = ioClass.IO_HEAT()
#IO_HEAT.writeMeshVTP(mesh, scalar, label, prefix, path)



