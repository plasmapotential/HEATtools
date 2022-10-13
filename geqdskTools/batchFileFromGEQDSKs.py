#batchFileFromGEQDSKs.py
#Description:   makes a HEAT batchFile from a dir of GEQDSKs
#Date:          20220901
#engineer:      T Looby
import os

#path where gfiles are read from and where we will save the batchFile.dat
rootPath = '/home/tom/HEATruns/SPARC/sweep7_T5/interpGEQDSK_T5_triangular_dt10ms_vSweep0.5ms/'

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
print(gFileList)
input('Press any key to continue')
for i,g in enumerate(gFileList):
    #append line to batchFile
    line = 'sparc,sweep7_T5_triangle, '+g+', T5_withPlanes.stp, PFCs.csv, SPARC_input.csv, hfOpt:T\n'
    with open(rootPath + "batchFile.dat", "a") as myfile:
        myfile.write(line)

print("Wrote batchFile.dat")
