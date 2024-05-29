#sweepInterpolatorFromSpol.py
#Description:   Uses a Spol(t) profile from csv file, and existing GEQDSKs, to
#               stitch together a SP sweep at user specified dt
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
rootPath = '/home/tlooby/HEATruns/SPARC/oscillation_sweep/EQs/originalEQs/'
#geqdsks out
outPath = '/home/tlooby/HEATruns/SPARC/oscillation_sweep/EQs/interpolated/dt10ms_oneDir_400mmPerSec_150mm/'
#Spol(t) profile, which should be 1 period
Sfile = '/home/tlooby/HEATruns/SPARC/oscillation_sweep/EQs/SPsweep_oneDir_400mmPerSec.csv'
#timestep width
dtMax = 0.01 #[s]
#number of periods to stitch
Np = 1

#segments along a divertor tile
#v2a
#r0 = 1.578
#r1 = 1.82
#z0 = -1.303
#z1 = -1.6
#v2y
#r0 = 1.5872
#r1 = 1.7899
#z0 = -1.3214
#z1 = -1.6092
#T5 bottom
#r0 = 1.72
#r1 = 1.84
#z0 = -1.575
#z1 = -1.575

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


#find common factors between two numbers
def factors(n):
    return sorted(list(
        factor for i in range(1, int(n**0.5) + 1) if n % i == 0
        for factor in (i, n//i)
    ))
#read the Spol(t) profile, which should be 1 period
S_csv = np.genfromtxt(Sfile, comments='#', delimiter=',')
#use this for periodic cases
#f_St = interp1d(S_csv[:,0], S_csv[:,1], kind='linear')
#use this if you have a linear sweep and you are running into bound errors
f_St = interp1d(S_csv[:,0], S_csv[:,1], kind='linear', bounds_error=False, fill_value='extrapolate')
#create inverse function, f_tS
tMidIdx = np.argmax(S_csv[:,1])
#create monotonic function for inverse interpolation
f_tS = interp1d(S_csv[:tMidIdx,1], S_csv[:tMidIdx,0], kind='linear')


#generate t and S using user inputs
#mode for determining timestep size, dt.  Can be manual or factor
mode='manual'
#define tMax manually
if mode=='manual':
    #tMax = 0.57 #[s] #quadratic
    #tMax = 0.651 #[s] #triangle
    #tMax = 0.3 #[s] #T5
    tMax = np.round(S_csv[-1,0], 10) #[s]
    dt = dtMax
#define tMax using Sweep Trajectory final timestep and common factors
#finds the largest factor of the final timestep that is less than dtMax
#dtMax
else:
    tMax = np.round(S_csv[-1,0], 3)
    fact = np.array(factors(tMax*1000))
    use = np.where(fact <= dtMax*1000.0)[0]

    if len(fact) == 0:
        print("Cannot find a factor.")
        sys.exit()
    else:
        dt = fact[use][-1] / 1000.0

Nsteps = int(np.round(tMax / dt))
tMax = Nsteps * dt
ts = np.linspace(0.0, Np*tMax, Nsteps+1)
print("Found dt = {:f} [s]".format(dt))
S = f_St(ts)

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
    if np.min(psi) > 1.0:
        print("skipping EQ: "+file)
        print("min psi for skipped EQ: {:f}".format(np.min(psi)))
    else:
        fS_g = interp1d(psi, S_rz, kind='linear')
        S_gFiles.append(fS_g(1.0))
        print(fS_g(1.0))

#now normalize S from Spol(t) profile so Spol(0)=min(S_gFiles)
#=== FOR PERIODIC S:
#S += np.abs(S[0] - min(S_gFiles))
#alternatively, change S so it is in middle of target
#S += (np.max(S_gFiles) - np.min(S_gFiles)) / 2.0 + np.min(S_gFiles)
#alternatively, use a predefined definition of S
#S += 0.9*(np.max(S_gFiles) - np.min(S_gFiles)) / 2.0 + np.min(S_gFiles)
#=== SLOW SCAN S IN ONE DIRECTION:
S += 0.05*(np.max(S_gFiles) - np.min(S_gFiles)) + np.min(S_gFiles)
#S += np.min(S_gFiles)

print("GEQDSK dS: {:f}mm".format(np.max(S_gFiles) - np.min(S_gFiles)))

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

