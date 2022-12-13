#calculatePowerTSC.py
#description:  example script that loads TSC data, then calculates plasma power
#              uses radial current density and Spitzer resistivity
#date:          Nov 2021
#engineer:      T Looby
import numpy as np
from scipy.interpolate import interp1d
import scipy.integrate as integrate
import tscClass

#TSC outputa file
f = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/outputaV2h01a'
#read the file and get some profiles
tsc = tscClass.tscIO(f)
tsc.readRhoProfile()
tsc.readRadialTprofiles()
tsc.readRadialCurrentProfiles()
tsc.readTimeSteps()
tsc.readRminor()
tsc.readRadii()

#various constants
Zeff = 1.0
kB = 8.617e-5 #ev/K
e = 1.602e-19 # C
c = 299792458 #m/s


#idx used to select which TSC timestep we are looking at
idx = 8
#normalized radial coordinate
rho = tsc.rho[idx]
#Temperature
T = tsc.Te[idx]
#Current density
J = tsc.J[idx]
#minor radius
rMinor = tsc.rMinor[idx]

#interpolators (not used currently, left for reference)
#Tinterp = interp1d(rho, T)
#Jinterp = interp1d(rho, J)
#rhoNew = np.linspace(min(rho),max(rho), 1000)
#Tnew = Tinterp(rhoNew)
#Jnew = Jinterp(rhoNew)

#calculate area of each current shell
A = []
for i in range(len(J)-1):
    A.append( np.pi*(rMinor[i+1]**2 - rMinor[i]**2) )
A = np.array(A)

#calculate approximate Spitzer resistivity, assuming Coulomb logarithm = 17
CoulLog = 17
spitz = 0.53e-4 * CoulLog * T**(-3.0/2.0)
#spitz = 2.8e-8 *(T*1e-3)**(-3.0/2.0)

#ohms
R = spitz[:-1] * 2*np.pi*tsc.r0[idx] / A
#print(R)

#ohms law
P = (J[:-1]*A)**2 * R

print("Integrated power: {:f} [W]".format(np.sum(P)))
print("Integrated current: {:f} [A]".format(np.sum(J[:-1]*A)))
print(tsc.ts)
print("Complete")

#write a csv file with the J(r) profile
profFile = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/J_8710ms.csv'
arr = np.vstack([tsc.rMinor[idx], tsc.J[idx]]).T
head = "rMinor[m],J[A/m^2]"
np.savetxt(profFile, arr, delimiter=",", header=head)
