#sPolFromRZ.py
#Description:   Calculates Spol for RZ coordinates of machine wall
#Date:          20220909
#engineer:      T Looby
import numpy as np
import sys
import os
import shutil
import scipy.interpolate as scinter
from scipy.interpolate import interp1d

rootPath = '/home/tlooby/HEATruns/SPARC/sweepMEQ_T4/'
name = 'v3b.csv'
f = rootPath + name

# Calculate distance along curve/wall (also called S):
def distance(rawdata):
    distance = np.cumsum(np.sqrt(np.sum(np.diff(rawdata,axis=0)**2,axis=1)))
    distance = np.insert(distance, 0, 0)
    return distance

#read file
RZ = np.genfromtxt(f, comments='#', delimiter=',')

#calculate distance, S
S = distance(RZ)

for i,row in enumerate(S):
    print("{:.6f}, {:.6f}, {:.6f},".format(RZ[i,0], RZ[i,1], row))
