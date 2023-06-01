#correctMultipleGEQDSKs.py
#Description:   user specified modification of all geqdsks in a directory
#Engineer:      T Looby
#Date:          20220819

import numpy as np
import sys
import os
import shutil

EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

rootPath = '/home/tom/work/CFS/GEQDSKs/MEQ_20230501/originals/'
#rootPath = '/home/tom/HEATruns/SPARC/sweep7/renamedFullSweep/'
outPath = '/home/tom/work/CFS/GEQDSKs/MEQ_20230501/corrected/'

#expicitly define gFileList
#gFileList = ['geqdsk_freegsu_run{:d}.geq_newWall_negPsi'.format(x) for x in np.arange(18)]

#read all files with a prefix
prefix = 'sparc_'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])

print("GEQDSKs in this directory w/ prefix:")
print(gFileList)

#multipliers for various parameters (these are also in HEAT GUI)
#change these to flip sign of arrays they describe
psiRZMult = 1.0 / (2*np.pi)
psiSepMult = 1.0 / (2*np.pi)
psiAxisMult = 1.0 / (2*np.pi)
FpolMult = -1.0
Bt0Mult = -1.0
IpMult = -1.0

newPrefix = outPath+'g000001.'

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
    ep.g['psiRZ'] *= psiRZMult
    ep.g['psiSep'] *= psiSepMult
    ep.g['psiAxis'] *= psiAxisMult
    ep.g['Fpol'] *= FpolMult
    ep.g['Bt0'] *= Bt0Mult
    ep.g['Ip'] *= IpMult
    psi = ep.g['psiRZ']
    psiSep = ep.g['psiSep']
    psiAxis = ep.g['psiAxis']
    ep.g['psiRZn'] = (psi - psiAxis) / (psiSep - psiAxis)
    
    #use this for d3d naming convention
    #MHD.writeGfile(newPrefix+'{:05d}'.format(i))
    #use this to preserve original filename
    MHD.writeGfile(outPath + gf + "_PsiOver2pi_negIp_negBt_negFpol")

print("wrote all geqdsks")
