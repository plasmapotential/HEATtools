#sweepInterpolator.py
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
EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

rootPath = '/home/tom/HEATruns/SPARC/sweep7_T4/halfPeriod/'
outPath = '/home/tom/HEATruns/SPARC/sweep7_T4/S_interpolated/'

#segments along a divertor tile
#v2a
r0 = 1.578
r1 = 1.82
z0 = -1.303
z1 = -1.6
#v2y
#r0 = 1.5872
#r1 = 1.7899
#z0 = -1.3214
#z1 = -1.6092
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
Sfile = '/home/tom/source/dummyOutput/SPsweep.csv'
S_csv = np.genfromtxt(Sfile, comments='#', delimiter=',')
f_St = interp1d(S_csv[:,0], S_csv[:,1], kind='linear')
#create inverse function, f_tS
tMidIdx = np.argmax(S_csv[:,1])
#create monotonic function for inverse interpolation
f_tS = interp1d(S_csv[:tMidIdx,1], S_csv[:tMidIdx,0], kind='linear')


#generate t and S using user inputs
#timestep width
dtMax = 0.007 #[s]
#number of periods to stitch
Np = 1


#mode for determining timestep size, dt.  Can be manual or factor
#in both cases rounds to nearest [ms]
mode='manual'
#define tMax manually
if mode=='manual':
    #tMax = 0.735 #[s] #quadratic
    tMax = 0.651 #[s] #triangle
    dt = dtMax
#define tMax using Sweep Trajectory final timestep and common factors
#inds the largest factor of the final timestep that is less than dtMax
#dtMax
else:
    tMax = np.round(S_csv[-1,0], 3)
    fact = np.array(factors(tMax*1000))
    use = np.where(fact < dtMax*1000.0)[0]

    if len(fact) == 0:
        print("Cannot find a factor.")
        sys.exit()
    else:
        dt = fact[use][-1] / 1000.0

Nsteps = int(tMax / dt)
ts = np.linspace(0.0, Np*tMax, Nsteps+1)

print("Found dt = {:f} [s]".format(dt))
print(ts)
input()
S = f_St(ts)

#calculate S
#step size
dS = 0.001 #[m]
Ns = int(sMag / dS)

r = np.linspace(r0,r1,Ns)
z = np.linspace(z0,z1,Ns)
S_rz = np.linspace(0,sMag,Ns)

#read all files with a prefix and calculate S and t
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
S_gFiles = []
t_gFiles = []
for file in gFileList:
    f = rootPath + file
    MHD = MHDClass.setupForTerminalUse(gFile=f)
    psi = MHD.ep.psiFunc.ev(r,z)
    fS_g = interp1d(psi, S_rz, kind='linear')
    S_gFiles.append(fS_g(1.0))


#now normalize S from Spol(t) profile so Spol(0)=min(S_gFiles)
S += np.abs(S[0] - min(S_gFiles))

#create interpolators for geqdsk
MHD = MHDClass.setupForTerminalUse(gFile=[rootPath+x for x in gFileList])
MHD.Spols = S_gFiles
for i,t in enumerate(ts):
    #interpolate this timestep
    ep = MHD.gFileInterpolateByS(S[i])

    #here we are changing sign of Ip for a specific use case (flipping helicity)
    ep.g['Ip'] *= -1.0

    #write file
    name = 'g000001.{:05d}'.format(int(t*1000.0))
    f = outPath + name
    MHD.writeGfile(f, shot=1, time=int(t*1000.0), ep=ep)
