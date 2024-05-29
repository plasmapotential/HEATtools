#interpolateRZprofile.py
#Description:   interpolates an existing RZ scalar profile onto user supplied grid
#               defined by a bounding box
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


#===points we are interpolating
radPath = '/home/tlooby/HEATruns/AUG/validation39231/aug/'
f = radPath + 'input_rad_39231.csv'
data = np.genfromtxt(f, comments='#', delimiter=',')


#define bounding box [m]
rMin = 1.1
rMax = 1.8
zMin = -1.2
zMax = -0.6

#no bounding box [m]
#rMin = np.min(data[:,0])
#rMax = np.max(data[:,0])
#zMin = np.min(data[:,1])
#zMax = np.max(data[:,1])

NR = 40
NZ = 40
r = np.linspace(rMin,rMax,NR)
z = np.linspace(zMin,zMax,NZ)
R,Z = np.meshgrid(r, z)


#rData = np.unique(data[:,0])
#zData = np.unique(data[:,1])
#scalarFunc = interp.RectBivariateSpline(rData, zData, scalar)
#P = scalarFunc.ev(R,Z)

sparse_points = np.stack([data[:,0].ravel(), data[:,1].ravel()], -1)
dense_points = np.stack([R.ravel(), Z.ravel()], -1)
scalarFunc = interp.RBFInterpolator(sparse_points, data[:,2].ravel(),
                                         smoothing=0, kernel='cubic')
P = scalarFunc(dense_points).reshape(R.shape)

#if you want to normalize to 1.0MW, use this line
P /= np.sum(P)
#if you want to eliminate noise floor points, use this line
noise = np.where(P<0)
P[noise] = 0.0

#save CSV file with R,Z,power
N_cells = len(R.flatten())
outFile = radPath + "P_RZ_39231_interpolated_1600pts_box.csv"
pc = np.zeros((N_cells, 3))
pc[:,0] = R.flatten()#*1000.0 #convert to mm
pc[:,1] = Z.flatten()#*1000.0
pc[:,2] = P.flatten()
head = "R[m],Z[m],P[MW]"
np.savetxt(outFile, pc, delimiter=',',fmt='%.10f', header=head)


#save X,Y,Z,P for paraview
xyzFile = radPath + 'P_xyz_39231_interpolated_1600pts_box.csv'
phi = 0.0 #toroidal angle
pc = np.zeros((N_cells, 4))
pc[:,0] = R.flatten()*1000.0 #convert to mm
pc[:,2] = Z.flatten()*1000.0
pc[:,3] = P.flatten()
head = "X[m],Y[m],Z[m],P[MW]"
np.savetxt(xyzFile, pc, delimiter=',',fmt='%.10f', header=head)
