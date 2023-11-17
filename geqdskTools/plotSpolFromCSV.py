#plotSpolFromCSV.py
#Description:   plots Spol(t) from a trajectory CSV file
#Date:          20220830
#engineer:      T Looby

import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import interp1d

#csv file
f = '/home/tlooby/HEATruns/SPARC/sweepMEQ_T4/SPsweep.csv'
#output file
fOut = '/home/tlooby/HEATruns/SPARC/sweepMEQ_T4/SPtrajectory.png'
#read user specified SP trajectory file
S_csv = np.genfromtxt(f, comments='#', delimiter=',')

#create inverse function, f_tS
tMidIdx = np.argmax(S_csv[:,1])
#create function for forward interpolation
f_St = interp1d(S_csv[:,0], S_csv[:,1], kind='linear')
#create monotonic function for inverse interpolation
f_tS = interp1d(S_csv[:tMidIdx,1], S_csv[:tMidIdx,0], kind='linear', fill_value="extrapolate")

#user specified points to overlay onto plot (get these from sPolFromGfile.py)
#S1 = [0.02427542, 0.03559984, 0.04740993, 0.05975101, 0.07267976, 0.08626334, 0.10058658]
#S1 = S1 - np.min(S1)
S1 = [np.min(S_csv[:,1]), np.max(S_csv[:,1])]

#user supplies dt that corresponds to new GEQDSK interpolation timestep
dt = 0.005
tMax = S_csv[-1,0] / 2
Nt = int(tMax/dt)
t0 = np.linspace(0,tMax,Nt+1)
print(t0)
S2 = f_St(t0)

t1 = f_tS(S1)

fig = go.Figure()
fig.add_trace(go.Scatter(x=S_csv[:,0], y=S_csv[:,1], name="SP Trajectory", 
                         line=dict(width=5)))
fig.add_trace(go.Scatter(x=t1, y=S1, mode='markers',
            marker=dict(
            size=40,
            ),
            name="Original GEQDSK Points"
            ))
fig.add_trace(go.Scatter(x=t0, y=S2, mode='markers',
            marker=dict(
            size=15,
            ),
            marker_symbol='x',
            name="Interpolated GEQDSK Points"
            ))
fig.update_xaxes(title="t [s]")
fig.update_yaxes(title="S [m]")
fig.update_layout(
    font=dict(
        size=40,
    )
    )

fig.update_layout(
    legend=dict(
        x=0.4,
        y=0.1,
        traceorder='normal',
    ),
    width=1800,
    height=1200,
    margin=dict(l=10,r=10,b=10,t=10)
)
fig.show()
fig.write_image(fOut)
