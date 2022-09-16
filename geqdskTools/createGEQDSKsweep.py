#createGEQDSKsweep.py
#Description:   creates a GEQDSK sweep at specified freq and duration from list of gfiles
#               does NOT space the GEQDSKs evenly in Spol (use sweepInterpolaror.py for that)
#Engineer:      T Looby
#Date:          20220420
import numpy as np
import sys
import os
import shutil

EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

rootPath = '/home/tom/HEATruns/SPARC/sweep7_T4/interpolatedGfiles/'
#rootPath = '/home/tom/HEATruns/SPARC/sweep7/renamedFullSweep/'
outPath = '/home/tom/HEATruns/SPARC/sweep7_T4/interpolated1s/'

#expicitly define gFileList
#gFileList = ['geqdsk_freegsu_run{:d}.geq_newWall_negPsi'.format(x) for x in np.arange(18)]

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])


shot = 1
shotDur = 1 #seconds
freq = 1.0 #Hz

dt = int(round(freq / len(gFileList), 3)*1000.0) # rounded to nearest whole ms
N_steps = int(len(gFileList) * freq * shotDur)

print("dt = {:f}".format(dt))
print("N_steps = {:d}".format(N_steps))
print("adjusted shot length = {:f}".format(N_steps*dt))
print(len(gFileList))
try:
    os.mkdir(outPath)
except:
    print("could not make outPath!")

j=0
for i in range(N_steps):
    if j==0:
        print('=======')
    t = dt*(i+1)

    #write geqdsk
    gName = 'g{:06d}.{:05d}'.format(shot, int(t))
    print(gName)
    shutil.copyfile(rootPath+gFileList[j], outPath + gName)

    #append line to batchFile
    line = 'sparc,sweep7, '+gName+', lowerDivertorPFCs.step, lowerDivPFCs.csv, SPARC_input.csv, hfOpt:T\n'
    with open(outPath + "batchFile.dat", "a") as myfile:
        myfile.write(line)

    if j==len(gFileList)-1:
        j=0
    else:
        j+=1
print("final j: {:d}".format(j))
print("N gfiles: {:d}".format(len(gFileList)))
