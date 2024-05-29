#sweepInterpolatorFromSpol.py
#Description:   Stiches a SP sweep at user specified dt between two GEQDSKs
#Date:          20220831
#engineer:      T Looby
#
#how to build a sweep using vSweep, turntime, and geqdsks
#1) run SpolFromVelocity.py to define SP trajectory
#2) run sweepInterpolator.py to interpolate GEQDSKs along SP trajectory
#3) run makeGEQDSKimages.py to generate .pngs of each sweep step

import numpy as np
import pandas as pd
import sys
import os
import shutil
import scipy.interpolate as scinter
from scipy.interpolate import interp1d
import plotly.graph_objects as go
from functools import reduce

#you need a valid HEAT install.  can be run in container
EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

#geqdsks in
rootPath = '/home/tlooby/HEATruns/SPARC/slowSweep/EQ/originals/'
#geqdsks out
outPath = '/home/tlooby/HEATruns/SPARC/slowSweep/EQ/interpolated/dt10ms_vSP1200mmps/'
#timestep width
dt = 0.01 #[s]
#strike point velocity
vSP = 1.2 #[m/s]

#v3b
#T4
r0 = 1.57
r1 = 1.72
z0 = -1.297
z1 = -1.51
#S_midT4 = 1.762

#mid tile T4
#r0 = 1.6203
#r1 = 1.6707
#z0 = -1.3685
#z1 = -1.4378
rMag = r1-r0
zMag = np.abs(z1-z0)
sMag = np.sqrt(rMag**2+zMag**2)

#calculate S
#step size
dS = 0.0001 #[m]
Ns = int(sMag / dS)
r = np.linspace(r0,r1,Ns)
z = np.linspace(z0,z1,Ns)
S_rz = np.linspace(0,sMag,Ns)

#read all files with a prefix and calculate S and t
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
S_gFiles = []
t_gFiles = []
print(gFileList)
for file in gFileList:
    print(file)
    f = rootPath + file
    MHD = MHDClass.setupForTerminalUse(gFile=f)
    psi = MHD.ep.psiFunc.ev(r,z)
    fS_g = interp1d(psi, S_rz, kind='linear')
    S_gFiles.append(fS_g(1.0))
    print(fS_g(1.0))


tMax = (np.max(S_gFiles) - np.min(S_gFiles)) / vSP
Nsteps = int(np.round(tMax / dt))
ts = np.linspace(0.0, dt*Nsteps, Nsteps+1)
S = np.linspace(np.min(S_gFiles),np.max(S_gFiles),Nsteps+1)

print("GEQDSK dS: {:f} [m]".format(np.max(S_gFiles) - np.min(S_gFiles)))
print("Min S: {:f}[m]".format(np.min(S_gFiles)))
print("Max S: {:f}[m]".format(np.max(S_gFiles)))
print("Sweep duration: {:f}[s]".format(tMax))

#create interpolators for geqdsk
MHD = MHDClass.setupForTerminalUse(gFile=[rootPath+x for x in gFileList])
MHD.Spols = S_gFiles 
#ts += dt
print(ts)
input()
for i,t in enumerate(ts):
    #interpolate this timestep
    print(S[i])
    ep = MHD.gFileInterpolateByS(S[i])

    #here we are changing sign of Ip for a specific use case (flipping helicity)
    #ep.g['Ip'] *= -1.0

    #write file
    #time = int(round(t*1000.0)) #offset timesteps by one dt so we dont start at 0 ms
    #HEAT v4.0 convention
    name = 'g000001_{:08f}'.format(t)
    #HEAT v3.0 convention
    #name = 'g000001_{:06d}'.format(i)
    f = outPath + name
    MHD.writeGfile(f, shot=1, time=t, ep=ep)

