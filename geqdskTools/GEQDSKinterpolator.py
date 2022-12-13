#GEQDSKinterpolator.py
#Description:   given a directory of geqdsks (named as g<shot>.<timestep>),
#               interpolate at user specified dt
#Engineer:      T Looby
#Date:          20221129
import numpy as np
import sys
import os
import shutil

EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

#===inputs, paths, etc.
rootPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/withTimesteps/'
outPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/interpolated/'
#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
#expicitly define gFileList
#gFileList = ['geqdsk_freegsu_run{:d}.geq_newWall_negPsi'.format(x) for x in np.arange(18)]

#===find timestep size, dt [ms]
#find common factors between two numbers
def factors(n):
    return sorted(list(
        factor for i in range(1, int(n**0.5) + 1) if n % i == 0
        for factor in (i, n//i)
    ))
#maximum allowable timestep size
dtMax = 25
tsOrig = [int(x.replace('g000001.', '')) for x in gFileList]
tMin = min(tsOrig)
tMax = max(tsOrig)
#mode for determining timestep size, dt.  Can be manual or factor
#in both cases rounds to nearest [ms]
mode='factor'
#define tMax manually
if mode=='manual':
    dt = dtMax
#define tMax using Sweep Trajectory final timestep and common factors
#inds the largest factor of the final timestep that is less than dtMax
#dtMax
else:
    fact = np.array(factors(tMax*1000))
    use = np.where(fact <= dtMax*1000.0)[0]

    if len(fact) == 0:
        print("Cannot find a factor.")
        sys.exit()
    else:
        dt = fact[use][-1] / 1000.0

print("Timestep size: {:f} [ms]".format(dt))
#build new timesteps
Nsteps = int( (tMax-tMin) / dt )
ts = np.linspace(tMin, tMax, Nsteps+1)

#===create interpolators for geqdsk
MHD = MHDClass.setupForTerminalUse(gFile=[rootPath+x for x in gFileList])
for i,t in enumerate(ts):

    #interpolate this timestep
    ep = MHD.gFileInterpolate(t)
    #write file
    name = 'g000001.{:05d}'.format(int(t))
    f = outPath + name
    MHD.writeGfile(f, shot=1, time=int(t), ep=ep)

print("Wrote all GEQDSKs")
