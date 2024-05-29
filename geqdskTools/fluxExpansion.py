#calculates poloidal flux expansion from equilibria
#user provides divertor line segment and the poloidal flux expansion
#between omp and that line segment is calculated using 3 methods
#total flux expansion is also calculated

import numpy as np
import sys
import os
import shutil
import scipy.interpolate as scinter

EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

N=100

omp = np.array([[2.38,0.0], [2.42, 0.0]])
tgt = np.array([[1.57,-1.297],[1.72, -1.51]])

rootPath = '/home/tlooby/HEATruns/SPARC/axisymmetric/sparc/'
g = 'sparc_1718.EQDSK_PsiOver2pi_negIp_negBt_negFpol'

f = rootPath + g

try:
    f = rootPath+g
    MHD = MHDClass.setupForTerminalUse(gFile=f)
    ep = MHD.ep
except: #EFIT reader is very specific about shot names
    newf = rootPath+'g000001.00001'
    shutil.copyfile(f, newf)
    MHD = MHDClass.setupForTerminalUse(gFile=newf)
    ep = MHD.ep


# Calculate distance along curve/wall (also called S):
def distance(rawdata):
    distance = np.cumsum(np.sqrt(np.sum(np.diff(rawdata,axis=0)**2,axis=1)))
    distance = np.insert(distance, 0, 0)
    return distance

def normals(rawdata):
    N = len(rawdata) - 1
    norms = np.zeros((N,3))
    for i in range(N):
        RZvec = rawdata[i+1] - rawdata[i]
        vec1 = np.array([[RZvec[0], 0.0, RZvec[1]]])
        vec2 = np.array([[0.0, 1.0, 0.0]])
        n = np.cross(vec1, vec2)
        norms[i,:] = n / np.linalg.norm(n,axis=1)
    return norms

def centers(rz):
    centers = np.zeros((len(rz)-1, 2))
    dR = np.diff(rz[:,0])
    dZ = np.diff(rz[:,1])
    centers[:,0] = rz[:-1,0] + dR/2.0
    centers[:,1] = rz[:-1,1] + dZ/2.0
    return centers

    
#Equilibrium quantities from EQDSK at target
R_tgt = np.linspace(tgt[0,0], tgt[1,0], N)
Z_tgt = np.linspace(tgt[0,1], tgt[1,1], N)
tgt2 = np.vstack([R_tgt, Z_tgt]).T
dist_tgt2 = distance(tgt2)
ctrs = centers(tgt2)
dist_tgt = distance(ctrs)
norms_tgt = np.delete(normals(tgt2), 1, axis=1)
Brz_tgt = np.zeros((ctrs.shape))
Brz_tgt[:,0] = ep.BRFunc.ev(ctrs[:,0], ctrs[:,1])
Brz_tgt[:,1] = ep.BZFunc.ev(ctrs[:,0], ctrs[:,1])
Bt_tgt = ep.BtFunc.ev(ctrs[:,0], ctrs[:,1])
psiN_tgt = ep.psiFunc.ev(ctrs[:,0], ctrs[:,1])
psiN_tgt2 = ep.psiFunc.ev(tgt2[:,0], tgt2[:,1])
Bp_tgt = np.sqrt(Brz_tgt[:,0]**2 + Brz_tgt[:,1]**2)
B_tgt = np.sqrt(Brz_tgt[:,0]**2 + Brz_tgt[:,1]**2 + Bt_tgt**2)
brz_tgt = Brz_tgt / Bp_tgt[:, np.newaxis]


#Equilibrium quantities from EQDSK at midplane
#map this surface back to midplane
R = np.linspace(ep.g['RmAxis'], ep.g['R1'] + ep.g['Xdim'], N)
Z = np.zeros(len(R)) + ep.g['ZmAxis']
p = ep.psiFunc.ev(R,Z)
#In case of monotonically decreasing psi, sort R, p so that p is
#monotonically increasing
points = zip(R, p)
points = sorted(points, key=lambda point: point[1]) # Sort list of tuples by p-value (psi)
R, p = zip(*points)
f = scinter.UnivariateSpline(p, R, s = 0, ext = 'const') # psi outside of spline domain return the boundary value
R_omp = f(psiN_tgt2)
Z_omp = np.zeros((len(R_omp)))# + ep.g['ZmAxis']
omp = np.vstack([R_omp, Z_omp]).T
dist_omp = distance(omp)
norm_omp = normals(omp)

#calculate gradients
dPsi = np.diff(psiN_tgt2)
dS_omp = np.diff(dist_omp)
grad_omp = dPsi / dS_omp

