#reads an Elmer .vtu file and calculates the principal stresses by
#solving the eigenvalue problem.  Saves the max principal out to 
#a csv file
import numpy as np
import os
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import csv

# Path to the input .vtu file and output .csv file
rootDir = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stressReX_lq1.2_S0.6_fRadDiv90/elmer/'
#read all files with a prefix
prefix = 'case'
nombres = sorted([f for f in os.listdir(rootDir) if (os.path.isfile(os.path.join(rootDir, f)) and prefix in f)])
output_csv_file = rootDir + 'maxPrincipal.csv'

maxPrincipal = []

for n in nombres:
    # Read the .vtu file
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(rootDir + n)
    reader.Update()
    # Get the stress tensor components from the .vtu file
    data = reader.GetOutput()
    stress_xx = vtk_to_numpy(data.GetPointData().GetArray('stress_xx'))
    stress_yy = vtk_to_numpy(data.GetPointData().GetArray('stress_yy'))
    stress_zz = vtk_to_numpy(data.GetPointData().GetArray('stress_zz'))
    stress_xy = vtk_to_numpy(data.GetPointData().GetArray('stress_xy'))
    stress_xz = vtk_to_numpy(data.GetPointData().GetArray('stress_xz'))
    stress_yz = vtk_to_numpy(data.GetPointData().GetArray('stress_yz'))
    stress = np.zeros((len(stress_xx),3,3))
    stress[:,0,0] = stress_xx
    stress[:,0,1] = stress_xy
    stress[:,0,2] = stress_xz
    stress[:,1,0] = stress_xy
    stress[:,1,1] = stress_yy
    stress[:,1,2] = stress_yz
    stress[:,2,0] = stress_xz
    stress[:,2,1] = stress_yz
    stress[:,2,2] = stress_zz
    eigenvalues, eigenvectors = np.linalg.eig(stress)
    maxPrincipal.append(np.max(eigenvalues))
    print(n + ": MaxPrincipal: {:f}".format(maxPrincipal[-1]))

arr = np.zeros((len(maxPrincipal), 2))
arr[:,0] = np.arange(len(maxPrincipal))
arr[:,1] = maxPrincipal
np.savetxt(output_csv_file, arr, delimiter=',', comments="",  header="Time,maxprincipal[Pa]")