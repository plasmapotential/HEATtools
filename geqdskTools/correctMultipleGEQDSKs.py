#correctMultipleGEQDSKs.py
#Description:   user specified modification of all geqdsks in a directory
#Engineer:      T Looby
#Date:          20220819

import numpy as np
import sys
import os
import shutil

EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

#rootPath = '/home/tlooby/projects/MEQ_EQ/tmp/'
#outPath = '/home/tlooby/projects/MEQ_EQ/corrected/'

#rootPath = '/home/tlooby/source/tomTest/dummyEQ/'
#outPath = '/home/tlooby/source/tomTest/dummyEQ/'

rootPath = '/home/tlooby/projects/RE_limiter_EQ/originals/'
outPath = '/home/tlooby/projects/RE_limiter_EQ/corrected/'

netcdfOut = False

#expicitly define gFileList
#gFileList = ['geqdsk_freegsu_run{}.geq_newWall_negPsi'.format(x) for x in np.arange(18)]

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

newPrefix = outPath+'sparc_negBt_negFpol_negIp_psiOver2pi'

for i,gf in enumerate(gFileList):
    try:
        f = rootPath+gf
        print(f)
        MHD = MHDClass.setupForTerminalUse(gFile=f)
        ep = MHD.ep
    except: #EFIT reader is very specific about shot names
        print("copying")
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
    newName = gf + '_PsiOver2pi_negIp_negBt_negFpol'
    if netcdfOut==True:
        MHD.writeNetCDF(ep.g, outPath + newName + '.nc')
        print(ep.g['q'])
        print(len(ep.g['q']))
    else:

        MHD.writeGfile(outPath + newName, ep=ep)

print("wrote all files")
