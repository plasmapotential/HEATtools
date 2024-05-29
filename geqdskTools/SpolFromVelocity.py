#SpolOfSweep.py
#Description:   Calculates Spol of strike point for 1 oscillation period given the maximum
#               strike point velocity.  Uses quadratic turns with user defined
#               turn around time
#Date:          20220831
#engineer:      T Looby
#
#how to build a sweep using vSweep, turntime, and geqdsks
#1) run SpolFromVelocity.py to define SP trajectory
#2) run sweepInterpolator.py to interpolate GEQDSKs along SP trajectory
#3) run makeGEQDSKimages.py to generate .pngs of each sweep step


#for quadratic, you need to tune the height to match your intended deltaS
#note that the sweep interpolator normalizes S in the gfile to S=0 here,
#so your Smin can be 0

import numpy as np
import pandas as pd
import sys
import os
import shutil
import scipy.interpolate as scinter
from scipy.interpolate import interp1d
import plotly.graph_objects as go

#csv outfile
f = '/home/tlooby/HEATruns/SPARC/sweepMEQ_T4/SPsweep.csv'

#can be quadratic, triangle
mode='quadratic'

#Strike point maximum velocity
vMax = 0.7 #[m/s]
#SP turn around time
turnTime = .08 #[s]
#min / max S of sweep
#minS = 0.0 #[m]
#maxS = 0.076#[m] for T5 calcs
#maxS = 0.230 #[m] tune this to get your objective maxS with the triangle
#maxS = 0.2575 #for quad with 230mm extent
#T4 v3b
#actual
#minS = 0.038
#maxS = 0.22
#minS = 1.6318
#maxS = 1.8923
#tuned
minS = 0.0
maxS = 0.20


deltaS = maxS - minS
print(deltaS)
period = 2*deltaS/vMax
freq = 1/period


#calculate evenly spaced S coordinates as a function of time
#step size in S
dS = 0.001 #[m]
N = int(2*deltaS / dS)
midPt = int(N/2.0)
t = np.linspace(0,period,N+1)
dt = t[1]-t[0]
tMid = t[midPt]
S = np.zeros((len(t)))
S[:midPt] = vMax * t[:midPt]
S[midPt:] = -vMax * (t[midPt:]-t[midPt]) + deltaS

if mode=='quadratic':
    #add in quadratic turn
    #linear segment: f1(t) = vMax*t, df1/dt = vMax
    #quad segment: f2(t) = alpha*t^2 + c0, df2/dt = 2*alpha*t
    #constrain solution such that:
    #f1(t1) = f2(t1)
    #df1(t1)/dt = df2(t1)/dt

    #first determine constants
    t1 = turnTime/2.0
    alpha = vMax / (2*t1)
    c0 = vMax * t1 / 2.0

    #at t=0
    S1 = vMax * t1
    use = np.where(t<t1)[0]
    S[use] = alpha*(t[use])**2 + c0

    #at tMid
    S1 = vMax * (tMid-t1)
    test = np.logical_and(t>(tMid-t1) ,t<(tMid+t1))
    use = np.where(test==True)[0]
    S[use] = -1.0 * alpha*(t[use]-tMid)**2 + c0 + S1


    #at t=period
    S1 = vMax * (period-t1)
    use = np.where(t > (period-t1))[0]
    S[use] = alpha*(t[use]-period)**2 + c0

elif mode=='triangle':
    S[:midPt] = vMax*t[:midPt]
    t1 = t[midPt]
    S1 = vMax * t1
    S[midPt:] = -vMax*(t[midPt:]-t1) + S1

#this printout is for tuning deltaS to be maximum range of PFCs
print("Actual deltaS: {:f} [m]".format(max(S)-min(S)))
print("timestep size: {:f} [s]".format(dt))

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=S))
fig.update_xaxes(title="t [s]")
fig.update_yaxes(title="S [m]")
fig.update_layout(
    font=dict(
        size=20,
    )
    )
fig.show()


#save csv for use later
arr = np.vstack([t,S]).T
np.savetxt(f, arr, delimiter=",")
