#Lmatrix3D.py
#Description:   Builds Reinke's L-matrix in 3D from 1 target pt and RZ emmision
#               grid points. Samples uniformly in solid angle over half hemishpere
#               normal to mesh triangle face
#Engineer:      T Looby
#Date:          20221014
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, LinearNDInterpolator

#input file with RZ coordinates of mesh grid centers in columns 0,1
radFile = '/home/tom/source/dummyOutput/RZpower.csv'
#file for saving glyphs to visualize rays in paraview
glyphFile = '/home/tom/source/dummyOutput/glyph.csv'
#file for saving L matrix
LmatFile = '/home/tom/source/dummyOutput/Lmatrix.csv'
#point where we are calculating the flux
ctr = np.array([1.657,0.0,-1.42]) #[m]
#normal vector of the face on which we calculate flux
norm = np.array([1.0, 0.0, 0.0])
#another point on the face
pt1 = np.array([1.657,0.02,-1.42])
#number of samples in alpha, ranges from (0,pi), polar angle
Na = 5 #ranges from 0,pi
#number of samples in beta, ranges from (0,pi), azimuthal angle
Nb = 5 #ranges from 0,pi
#toroidal location of the RZ emission grid [degrees]
phi = 0.0

#various objects that can be saved
saveBinCtrRays = False #each bin ctr
saveSrcTgtRays = False #source to target vectors
saveLmatrix = True #save L matrix in ixj csv file


#read 2D radiation R,Z,P file
#PC2D = pd.read_csv(radFile, header=0, names=['R','Z','P']).values #convert to m
#for testing, a user defined point
PC2D = np.array([[3.0, -1.7], [2.0, -0.5], [3.0, -1.4]])

Ni = len(PC2D)
Nj = Na*Nb

#calculate 3D coordinates at phi
radXYZ  = np.zeros((Ni,3))
radXYZ[:,0] = PC2D[:,0] * np.cos(np.radians(phi))
radXYZ[:,1] = PC2D[:,0] * np.sin(np.radians(phi))
radXYZ[:,2] = PC2D[:,1]

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
#alpha: polar angle, ranges from (0,pi), pi/2 points along face normal
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
#beta: azimuthal angle, ranges from (0,pi)
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
print("bounds")
print(np.degrees(aBounds))
print(np.degrees(bBounds))
#print(cdfBounds_a)
#print(cdfBounds_b)

#calculate distance from ctr to each source object
vec = radXYZ - ctr
l = np.linalg.norm(vec, axis=1)
UVW = np.matmul(vec, uvw2xyz.T)

print("vectors")
print(vec)
print(UVW)
#calculate angles to source points
angles = np.zeros((Ni,2))
for i in range(Ni):
    u0 = np.round(UVW[i,0], 8)
    v0 = np.round(UVW[i,1], 8)
    w0 = np.round(UVW[i,2], 8)
    l0 = np.sqrt(u0**2+v0**2+w0**2)
    u0 /= l0
    v0 /= l0
    w0 /= l0

    #alpha
    angles[i,0] = np.round(np.arcsin(w0), 8)
    if v0 < 0:
        angles[i,0] += np.pi/2.0
    #beta
    angles[i,1] = np.round(np.arccos( np.round(u0 / np.cos(angles[i,0]), 8) ), 8)

print("angles")
#print(angles)
print(np.degrees(angles))

#calculate L matrix
L = np.zeros((Ni,Nj))
angleMap = np.zeros((Nj,2)) #keeps track of angles as a function of j
for i in range(Ni):
    jIdx=0
    #we loop thru j by looping through alpha and beta
    for j1 in range(Na):
        aLo = aBounds[j1]
        aHi = aBounds[j1+1]
        if angles[i,0] >= aLo and angles[i,0] <= aHi:
            aFlag = True
        else:
            aFlag = False
        for k in range(Nb):
            bLo = bBounds[k]
            bHi = bBounds[k+1]
            if angles[i,1] >= bLo and angles[i,1] <= bHi:
                bFlag = True
            else:
                bFlag = False

            if aFlag != False and bFlag != False:
                L[i,jIdx] = l[i]

            #map angles back to j (where Nj=Na*Nb)
            angleMap[jIdx,0] = aSlices[j1]
            angleMap[jIdx,1] = bSlices[k]
            jIdx+=1

#scale to account for fractional component of solid angle
#because we sampled uniformly in solid angle all bins have equal weight, dOmega
#we also divide normalize to entire solid angle, 4pi
#remember that we only sampled from half hemisphere (normal to mesh face)
dOmega = 2*np.pi / Nj
L *= dOmega / (4 * np.pi)

print("L matrix")
print(L)
print(L.shape)

#create rays of length l in the direction of each bin center
if saveBinCtrRays == True:
    rays_xyz = np.zeros((Na,Nb,3))
    for i,a in enumerate(aSlices):
        for j,b in enumerate(bSlices):
            uRay = max(l) * np.cos(a) * np.cos(b)
            vRay = max(l) * np.cos(a)
            wRay = max(l) * np.sin(a) * np.sin(b)
            rays_uvw = np.array([uRay,vRay,wRay])
            rays_xyz[i,j,:] = np.matmul(rays_uvw, uvw2xyz)

    #save bin center rays to CSV
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
    print("Saved glyphs of bin centers")

#create rays between source and target points
if saveSrcTgtRays == True:
    rays_xyz = np.zeros((Ni,3))
    for i in range(Ni):
        uRay = l[i] * np.cos(angles[i,0]) * np.cos(angles[i,1])
        vRay = l[i] * np.cos(angles[i,0])
        wRay = l[i] * np.sin(angles[i,0]) * np.sin(angles[i,1])
        rays_uvw = np.array([uRay,vRay,wRay])
        rays_xyz[i,:] = np.matmul(rays_uvw, uvw2xyz)
    #save vectors to source points to CSV
    r = rays_xyz.reshape(Ni,3)
    pc = np.zeros((Ni, 6))
    pc[:,0] = ctr[0]*1000.0
    pc[:,1] = ctr[1]*1000.0
    pc[:,2] = ctr[2]*1000.0
    pc[:,3] = r[:,0]*1000.0
    pc[:,4] = r[:,1]*1000.0
    pc[:,5] = r[:,2]*1000.0
    head = "X,Y,Z,vx,vy,vz"
    np.savetxt(glyphFile, pc, delimiter=',',fmt='%.10f', header=head)
    print("Saved glyphs of angles to sources")

#use this command in Paraview calculator to view glyphs
#(iHat*vx) + (jHat*vy) + (kHat*vz)

if saveLmatrix == True:
    np.savetxt(LmatFile, L, delimiter=',', fmt='%.10f')
    print("Saved L matrix to ixj CSV file")
