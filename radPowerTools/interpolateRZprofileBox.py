#interpolateRZprofile.py
#Description:   interpolates an existing RZ scalar profile onto user supplied grid
#               defined by a bounding box
#Engineer:      T Looby
#Date:          20230120

import sys
import shutil
import numpy as np
import scipy.interpolate as interp
from matplotlib.path import Path

EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)

#===points we are interpolating
radPath = '/home/tlooby/HEATruns/AUG/validation39231/aug/'
f = radPath + 'input_rad_39231.csv'
data = np.genfromtxt(f, comments='#', delimiter=',')

#define bounding box [m]
rMin = 1.1
rMax = 1.65
zMin = -1.2
zMax = -0.5

#no bounding box [m]
#rMin = np.min(data[:,0])
#rMax = np.max(data[:,0])
#zMin = np.min(data[:,1])
#zMax = np.max(data[:,1])

NR = 40
NZ = 20
r = np.linspace(rMin,rMax,NR)
z = np.linspace(zMin,zMax,NZ)
R,Z = np.meshgrid(r, z)


#if we want to only include points within the rlim,zlim from a GEQDSK, 
#set this flag to true
limBound = True
if limBound == True:
    import MHDClass
    gFile = '/home/tlooby/HEATruns/AUG/validation39231/aug/39231_3.000.eqdsk'
    MHD = MHDClass.setupForTerminalUse(gFile=gFile)
    ep = MHD.ep
    # Create a Path object from the contour points
    contour_path = Path(ep.g['wall'])
    points = np.stack((R.flatten(), Z.flatten())).T
    inside = contour_path.contains_points(points)
else:
    inside= np.ones((NZ*NR))*True

use = np.where(inside == True)[0]
    
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
N_cells = len(R.flatten()[use])
outFile = radPath + "P_RZ_39231_interpolated_400pts_box.csv"
pc = np.zeros((N_cells, 3))
pc[:,0] = R.flatten()[use]#*1000.0 #convert to mm
pc[:,1] = Z.flatten()[use]#*1000.0
pc[:,2] = P.flatten()[use]
head = "R[m],Z[m],P[MW]"
np.savetxt(outFile, pc, delimiter=',',fmt='%.10f', header=head)


#save X,Y,Z,P for paraview
xyzFile = radPath + 'P_xyz_39231_interpolated_400pts_box.csv'
phi = 0.0 #toroidal angle
pc = np.zeros((N_cells, 4))
pc[:,0] = R.flatten()[use]*1000.0 #convert to mm
pc[:,2] = Z.flatten()[use]*1000.0
pc[:,3] = P.flatten()[use]
head = "X[m],Y[m],Z[m],P[MW]"
np.savetxt(xyzFile, pc, delimiter=',',fmt='%.10f', header=head)
