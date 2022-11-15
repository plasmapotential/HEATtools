#BfieldOnGrid.py
#Description:   outputs csv and vtp with Br,Bz on geqdsk grid
#Date:          20221115
#engineer:      T Looby
import sys
import numpy as np
#import HEAT MHDclass
EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

gFile = '/home/tom/work/CFS/devon/g000001.00001'
outFile = '/home/tom/work/CFS/devon/BrBz.csv'
MHD = MHDClass.setupForTerminalUse(gFile=gFile)
ep = MHD.ep

r = ep.g['R']
z = ep.g['Z']
R,Z = np.meshgrid(r,z)

Br = ep.B_R
Bz = ep.B_Z

rFlat = R.flatten()
zFlat = Z.flatten()
BrFlat = Br.flatten()
BzFlat = Bz.flatten()

array = np.vstack([rFlat,zFlat,BrFlat,BzFlat]).T
header = "R,Z,Br,Bz"
np.savetxt(outFile, array, delimiter=',',fmt='%.10f', header=header)
