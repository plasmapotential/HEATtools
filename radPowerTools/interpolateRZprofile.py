#interpolateRZprofile.py
#Description:   interpolates an existing RZ scalar profile onto user supplied
#               RZ grid
#Engineer:      T Looby
#Date:          20230120

import sys
import shutil
import numpy as np
import scipy.interpolate as interp
EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

#===points we are going to interpolate onto
path = '/home/tom/work/CFS/projects/coreRadiation/'
gFile = path + 'geqdsk_nominal'
#read GEQDSK that this data corresponds to
try:
    MHD = MHDClass.setupForTerminalUse(gFile=gFile)
    ep = MHD.ep
except: #EFIT reader is very specific about shot names
    newf = path+'g000001.00001'
    shutil.copyfile(gFile, newf)
    MHD = MHDClass.setupForTerminalUse(gFile=newf)
    ep = MHD.ep
R,Z = np.meshgrid(ep.g['R'], ep.g['Z'])

psi2D = ep.g['psiRZn']
#filter out points above/below this z
zMax = 1.1 #[m]
#use = np.where(np.logical_and(psi2D < 1.0, np.abs(Z)<zMax))
use = np.where(psi2D < 20.0) #use all points

#===points we are interpolating
profPath = '/home/tom/work/CFS/projects/TRANSPdata/SPARC_V1E_transp_scan_2/'
f = profPath + 'Prad2D.csv'
data = np.genfromtxt(f, comments='#', delimiter=',')
r = np.unique(data[:,0])
z = np.unique(data[:,1])
scalar = data[:,2].reshape(len(r),len(z))
scalarFunc = interp.RectBivariateSpline(r, z, scalar)
P = scalarFunc(ep.g['R'],ep.g['Z'])[use]

#save CSV file with R,Z,power
N_cells = len(R[use].flatten())
outFile = path + "P_RZ_interpolated.csv"
pc = np.zeros((N_cells, 3))
pc[:,0] = R[use].flatten()#*1000.0 #convert to mm
pc[:,1] = Z[use].flatten()#*1000.0
pc[:,2] = P.flatten()
head = "R[m],Z[m],P[MW]"
np.savetxt(outFile, pc, delimiter=',',fmt='%.10f', header=head)


#save X,Y,Z,P for paraview
xyzFile = path + 'P_xyz_interpolated.csv'
phi = 0.0 #toroidal angle
pc = np.zeros((N_cells, 4))
pc[:,0] = R[use].flatten()*1000.0 #convert to mm
pc[:,2] = Z[use].flatten()*1000.0
pc[:,3] = P.flatten()
head = "X[m],Y[m],Z[m],P[MW]"
np.savetxt(xyzFile, pc, delimiter=',',fmt='%.10f', header=head)
