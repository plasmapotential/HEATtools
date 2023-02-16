#core2DRadProfile.py
#Description:   creates an axisymmetric radiation profile on a grid inside
#               separatrix from GEQDSK
#Engineer:      T Looby
#Date:          20230118
import sys
import shutil
import numpy as np
import scipy.interpolate as interp
EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

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

#calculate the area of the core using shoelace method
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

rLcfs = ep.g['lcfs'][:,0]
zLcfs = ep.g['lcfs'][:,1]
A_core = PolyArea(rLcfs,zLcfs)

P_tot = 1.0 #MW

#get grid points (points inside separatrix)
R,Z = np.meshgrid(ep.g['R'], ep.g['Z'])
psi2D = ep.g['psiRZn']
#use = np.where(psi2D < 1.0)

#filter out points above/below this z
zMax = 1.1 #[m]
use = np.where(np.logical_and(psi2D < 1.0, np.abs(Z)<zMax))

#get volumes of each cell in grid
A_cell = ep.g['dR']*ep.g['dZ']
V_cell = A_cell * 2.0 * np.pi * R[use]
N_cells = len(V_cell.flatten())

xPt = np.where(psi2D)

#total volume of core
V_core = np.sum(V_cell)

#power density
PD = P_tot / V_core

#create uniform power density profile
P = PD * V_cell

#save CSV file with R,Z,power
outFile = path + "P_RZ.csv"
pc = np.zeros((N_cells, 3))
pc[:,0] = R[use].flatten()#*1000.0 #convert to mm
pc[:,1] = Z[use].flatten()#*1000.0
pc[:,2] = P.flatten()
head = "R[m],Z[m],P[MW]"
np.savetxt(outFile, pc, delimiter=',',fmt='%.10f', header=head)


#save X,Y,Z,P for paraview
xyzFile = path + 'P_xyz.csv'
phi = 0.0 #toroidal angle
pc = np.zeros((N_cells, 4))
pc[:,0] = R[use].flatten()*1000.0 #convert to mm
pc[:,2] = Z[use].flatten()*1000.0
pc[:,3] = P.flatten()
head = "X[m],Y[m],Z[m],P[MW]"
np.savetxt(xyzFile, pc, delimiter=',',fmt='%.10f', header=head)
