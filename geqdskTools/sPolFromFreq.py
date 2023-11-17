#sPolFromFreq.py
#Description:   Calculates Spol of strike point for 1 period given a sweep
#               frequency and amplitude
#Date:          20231026
#engineer:      T Looby
#
#how to build a sweep using vSweep, turntime, and geqdsks
#1) run sPolFromFreq.py to define SP trajectory
#2) run sweepInterpolator.py to interpolate GEQDSKs along SP trajectory
#3) run makeGEQDSKimages.py to generate .pngs of each sweep step
import numpy as np
import plotly.graph_objects as go


#csv outfile
fOut = '/home/tlooby/HEATruns/SPARC/oscillation/SPsweep.csv'

#amplitude [m]
A = 0.001
#sweep frequency [Hz]
f = 50.0
omega = 2*np.pi*f
#calculate period
period = 1.0/f
#create time basis
t = np.linspace(0,period, 1000)

S = A*np.sin(omega*t)


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
