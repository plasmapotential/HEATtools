#batchFileFromGEQDSKs.py
#Description:   makes a HEAT batchFile from a dir of GEQDSKs
#Date:          20220901
#engineer:      T Looby
import os

#path where gfiles are read from and where we will save the batchFile.dat
rootPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/interpolated_100ms/'

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
print(gFileList)
input('Press any key to continue')
for i,g in enumerate(gFileList):
    t = int(g.split('.')[1])
    #append line to batchFile
    line = 'sparc,rampup_TSCvh01a, '+g+', fullSlice.stp, PFCs.csv, SPARC_input_{:05d}.csv, hfOpt:T\n'.format(t)
    if i==0:
        with open(rootPath + "batchFile.dat", "w") as myfile:
            myfile.write(line)
    else:
        with open(rootPath + "batchFile.dat", "a") as myfile:
            myfile.write(line)

print("Wrote batchFile.dat")
