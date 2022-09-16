#ST40gfile.py
#Description:   Writes gfile from ST40 matlab file
#Engineer:      T Looby
#Date:          20191206

import os
import numpy as np
import scipy.io
import scipy.integrate as integ
import scipy.interpolate as interp
import matplotlib.pyplot as plt

matlab_file = '/u/tlooby/ST40/eq_0002_export.mat'
gpath = '/u/tlooby/ST40/'
mat = scipy.io.loadmat(matlab_file)
writeMask = True
plotMask = False

#These are all defined in the MATLAB file
r = mat['r'][0]
z = mat['z'][0]
psiRZ = mat['psi']
psiAxis = mat['psi_a'][0][0]
psiSep = mat['psi_b'][0][0]
RmAxis=mat['mag_axis'][0][0]
ZmAxis=mat['mag_axis'][0][1]
xpoints = mat['xpoints']
psiN1D = mat['f_profile'][0]
Fpol = mat['f_profile'][1]
qpsi = mat['q_profile'][1]
Bvacrad = mat['b_vacuum_radius'][0][0]
Bt0 = mat['b_vacuum_magnitude'][0][0]
lcfs = mat['lcfs_polygon']
rlim = mat['R_limits'][0]
zlim = mat['Z_limits'][0]

#These we derive from what came out of the matlab file
R,Z = np.meshgrid(r,z)
wall = np.vstack((rlim, zlim)).T
Nwall = len(rlim)
Nr = len(r)
Nz = len(z)
R1 = min(r)
Xdim = max(r) - min(r)
Zdim = max(z) - min(z)
R0 = Xdim / 2.0
Zmid = Zdim / 2.0
Nlcfs = len(lcfs[0])
psi1D = psiN1D * (psiSep - psiAxis) + psiAxis
psiN2D = (psiRZ - psiAxis) / (psiSep - psiAxis)
Fprime = np.diff(Fpol) / np.diff(psi1D)

#Interpolate the first point in FFprime
deltaFp = Fprime[0] - Fprime[1]
Fp0 = deltaFp + Fprime[0]
FFprime = np.insert(Fprime,0,Fp0) * Fpol

#These we don't have so we just write arbitrary values in
KVTOR = 0
RVTOR = 0
NMASS = 0
RHOVN = np.zeros((Nr))
Ip = 1.0
Pprime = np.zeros((Nr))
Pres = np.ones((Nr))

if plotMask:
    print(FFprime)
    plt.plot(FFprime, label='FFprime')
    plt.plot(psi1D, label='psi')
    plt.plot(Fpol, label='Fpol')
    plt.legend()
    plt.show()


# Writing to match J. Menard's idl script
# in /u/jmenard/idl/efit/efit_routines_jem.pro
# Scale FFprime, Pprime, psiRZ, qpsi, Ip, psiSep, psiAxis,
# per the AUTO keyword in J. Menard's function, 'rescale_gstructures'
#       -From the Menard script line 395:
# "This function re-scales the poloidal flux to be consistent with the
# specified sign of Ip, where Ip is the toroidal component of the plasma
# current in cylindrical coordinates, i.e. + --> C.C.W. as viewed from
# above.  Note that in the re-definition of q, the theta flux coordinate
# is C.C.W. in the poloidal plane, so that if Ip > 0 and Bt > 0, q will
# be negative, since then B.grad(theta) < 0."

dsign = np.sign(Ip)
gsign = np.sign( -(psiSep - psiAxis) )
qsign = np.sign(Fpol[-1]) #F_edge sign
FFprime *= dsign*gsign
Pprime *= dsign*gsign
psiRZ *= dsign*gsign
qpsi *= -qsign*dsign
Ip *= dsign
psiSep *= dsign*gsign
psiAxis *= dsign*gsign


# --- _write_array -----------------------
# write numpy array in format used in g-file:
# 5 columns, 9 digit float with exponents and no spaces in front of negative numbers
def write_array(x, f):
    N = len(x)
    rows = int(N/5)  # integer division
    rest = N - 5*rows
    for i in range(rows):
        for j in range(5):
                f.write('% .9E' % (x[i*5 + j]))
        f.write('\n')
    if(rest > 0):
        for j in range(rest):
                f.write('% .9E' % (x[rows*5 + j]))
        f.write('\n')



shot = 2
time = 500
# Now, write to file using same style as J. Menard script (listed above)
# Using function in WRITE_GFILE for reference

if writeMask:
    with open(gpath + 'g' + format(shot, '06d') + '.' + format(time,'05d'), 'w') as f:
        f.write('  EFITD    xx/xx/xxxx    #' + str(shot) + '  ' + str(time) + 'ms        ')
        f.write('   3 ' + str(Nr) + ' ' + str(Nz) + '\n')
        f.write('% .9E% .9E% .9E% .9E% .9E\n'%(Xdim, Zdim, R0, R1, Zmid))
        f.write('% .9E% .9E% .9E% .9E% .9E\n'%(RmAxis, ZmAxis, psiAxis, psiSep, Bt0))
        f.write('% .9E% .9E% .9E% .9E% .9E\n'%(Ip, psiAxis, 0, RmAxis, 0))
        f.write('% .9E% .9E% .9E% .9E% .9E\n'%(ZmAxis,0,psiSep,0,0))
        write_array(Fpol, f)
        write_array(Pres, f)
        write_array(FFprime, f)
        write_array(Pprime, f)
        write_array(psiRZ.flatten(), f)
        write_array(qpsi, f)
        f.write(str(Nlcfs) + ' ' + str(Nwall) + '\n')
        write_array(lcfs.flatten(), f)
        write_array(wall.flatten(), f)
        f.write(str(KVTOR) + ' ' + format(RVTOR, ' .9E') + ' ' + str(NMASS) + '\n')
        write_array(RHOVN, f)
