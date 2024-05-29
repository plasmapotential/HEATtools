#batchFileFromGEQDSKs.py
#Description:   makes a HEAT batchFile from a dir of GEQDSKs
#Date:          20220901
#engineer:      T Looby
import os

#path where gfiles are read from and where we will save the batchFile.dat
rootPath = '/home/tlooby/HEATruns/SPARC/slowSweep/EQ/interpolated/dt10ms_vSP1200mmps/'

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
print(gFileList)
input('Press any key to continue')
for i,g in enumerate(gFileList):
    t = float(g.split('_')[1])
    #append line to batchFile
    line = 'sparc, slowSweep_lq0.6_S1.25_fRadDiv70_dt10ms_vSP1200mmps, 1, {:f}, '.format(t)+g+', T4_20231206_nominal.step, PFCs_T4_20231206.csv, SPARC_input.csv, hfOpt:elmer\n'
    if i==0:
        with open(rootPath + "batchFile.dat", "w") as myfile:
            myfile.write(line)
    else:
        with open(rootPath + "batchFile.dat", "a") as myfile:
            myfile.write(line)

print("Wrote batchFile.dat")
