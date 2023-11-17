#makeGEQDSKimages.py
#Description:   makes a series of images from a series of user supplied GEQDSKs
#Date:          20220831
#engineer:      T Looby
#
#how to build a sweep using vSweep, turntime, and geqdsks
#1) run SpolFromVelocity.py to define SP trajectory
#2) run sweepInterpolator.py to interpolate GEQDSKs along SP trajectory
#3) run makeGEQDSKimages.py to generate .pngs of each sweep step

import numpy as np
import pandas as pd
import sys
import os
import shutil
import scipy.interpolate as scinter
from scipy.interpolate import interp1d
import plotly.graph_objects as go

#rocinante
EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
#CFS machine
#EFITPath = '/home/tlooby/source'
#HEATPath = '/home/tlooby/source/HEAT/github/source'

sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass
import GUIscripts.plotly2DEQ as pEQ

#rootPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/interpolated_25ms/'
#outPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/EQplots/'
#rootPath = '/home/tlooby/projects/VDEs/GEQDSKs_wide_120ms/paraview_q95/'
#outPath = '/home/tlooby/projects/VDEs/GEQDSKs_wide_120ms/paraview_q95/'
#sweepMEQ
#rootPath = '/home/tlooby/HEATruns/SPARC/sweepMEQ_T4/interpolated/dt10ms_quadratic_T4_vSweep0.7/'
#outPath = '/home/tlooby/results/sweepMEQ/EQimages2/'
#rootPath = '/home/tlooby/results/VDEs/OLIM/'
#outPath = '/home/tlooby/results/VDEs/OLIM/'
#rootPath = '/home/tlooby/HEATruns/SPARC/sweepMEQ_T4/EQplots/'
#outPath = '/home/tlooby/HEATruns/SPARC/sweepMEQ_T4/EQplots/'
#rootPath = '/home/tlooby/source/sparc_Forced_VDE/output/'
#rootPath = '/home/tlooby/source/tomTest/dummyEQ/'
#outPath = '/home/tlooby/source/tomTest/dummyEQ/'
rootPath = '/home/tlooby/HEATruns/SPARC/oscillation/interpolated/dt1ms_sinusoid_1mm_100Hz/'
outPath = '/home/tlooby/HEATruns/SPARC/oscillation/EQplots/'

#height in pixels
h = 1300
xBox = [1.55, 1.75]
yBox = [-1.6, -1.2]
#xBox = None
#yBox = None

#read all files with a prefix
prefix = 'g000001.'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])

for i,g in enumerate(gFileList):
    f = rootPath+g
    MHD = MHDClass.setupForTerminalUse(gFile=f)
    ep = MHD.ep
    fig = pEQ.makePlotlyEQDiv(1, ep.g['time'], 'sparc', ep, height=h, gfile=None, logFile=False,
                                bg='#252625', xRange=xBox, yRange=yBox)

    #calculate q95 and display in title
    Bt0 = ep.g['Bt0']
    R0 = ep.g['RmAxis']
    Ip = ep.g['Ip'] / 1e6
    #95% flux surface
    surf = ep.getBs_FluxSur(0.9)
    Ridx = ~np.isnan(surf['Rs'])
    Zidx = ~np.isnan(surf['Zs'])
    idxs = np.logical_and(Ridx,Zidx)
    Rs = surf['Rs'][idxs]
    Zs = surf['Zs'][idxs]
    lcfs = np.vstack((Rs, Zs)).T
    #print(lcfs)
    #print(surf['Rs'])


    Rmax = np.max(lcfs[:,0])
    idxRmax = np.argmax(lcfs[:,0])
    maxSep = lcfs[idxRmax]
    Rmin = np.min(lcfs[:,0])
    Zmax = np.max(lcfs[:,1])
    Zmin = np.min(lcfs[:,1])
    Rgeo = (Rmax + Rmin)/2.0
    a = Rmax - ep.g['RmAxis']
    idx = np.argmax(lcfs[:,1])
    R_upper = lcfs[idx,0]
    idx = np.argmin(lcfs[:,1])
    R_lower = lcfs[idx,0]
    b = Zmax / a
    #ellipticity
    k = (Zmax - Zmin)/(2.0*a)
    #triangularity
    d_upper = (Rgeo - R_upper) / a
    d_lower = (Rgeo - R_lower) / a
    d = (d_upper + d_lower) / 2.0

    Bp = ep.BpFunc(maxSep[0], maxSep[1])[0][0]
    Bt = ep.BtFunc(maxSep[0], maxSep[1])[0][0]


    #print("Elongation at psiN=0.95: {:F}".format(k))
    #print("Triangularity at psiN=0.95: {:f}".format(d))

    term2 = ( 1 + k**2*(1 + 2*d**2 - 1.2*d**3) ) / 2.0
    q_uckan = (5 * a**2 *Bt0) / (R0 * Ip) * term2
    #print("Uckan Safety Factor using k,d at psiN=0.95: {:f}".format(q_uckan))
    eps = a / R0
    q95 = q_uckan * ( (1.17-0.65*eps)/(1-eps**2)**2 )
    #print("Uckan q95: {:f}".format(q95))

    #for printing q95
    #fig.update_layout(title="t={:0.1f} [ms]; q95 = {:0.3f}".format(ep.g['time']/10.0, q95))
    #fig.update_layout(title="t={:0.1f} [ms]".format(ep.g['time']))
    fig.update_layout(font=dict(size=40), margin=dict(l=10,r=10,b=10,t=100))
    #for no title
    fig.update_layout(title=None)
#    fig.update_layout(font=dict(size=40), margin=dict(l=10,r=10,b=50,t=100))
    #for timestep in name
    #fig.write_image(outPath+'{:05d}.png'.format(ep.g['time']))
    #for index in name
    fig.write_image(outPath+'{:05d}.png'.format(i))



    print("wrote image: {:05d}.png".format(ep.g['time']))
