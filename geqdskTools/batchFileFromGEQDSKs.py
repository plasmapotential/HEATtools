#batchFileFromGEQDSKs.py
#Description:   makes a HEAT batchFile from a dir of GEQDSKs
#Date:          20220901
#engineer:      T Looby
import os

#path where gfiles are read from and where we will save the batchFile.dat
rootPath = '/home/tlooby/HEATruns/SPARC/sweepMEQ_T4/interpolated/dt100us_sinusoid_10mm_100Hz/'

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
print(gFileList)
input('Press any key to continue')
for i,g in enumerate(gFileList):
    t = int(g.split('.')[1])
    #append line to batchFile
    line = 'sparc, sweepMEQ_T4_20230915_nominal, '+g+', T4_20230915_nominal.step, PFCs_T4_20230915.csv, SPARC_input.csv, hfOpt:T\n'
    if i==0:
        with open(rootPath + "batchFile.dat", "w") as myfile:
            myfile.write(line)
    else:
        with open(rootPath + "batchFile.dat", "a") as myfile:
            myfile.write(line)

print("Wrote batchFile.dat")
