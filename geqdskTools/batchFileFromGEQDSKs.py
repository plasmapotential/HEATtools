#batchFileFromGEQDSKs.py
#Description:   makes a HEAT batchFile from a dir of GEQDSKs
#Date:          20220901
#engineer:      T Looby
import os

#path where gfiles are read from and where we will save the batchFile.dat
rootPath = '/home/tom/HEATruns/SPARC/oscillation/interpolated/dt200us_sinusoid_10mm_500Hz/'

#HEAT version
#v = 3
v = 4

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
print(gFileList)
input('Press any key to continue')
for i,g in enumerate(gFileList):
    #HEAT v3.0 convention
    if v == 3:
        t = int(g.split('.')[1])
        #append line to batchFile
        line = 'sparc, oscillationTest,'+g+', T4_20230915_nominal.step, PFCs.csv, SPARC_input_{:05d}.csv, hfOpt:T\n'.format(t)
    #HEAT v4.0 convention
    else:
        t = g.split('_')[1]
        #append line to batchFile
        line = 'sparc, 1, oscillationTest, '+t+', '+g+', T4_20230915_nominal.step, PFCs.csv, SPARC_input.csv, hfOpt:T\n'.format(t)
    
    if i==0:
        with open(rootPath + "batchFile.dat", "w") as myfile:
            myfile.write(line)
    else:
        with open(rootPath + "batchFile.dat", "a") as myfile:
            myfile.write(line)

print("Wrote batchFile.dat")
