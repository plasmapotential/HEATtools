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
#EFITPath = '/home/tom/source'
#HEATPath = '/home/tom/source/HEAT/github/source'
#CFS machine
EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'

sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass
import GUIscripts.plotly2DEQ as pEQ

#rootPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/interpolated_25ms/'
#outPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/EQplots/'
rootPath = '/home/tlooby/projects/VDEs/GEQDSKs_wide_120ms/paraviewImages/'
outPath = '/home/tlooby/projects/VDEs/GEQDSKs_wide_120ms/paraviewImages/'

#height in pixels
h = 820
xBox = [1.02, 2.72]
yBox = [-1.75, 1.75]

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])

for i,g in enumerate(gFileList):
    f = rootPath+g
    MHD = MHDClass.setupForTerminalUse(gFile=f)
    ep = MHD.ep
    fig = pEQ.makePlotlyEQDiv(1, ep.g['time'], 'sparc', ep, height=h, gfile=None, logFile=False,
                                bg='#252625', xRange=xBox, yRange=yBox)

    fig.update_layout(title="{:0.1f} [ms]".format(ep.g['time']/10.0))

    #for timestep in name
    #fig.write_image(outPath+'{:05d}.png'.format(ep.g['time']))
    #for index in name
    fig.write_image(outPath+'{:05d}.png'.format(i))
    print("wrote image: {:05d}.png".format(ep.g['time']))
