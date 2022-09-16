#script for printing various quantities related to the gFile.  can
#be used to test if gFile psiRZ is normalized by using Ampere's Law

import sys
from scipy import interpolate
import numpy as np
EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

gFilePath = '/home/tom/HEATruns/SPARC/fishScale/sparc/g000001.00001'
ep = MHDClass.setupForTerminalUse(gFile=gFilePath).ep


#R=0.621875
#location of OMP separatrix
R=2.43
Z = 0.0
kappa = 1.75
Raxis = ep.g['RmAxis']
a = R - Raxis

Bp = ep.BpFunc.ev(R,Z)
Bt = ep.BtFunc.ev(R,Z)
psi1 = ep.psiFunc.ev(R,Z)




Ip = ep.g['Ip']
mu = 4*np.pi*10**-7
Bp1 = mu * Ip / (2*np.pi*a)
print("Bp [T] calculated @R using Ampere's Law:".format(R))
print(Bp1)
print("Bp [T] calculated @R from gfile:")
print(Bp)

print("TEST")
print(ep.g['Bt0'])
print(ep.g['Fpol'][-1] / R)
print(Bt)
print(ep.g['Bt0']*Raxis/R)
print(a)
print(ep.g['RmAxis'])


psi = ep.g['psi']
q = ep.g['q']
f = interpolate.interp1d(psi,q)
q1 = f(psi1)
q1_calc = (a * Bt) / (R * Bp)

qStar = 2*np.pi*a**2*kappa*ep.g['Bt0'] / (mu * ep.g['RmAxis'] * ep.g['Ip'])

print("\nq95 calculated from gfile:".format(R))
print(f(0.95))
print("q calculated @R from gfile:".format(R))
print(q1)
print("q calculated @R from Ip and Bt:")
print(q1_calc)
print("q* calculated @R from Ip and Bt:")
print(qStar)

# For putting in a google slide / Latex:
#Bp = \frac{\mu_0 I_p}{2 \pi a} = \frac{(4 \pi \times 10^{-7} \text{T m/A}) (2 \text{MA}) }{2 \pi (0.12726 \text{m})} = 3.1433 \text{ T}
#q = \frac{aB_t}{RB_p} = \frac{(0.12726 \text{m}) (2.1137 \text{T})}{(0.621875 \text{m})(0.72173 \text{T})} = 0.5993
