#makeSweepLonger.py
#Description:   given a set of GEQDSKs representing a sweep of 1 period,
#               duplicates it a user specified number of times, resulting in a
#               longer sweep
#Date:          20220901
#engineer:      T Looby
import os
import numpy as np
import shutil

rootPath = '/home/tom/HEATruns/SPARC/sweep7_T4/S_interpolated_vSweep0.7_dt7ms_tri_10s/'
#number of times to duplicate
N = 16
dt = 7 #[ms]
tMaxOrig = 651 #ms
tMax = tMaxOrig
#tMax = tMaxOrig - dt #if tMaxOrig=t0
NstepsOrig = int(tMax / dt)

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
print(gFileList)

tsOrig = np.linspace(0,tMax, NstepsOrig+1)
tsNew = np.linspace(0,tMax*N, NstepsOrig*N+1)
print("Old timesteps")
print(tsOrig)
print("New timesteps")
print(list(tsNew))
print(len(gFileList))
input('Press any key to continue')
for j in range(N-1):
    for i in range(len(gFileList)):
        t = tMax*(j+1) + (i)*dt
        newG = rootPath + 'g000001.{:05d}'.format(t)
        oldG = rootPath + gFileList[i]
        shutil.copyfile(oldG,newG)
        print(newG)
print("Sweep extension completed")
