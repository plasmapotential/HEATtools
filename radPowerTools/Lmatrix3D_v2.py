import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, LinearNDInterpolator

radFile = '/home/tom/source/dummyOutput/RZpower.csv'
glyphFile = '/home/tom/source/dummyOutput/glyph.csv'

ctr = np.array([1.657,0.008,-1.42]) #[m]
norm = np.array([1.0, 0.0, 0.0])
pt1 = np.array([1.657,0.02,-1.42])
Na = 1 #ranges from 0,pi
Nb = 1 #ranges from 0,pi
phi = 0.0

#read 2D radiation R,Z,P file
#PC2D = pd.read_csv(radFile, header=0, names=['R','Z','P']).values #convert to m
PC2D = np.array([[1.67,0.008,-1.42]])

Ni = len(PC2D)
Nj = Na*Nb
#calculate 3D coordinates at phi
radXYZ  = np.zeros((Ni,3))
radXYZ[:,0] = PC2D[:,0] * np.cos(phi)
radXYZ[:,1] = PC2D[:,1] * np.sin(phi)
radXYZ[:,2] = PC2D[:,2]

#build 2D interpolator
#f_PC = LinearNDInterpolator(PC2D[:,0:2],PC2D[:,2], fill_value=0)

#build local coordinate system
W = norm
U = pt1-ctr
V = np.cross(W,U)
u = U / np.linalg.norm(U)
v = V / np.linalg.norm(V)
w = W / np.linalg.norm(W)
uvw2xyz = np.vstack([u,v,w])
#print(u)
#print(v)
#print(w)
#print(uvw2xyz)

#discretize the half hemisphere along w in bin centers
pdf_a = lambda x: np.sin(x)/2.0 #normalized angle pdf
a = np.linspace(0,np.pi,100000)
alpha = pdf_a(a)
cdf_a = np.cumsum(alpha[1:])*np.diff(a)
cdf_a = np.insert(cdf_a, 0, 0)
cdfBounds_a = np.linspace(0,cdf_a[-1],Na+1)
cdfSlices_a = np.diff(cdfBounds_a)/2.0 + cdfBounds_a[:-1]
inverseCDF_a = interp1d(cdf_a, a, kind='linear')
aSlices = inverseCDF_a(cdfSlices_a)
aBounds = inverseCDF_a(cdfBounds_a)
#beta
# alpha
pdf_b = lambda x: [1.0/np.pi for i in x] #normalized angle PDF
b = np.linspace(0,np.pi,100000) #only half hemisphere
beta = pdf_b(b)
cdf_b = np.cumsum(beta[1:])*np.diff(b)
cdf_b = np.insert(cdf_b, 0, 0)
cdfBounds_b = np.linspace(0,cdf_b[-1],Nb+1)
cdfSlices_b = np.diff(cdfBounds_b)/2.0 + cdfBounds_b[:-1]
inverseCDF_b = interp1d(cdf_b, b, kind='linear')
bSlices = inverseCDF_b(cdfSlices_b)
bBounds = inverseCDF_b(cdfBounds_b)

#print(np.degrees(aSlices))
#print(np.degrees(bSlices))
print(np.degrees(aBounds))
print(np.degrees(bBounds))
#print(cdfBounds_a)
#print(cdfBounds_b)


#calculate distance from ctr to each source object
vec = radXYZ - ctr
l = np.linalg.norm(vec, axis=1)
UVW = np.matmul(vec, uvw2xyz.T)

#calculate which half hemisphere cell the ray from ctr to each rad pt is in
angles = np.zeros((Ni,Nj,2))
for i in range(Ni):
    u0 = np.round(UVW[i,0], 8)
    v0 = np.round(UVW[i,1], 8)
    w0 = np.round(UVW[i,2], 8)
    #alpha
    angles[i,:,0] = np.round(np.arcsin(w0), 8)
    #beta
    angles[i,:,1] = np.round(np.arcsin( v0 / np.cos(angles[i,:,0]) ), 8)
#print(angles)
#print(np.degrees(angles))

#now calculate L matrix
L = np.zeros((Ni,Nj))
for i in range(Ni):
    for j in range(Nj):
        #alpha
        for k in range(len(aBounds)-1):
            #check if ray is inside this j
            if (angles[i,j,0] >= aBounds[k]) and (angles[i,j,0] <= aBounds[k+1]):
                aFlag = True
            else:
                aFlag = False
        #beta
        for k in range(len(bBounds)-1):
            #check if ray is inside this j
            if (angles[i,j,1] >= bBounds[k]) and (angles[i,j,1] <= bBounds[k+1]):
                bFlag = True
            else:
                bFlag = False
        if aFlag == True and bFlag == True:
            L[i,j] = l[i]
            
#scale to account for fractional component of solid angle
L *= 2*np.pi / Nj

print(L)

#now you need to scale by fractional solid angle
