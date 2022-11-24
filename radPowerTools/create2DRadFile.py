#create2DRadFile.py
#Description:   creates an axisymmetric radiation profile on a grid
#Engineer:      T Looby
#Date:          20220614

import numpy as np
import pandas as pd

#csv file to save
pcFile = '/home/tom/source/dummyOutput/RZpower.csv'

#create R,Z grid
#rMin = 1.0 #meters
#rMax = 2.5
#NR = 50
#zMin = -1.85
#zMax = 1.85
#NZ = 50

rMin = 1.755 #meters
rMax = 1.805
NR = 20
zMin = -1.5025
zMax = -1.4525
NZ = 20


#minor radius #[m]
a = 0.02
#Total power
Ptotal = 4.212 #MW

#define center manually (otherwise defined below at center of grid below)
manualCtr = True
rCtr = 1.78
zCtr = -1.4775

r = np.linspace(rMin, rMax, NR)
z = np.linspace(zMin, zMax, NZ)
Rgrid,Zgrid = np.meshgrid(r,z)

dr = np.diff(r)[0]
dz = np.diff(z)[0]

r2 = r-dr/2.0
z2 = z-dz/2.0
r2 = np.append(r2, r[-1]+dr/2.0)
z2 = np.append(z2, z[-1]+dz/2.0)
R, Z = np.meshgrid(r,z)
R2, Z2 = np.meshgrid(r2,z2)
dR2 = np.diff(R2)
dZ2 = np.diff(Z2, axis=0)
#area surrounding each point (ie a "cell")
A = np.zeros((NZ,NR))
for i in range(NZ):
    for j in range(NR):
        A[i,j] = np.abs( (Z2[i+1,j] - Z2[i,j]) * (R2[i,j+1] - R2[i,j]) )

#volume of each cell
V = A*2*np.pi*R
Vtotal = np.sum(V)

#create a uniform circular profile centered between rMin,rMax,zMin,zMax
if manualCtr == False:
    rCtr = (rMax - rMin) / 2.0 + rMin
    zCtr = (zMax - zMin) / 2.0 + zMin

#only assign power to mesh elements within minor radius
dist2Ctr = np.sqrt((R-rCtr)**2 + (Z-zCtr)**2)
use = np.where(dist2Ctr < a)
#core volume
Vcore = np.sum(V[use])
#power density (here uniform)
powerMask = np.zeros((V.shape))
powerMask[use] = 1.0
PD = Ptotal / Vcore
PDmatrix = PD*powerMask
P = PDmatrix*V

#save CSV file with R,Z,power
pc = np.zeros((NR*NZ, 3))
pc[:,0] = R.flatten()#*1000.0 #convert to mm
pc[:,1] = Z.flatten()#*1000.0
pc[:,2] = P.flatten()
head = "R[m],Z[m],P[MW]"
np.savetxt(pcFile, pc, delimiter=',',fmt='%.10f', header=head)


##the following lines are for testing out functions that will be included in HEAT
#PC2D = pd.read_csv(pcFile, header=0, names=['R','Z','P'])
#
##create 3D point cloud
#N3D = 10
#phis = np.linspace(0,2*np.pi, N3D+1)[:-1]
#phiArr = []
#for i in range(N3D):
#    phiArr.append([phis[i]]*len(PC2D))
#phiArr = np.array(phiArr)
#rad3D = np.zeros((N3D*len(PC2D),4))
#rad3D[:,0] = PC2D['R'].values * np.cos(phiArr)
#rad3D[:,1] = PC2D['R'].values * np.sin(phiArr)
#rad3D[:,2] = PC2D['Z'].values * np.cos(phiArr)
