#correctMultipleGEQDSKs.py
#Engineer:      T Looby
#Date:          20231214
#description:
#changes psiSep such that it is redefined at a user specified value of psiN

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



rootPath = '/home/tlooby/HEATruns/SPARC/IOLIM_shaping/EQ/misalignments/'
outPath = '/home/tlooby/HEATruns/SPARC/IOLIM_shaping/EQ/misalignments/'

#read all files with a prefix
prefix = 'sparcVDE'
suffix = '_LCFS_psiN9989'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f and suffix not in f)])

print("GEQDSKs in this directory w/ prefix:")
print(gFileList)

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

    #write new psiSep value from user specified psiN
    psiN = 0.9989
    print("Original psi = {:f}".format(ep.g['psiSep']))
    newPsiSep = psiN * (ep.g['psiSep'] - ep.g['psiAxis']) + ep.g['psiAxis']
    ep.g['psiSep'] = newPsiSep
    print("New psi = {:f}".format(ep.g['psiSep']))

    newName = gf + suffix
    MHD.writeGfile(outPath + newName)

print("Complete")

    


    

