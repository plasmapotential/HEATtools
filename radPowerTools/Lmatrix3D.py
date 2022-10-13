import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, LinearNDInterpolator

radFile = '/home/tom/source/dummyOutput/RZ_SOLPS.csv'
glyphFile = '/home/tom/source/dummyOutput/glyph.csv'

ctr = np.array([1.657,0.008,-1.42]) #[m]
norm = np.array([0.0,0.0,1.0])
pt1 = np.array([1.657,0.02,-1.42])



lMax = 1.0 #[m]
Na = 1 #ranges from 0,pi/2
Nb = 1 #ranges from 0,2pi
Nl = 10

#read radiation R,Z,P file
PC2D = pd.read_csv(radFile, header=0, names=['R','Z','P']).values #convert to m
#build 2D interpolator
f_PC = LinearNDInterpolator(PC2D[:,0:2],PC2D[:,2], fill_value=0)

#build local coordinate system
W = norm
U = pt1-ctr
V = np.cross(W,U)
u = U / np.linalg.norm(U)
v = V / np.linalg.norm(V)
w = W / np.linalg.norm(W)
uvw = np.vstack([u,v,w])
#print(u)
#print(v)
#print(w)
#print(uvw)

#discretize the half hemisphere along w in bin centers
pdf_a = lambda x: np.sin(x)/2.0
a = np.linspace(0,np.pi,100000)
alpha = pdf_a(a)
cdf_a = np.cumsum(alpha[1:])*np.diff(a)
cdf_a = np.insert(cdf_a, 0, 0)
cdfBounds_a = np.linspace(0,cdf_a[-1],Na+1)
cdfSlices_a = np.diff(cdfBounds_a)/2.0 + cdfBounds_a[:-1]
inverseCDF = interp1d(cdf_a, a, kind='linear')
aSlices = inverseCDF(cdfSlices_a)
#beta
# alpha
pdf_b = lambda x: [1.0 for i in x]
b = np.linspace(0,np.pi,100000) #only half hemisphere
beta = pdf_b(b)
cdf_b = np.cumsum(beta[1:])*np.diff(b)
cdf_b = np.insert(cdf_b, 0, 0)
cdfBounds_b = np.linspace(0,cdf_b[-1],Nb+1)
cdfSlices_b = np.diff(cdfBounds_b)/2.0 + cdfBounds_b[:-1]
inverseCDF = interp1d(cdf_b, b, kind='linear')
bSlices = inverseCDF(cdfSlices_b)

#print(np.degrees(aSlices))
#print(np.degrees(bSlices))

#create rays of length l in the direction of each bin center
rays_xyz = np.zeros((Na,Nb,3))
for i,a in enumerate(aSlices):
    for j,b in enumerate(bSlices):
#    uRay = lMax * np.sin(aSlices) * np.cos(b)
#    vRay = lMax * np.sin(aSlices) * np.sin(b)
#    wRay = lMax * np.cos(aSlices)

        uRay = lMax * np.cos(a) * np.sin(b)
        vRay = lMax * np.cos(a) * np.cos(b)
        wRay = lMax * np.sin(a)

        rays_uvw = np.array([uRay,vRay,wRay])
        rays_xyz[i,j,:] = np.matmul(rays_uvw, uvw)


#calculate ray end points
rayEnd = rays_xyz + ctr
rays = rays_xyz.reshape(Na*Nb,3)


#integrate along each ray
lNorm = np.linspace(0, 1, Nl)

#step through l
em = np.zeros((Na*Nb))
for i,lN in enumerate(lNorm):
    if i==0:
        continue
    else:
        lPt = ctr + lN*rays
        print(rays)
        print(lPt)
        r = np.sqrt(lPt[:,0]**2+lPt[:,1]**2)
        z = lPt[:,2]
        em += f_PC(r,z)

print(em)
r = rays_xyz.reshape(Na*Nb,3)
pc = np.zeros((Na*Nb, 6))
pc[:,0] = ctr[0]*1000.0
pc[:,1] = ctr[1]*1000.0
pc[:,2] = ctr[2]*1000.0
pc[:,3] = r[:,0]*1000.0
pc[:,4] = r[:,1]*1000.0
pc[:,5] = r[:,2]*1000.0
head = "X,Y,Z,vx,vy,vz"
np.savetxt(glyphFile, pc, delimiter=',',fmt='%.10f', header=head)

#(iHat*vx) + (jHat*vy) + (kHat*vz)
