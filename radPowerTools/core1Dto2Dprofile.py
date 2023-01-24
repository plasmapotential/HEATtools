#core1Dto2Dprofile.py
#Description:   takes a 1D core radiation profile and interpolates it to an RZ grid
#Engineer:      T Looby
#Date:          20230123
import sys
import shutil
import numpy as np
import scipy.interpolate as interp
EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

path = '/home/tom/work/CFS/projects/TRANSPdata/SPARC_V1E_transp_scan_2/'
fIn = path + 'Prad1D.csv'

#TRANSP EQ
#fGEQDSK = path + 'TRANSPrun.geq'
#fOut = path + 'Prad2D_transp.csv'

#freegs EQ
fGEQDSK = path + 'geqdsk_nominal'
fOut = path + 'Prad2D_freegs.csv'

#read 1D profile
data1D = np.genfromtxt(fIn, comments='#', delimiter=',')

#read GEQDSK that this data corresponds to
try:
    MHD = MHDClass.setupForTerminalUse(gFile=fGEQDSK)
    ep = MHD.ep
except: #EFIT reader is very specific about shot names
    newf = path+'g000001.00001'
    shutil.copyfile(fGEQDSK, newf)
    MHD = MHDClass.setupForTerminalUse(gFile=newf)
    ep = MHD.ep

#get data from TRANSP file
psi_X = data1D[:,0]
P_1D = data1D[:,1]

#extend profile all the way to magnetic axis
psi_X = np.insert(psi_X,0,0)
P_1D = np.insert(P_1D, 0, P_1D[0])

#get RZ grid from GEQDSK
r,z = np.meshgrid(ep.g['R'], ep.g['Z'])
psi2D = ep.g['psiRZn']

#only use points inside separatrix
#filter out points above/below this z
zMax = 1.1 #[m]
#use = np.where(np.logical_and(psi2D < 1.0, np.abs(Z)<zMax))
#use = np.where(psi2D<max(psi_X))
#only use points between min/max psi_X
use = np.where(np.logical_and(np.abs(z)<zMax , np.logical_and(psi2D<max(psi_X), psi2D>min(psi_X)) ))


#interpolation: P = f(psiN)
f_P = interp.interp1d(psi_X, P_1D)
#calculate power density
PD_2D = np.zeros((ep.g['NR'], ep.g['NZ']))
PD_2D[use] = f_P(psi2D[use])

#integrate power density toroidally
A_cell = ep.g['dR']*ep.g['dZ']
V_cell = A_cell * 2.0 * np.pi * r
P_2D = PD_2D * V_cell

#total power radiated
P_tot = np.sum(P_2D)
print("Total radiated power ~= {:f} [MW]".format(P_tot))
print("Total # pts ~= {:d}".format(len(r[use].flatten())))

scalePowerMask = True
if scalePowerMask == True:
    P_2D *= 1.0 / P_tot
    print("New total radiated power ~= {:f} [MW]".format(np.sum(P_2D)))
#save CSV file with R,Z,power for HEAT
pc = np.zeros((len(r[use].flatten()), 3))
pc[:,0] = r[use].flatten()#*1000.0 #convert to mm
pc[:,1] = z[use].flatten()#*1000.0
pc[:,2] = P_2D[use].flatten()
head = "R[m],Z[m],P[MW]"
np.savetxt(fOut, pc, delimiter=',',fmt='%.10f', header=head)

#save X,Y,Z,P for paraview
xyzFile = path + 'P_xyz.csv'
phi = 0.0 #toroidal angle
pc = np.zeros((len(r[use].flatten()), 4))
pc[:,0] = r[use].flatten()*1000.0 #convert to mm
pc[:,2] = z[use].flatten()*1000.0
pc[:,3] = P_2D[use].flatten()
head = "X[m],Y[m],Z[m],P[MW]"
np.savetxt(xyzFile, pc, delimiter=',',fmt='%.10f', header=head)
