#sPolOneDirection.py
#calculates SP trajectory along tile assuming 1 direction movement
# (ie no SP oscillations, just a scan in one direction).
#Date:          20220831
#engineer:      T Looby
#
#
#how to build a sweep using geqdsks
#1) run sPol<method>.py to define SP trajectory
#2) run sweepInterpolator.py to interpolate GEQDSKs along SP trajectory
#3) run makeGEQDSKimages.py to generate .pngs of each sweep step
#4) run makeSweepLonger.py to add additional periods (if periodic)

import numpy as np
import plotly.graph_objects as go


#csv outfile
fOut = '/home/tlooby/HEATruns/SPARC/oscillation_sweep/EQs/SPsweep_oneDir_400mmPerSec.csv'

#Strike point velocity
vSP = 0.4 #[m/s]

#extent of sweep
#coordinates R,Z,S of T4:
#1570.000000, -1297.000000, 1631.747458,
#1720.000000, -1510.000000, 1892.264252,
# T4 ~260mm long
# mid T4 is ~ 85mm long
minS = 0.0
maxS = 0.15
deltaS = maxS - minS
dS = 0.001 #[m]
N = int(deltaS / dS)

tMax = deltaS / vSP
t = np.linspace(0,tMax,N+1)
dt = t[1]-t[0]
S = np.zeros((len(t)))
S[:] = vSP * t

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
np.savetxt(fOut, arr, delimiter=",")
