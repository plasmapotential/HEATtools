#makeSweepLonger.py
#Description:   given a set of GEQDSKs representing a sweep of 1 period,
#               duplicates it a user specified number of times, resulting in a
#               longer sweep
#Date:          20220901
#engineer:      T Looby
import os
import numpy as np
import shutil

rootPath = '/home/tlooby/HEATruns/SPARC/oscillation_sweep/EQs/interpolated/dt500us_sinusoid_20mm_100Hz/0.5s_sweep/'
#HEAT v3.X
#v=3
#HEAT v4.X
v=4

#If you are pasting 1 period of gfiles in here, you need to remove the last gfile 
#if it is the same eq as the first gfile.  gfiles should start at 0ms

#number of times to duplicate
N = 50
dt =  0.0005#[s]
tMaxOrig =  0.01#[s]
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

print(len(tsNew))
input('Press any key to continue')

for j in range(N-1):
    for i in range(len(gFileList)):
        t = tMax*(j+1) + (i)*dt
        if v==3:
            newG = rootPath + 'g000001.{:05d}'.format(t)
        else:
            newG = rootPath + 'g000001_{:08f}'.format(t)
        oldG = rootPath + gFileList[i]

        shutil.copyfile(oldG,newG)
        #print(oldG)
        print(newG)
        #input()
print("Sweep extension completed")
