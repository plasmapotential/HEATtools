#batchFileFromGEQDSKs.py
#Description:   makes a HEAT batchFile from a dir of GEQDSKs
#Date:          20220901
#engineer:      T Looby
import os

#path where gfiles are read from and where we will save the batchFile.dat
rootPath = '/home/tom/HEATruns/SPARC/sweep7_T4/S_interpolated_vSweep0.7_dt7ms_tri_10s/'

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
print(gFileList)
input('Press any key to continue')
for i,g in enumerate(gFileList):
    #append line to batchFile
    line = 'sparc,sweep7_triangle, '+g+', axisymmetricT4.step, PFCs.csv, SPARC_input.csv, hfOpt:T\n'
    with open(rootPath + "batchFile.dat", "a") as myfile:
        myfile.write(line)

print("Wrote batchFile.dat")
