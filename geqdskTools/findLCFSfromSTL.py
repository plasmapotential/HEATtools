#correctMultipleGEQDSKs.py
#Engineer:      T Looby
#Date:          20231214
#description:
#adjusts psiLCFS such that the psiN=1 surface just barely touches the PFC
#this is is designed for adjusting the LCFS in inner limited plasmas
#so that the LCFS is in contact with the PFC, whereas it might not
#be contacting the PFC if the RZ contour is used to defined psiLCFS

import numpy as np
import sys
import os
import shutil

EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass
import toolsClass
tools = toolsClass.tools()
from stl import mesh


rootPath = '/home/tlooby/HEATruns/SPARC/ILIM_shaping/EQ/limiterAdjust/'
outPath = '/home/tlooby/HEATruns/SPARC/ILIM_shaping/EQ/limiterAdjust/'

stlFile = '/home/tlooby/HEAT/data/SPARC/STLs/Compound___10.000000mm.stl'

#read all files with a prefix
prefix = 'sparc_'
suffix = '_movedLCFS_2.5mmOffset'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f and suffix not in f)])

print("GEQDSKs in this directory w/ prefix:")
print(gFileList)

#load mesh and calculate centers
mesh1 = mesh.Mesh.from_file(stlFile)
# Calculate centers of each triangle
centers = np.zeros((len(mesh1), 3))
for i, triangle in enumerate(mesh1.vectors):
    centers[i] = np.mean(triangle, axis=0) / 1000.0
R,Z,phi = tools.xyz2cyl(centers[:,0],centers[:,1],centers[:,2])


for i,gf in enumerate(gFileList):
    try:
        f = rootPath+gf
        MHD = MHDClass.setupForTerminalUse(gFile=f)
        ep = MHD.ep
    except: #EFIT reader is very specific about shot names
        newf = rootPath+'g000001.00001'
        shutil.copyfile(f, newf)
        MHD = MHDClass.setupForTerminalUse(gFile=newf)
        ep = MHD.ep

    #calculate psi on the centers
    psiN = ep.psiFunc.ev(R,Z) #psiN
    psiMin = np.min(psiN)
    newPsi = psiMin*(ep.g['psiSep'] - ep.g['psiAxis']) + ep.g['psiAxis']
    print("Original psi = {:f}".format(ep.g['psiSep']))
    ep.g['psiSep'] = newPsi
    print("New psi = {:f}".format(ep.g['psiSep']))

    newName = gf + suffix
    MHD.writeGfile(outPath + newName)

print("Complete")

    


    

