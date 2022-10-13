#plotMaxTsFromCSV.py
#plots maximum temperatures from csv files instead of OF tree
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

f1 = '/home/tom/results/SPARC/T4sweep7/vSweep0.7_dt7ms_10s_maxTdata_T000_triangle.csv'
#f1 = '/home/tom/results/SPARC/T4sweep7/vSweep0.7_dt7ms_10s_maxTdata_T001_triangle.csv'
#f1 = '/home/tom/results/SPARC/T4sweep7/vSweep0.7_dt7ms_10s_maxTdata_T002_triangle.csv'

f2 = '/home/tom/results/SPARC/T4sweep7/vSweep0.7_dt7ms_10s_maxTdata_T000_quad80ms.csv'
#f2 = '/home/tom/results/SPARC/T4sweep7/vSweep0.7_dt7ms_10s_maxTdata_T001_quad80ms.csv'
#f2 = '/home/tom/results/SPARC/T4sweep7/vSweep0.7_dt7ms_10s_maxTdata_T002_quad80ms.csv'

fig = go.Figure()

triData = np.genfromtxt(f1)
quadData = np.genfromtxt(f2).T

fig.add_trace(go.Scatter(x=triData[:,0], y=triData[:,1], name='Triangle', line=dict(width=4,),
                     mode='lines', marker_size=4,))
fig.add_trace(go.Scatter(x=quadData[:,0], y=quadData[:,1], name='Quadratic 80ms Turn', line=dict(width=4,dash='dot'),
                     mode='lines', marker_size=4,))


#temperature limits
fig.add_trace(go.Scatter(
    x=[-0.05, triData[-1,0]+0.05],
    y=[1623, 1623],
    name="Recrystal. T (Pure)",
    mode="lines+markers",
    line=dict(color='firebrick', width=3, dash='dash'),
    marker_symbol='circle',
    marker_size=15,
#    mode="lines+markers+text",
#    text=["Limit 1", "Limit 1"],
#    textposition="top center",
#    textfont=dict(family="Arial", size=24, color="firebrick"),

))


fig.update_layout(
    margin=dict(
        l=100,
        r=100,
        b=100,
        t=100,
        pad=2
        ),
)

fig.update_layout(
#    legend=dict(
#    yanchor="middle",
#    y=0.9,
#    xanchor="left",
#    x=0.1
#    ),
    font=dict(
#        family="Courier New, monospace",
        size=30,
    )
#
    )


fig.update_yaxes(title_text="<b>Maximum PFC Temperature [K]</b>")
fig.update_xaxes(title_text="<b>Time [s]</b>")




fig.show()