dS_tgt = np.diff(dist_tgt2)
grad_tgt = dPsi / dS_tgt
gradRatio = grad_omp / grad_tgt
bpdotn = np.multiply(brz_tgt, norms_tgt).sum(1)

alpha = np.arccos(bpdotn)
beta = np.pi - alpha
fx = gradRatio * np.cos(beta)
#fx = np.cos(beta) * dS_tgt / dS_omp
lcfsIdx = np.argmin(np.abs(psiN_tgt - 1.0))
#print("Flux Expansion Array:")
#print(fx)
print("Average fx: {:f}".format(np.average(fx)))
print("fx at LCFS (psiN={:f}): {:f}".format(psiN_tgt[lcfsIdx],fx[lcfsIdx]))


#check using matt's formula from CALC
#B field from MHD Equilibrium at OMP
#R_omp = np.linspace(omp[0,0], omp[1,0], 99)
#Z_omp = np.linspace(omp[0,1], omp[1,1], 99)
omp2 = np.vstack([R_omp, Z_omp]).T
Brz_omp = np.zeros((len(R_omp), 2))
Brz_omp[:,0] = ep.BRFunc.ev(R_omp,Z_omp)
Brz_omp[:,1] = ep.BZFunc.ev(R_omp,Z_omp)
Bt_omp = ep.BtFunc.ev(R_omp,Z_omp)
B_omp = np.sqrt(Brz_omp[:,0]**2 + Brz_omp[:,1]**2 + Bt_omp**2)
psiN_omp = ep.psiFunc.ev(R_omp,Z_omp)
Bp_omp = np.sqrt(Brz_omp[:,0]**2 + Brz_omp[:,1]**2)
lcfsIdx_omp = np.argmin(np.abs(psiN_omp - 1.0))
fx_calc = (Bp_omp[lcfsIdx] / Bp_tgt[lcfsIdx]) * (R_omp[lcfsIdx] / ctrs[lcfsIdx,0]) * (1 / np.abs((bpdotn[lcfsIdx])))
print("From CALC doc (broken), fx = {:f}".format(fx_calc))
#
# Note:
#that calc is broken and i think the CALC document is incorrect
#for reference, i think matt uses this equation to calculate fx
#at outer tgt: (2.83*2.41)/(13.0*1.73) * 1/(np.sin(np.radians(0.73)))
#so the errors are: 1) using B_tot in denominator
#                   2) using total angle of incidence in denominator, not poloidal
#                   3) using sin instead of cos (sin is project of field into surface, not along gradB)
#
#
# see Himank's paper: "Plasma flux expansion control on the DIII-D tokamak" for a good description
#
#|grad(Psi)| = |dPsi/dr| = Bp * R
#so dPsi = Bp * R * dr
#flux expansion is the ration of dr's at two locations between the same two flux surfaces.  
#so dPsi_omp = dPsi_tgt
#for omp and tgt we have:
# dPsi_tgt / dPsi_omp = 1 = (dr_tgt * Bp_tgt * R_tgt) / (dr_omp * Bp_omp * Bp_omp) 
#rearragning yields:
# fx = dr_tgt / dr_omp = (Bp_omp * R_omp) / (Bp_tgt * R_tgt)
#so NO thetaHat dot nHat like in the CALC doc!
#this matches the previos fx result
fx_himank = (Bp_omp[lcfsIdx] / Bp_tgt[lcfsIdx]) * (R_omp[lcfsIdx] / ctrs[lcfsIdx,0]) 
print("From Himank's paper, fx = {:f}".format(fx_himank))



#total flux expansion
fx_total = fx[lcfsIdx] * B_tgt[lcfsIdx] / B_omp[lcfsIdx_omp]
print("Total fx at psiN=1: {:f}".format(fx_total))

#for matching to HEAT
#R1 = f(1.0)
#R2 = f(1.0033)
#dR = R2-R1
#dS = 53*1e-3
#print(dS / dR * np.cos(beta[lcfsIdx]))


#import plotly.graph_objects as go
#fig = go.Figure()
#fig.add_trace(go.Scatter(x=tgt[:,0], y=tgt[:,1]))
#normVec = np.array([ctrs[lcfsIdx],ctrs[lcfsIdx]+norms_tgt[lcfsIdx]*0.1])
#fig.add_trace(go.Scatter(x=normVec[:,0], y=normVec[:,1]))
#bVec = np.array([ctrs[lcfsIdx],ctrs[lcfsIdx] + brz_tgt[lcfsIdx]])
#fig.add_trace(go.Scatter(x=bVec[:,0], y=bVec[:,1]))
#fig.update_yaxes(scaleanchor = "x",scaleratio = 1,)
#fig.show()