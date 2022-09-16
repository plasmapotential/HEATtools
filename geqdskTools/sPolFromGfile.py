#calculateSpol.py
#Description:   Calculates Spol (poloidal coordinate) of strike point as a
#               function of geqdsk files (ie Spol(g))
#Date:          20220830
#engineer:      T Looby
import numpy as np
import sys
import os
import shutil
import scipy.interpolate as scinter
from scipy.interpolate import interp1d

EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

rootPath = '/home/tom/HEATruns/SPARC/sweep7_T5/originalGEQDSKs/'

#segments along divertor tile
#T4
#r0 = 1.578
#r1 = 1.82
#z0 = -1.303
#z1 = -1.6

#T5 bottom
r0 = 1.72
r1 = 1.84
z0 = -1.575
z1 = -1.575


rMag = r1-r0
zMag = np.abs(z1-z0)
vMag = np.sqrt(rMag**2+zMag**2)

#step size
dS = 0.001 #[m]
N = int(vMag / dS)

r = np.linspace(r0,r1,N)
z = np.linspace(z0,z1,N)
S = np.linspace(0,vMag,N)

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])

print(gFileList)

#f = rootPath + 'g000001.00000'
S_arr = []
for file in gFileList:
    f = rootPath + file
    MHD = MHDClass.setupForTerminalUse(gFile=f)
    psi = MHD.ep.psiFunc.ev(r,z)
    #fS = scinter.UnivariateSpline(psi, S, s = 0, ext = 'const')
    #fR = scinter.UnivariateSpline(psi, r, s = 0, ext = 'const')
    #fZ = scinter.UnivariateSpline(psi, z, s = 0, ext = 'const')
    fS = interp1d(psi, S, kind='linear')
    S_mapped = fS(1.0)
    S_arr.append(S_mapped)
    #R_mapped = fR(1.0)
    #Z_mapped = fZ(1.0)
    print(file+": {:0.8f}".format(S_mapped))

print(np.array(S_arr))
