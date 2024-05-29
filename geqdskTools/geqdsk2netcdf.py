#converts a geqdsk to netcdf
import numpy as np
import sys
import os
import shutil

EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

rootPath = '/home/tlooby/source/sparc_Forced_VDE/Equilibria/originals/'
outPath = '/home/tlooby/source/sparc_Forced_VDE/Equilibria/'


#read all files with a prefix
prefix = 'sparc_'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])

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

    MHD.writeNetCDF(ep.g, outPath + gf + '.nc')
    print(ep.g['q'])
    print(len(ep.g['q']))