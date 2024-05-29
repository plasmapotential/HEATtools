import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

field = 'max(vonmises)'

case1 = 'lq0.6_S1.25_fRadDiv70'
f1 = '/home/tlooby/HEAT/data/sparc_000001_oscillation_fixedSP_'+case1+'/elmer/max_T_stress.csv'
data1 = pd.read_csv(f1)

case2 = 'lq0.6_S1.25_fRadDiv70_20mm_100Hz'
f2 = '/home/tlooby/HEAT/data/sparc_000001_oscillation_sweep_'+case2+'/elmer/max_T_stress.csv'
data2 = pd.read_csv(f2)



fig = go.Figure()

colors = []
symbols = ['x', 'star', 'diamond', 'asterisk', 'bowtie', 'hourglass', 'circle-x', 'hexagram' ]


t = np.array(data1['Time'][:-1]*0.01+0.01)
#Elmer FEM data
fig.add_trace(go.Scatter(x=t, y=data1[field], name=case1, line=dict(width=2,),
                     mode='lines+markers', marker_size=10, marker_symbol=symbols[1], 
                     marker=dict(maxdisplayed=30)))

t = np.array(data2['Time'][:-1]*0.001+0.001)
fig.add_trace(go.Scatter(x=t, y=data2[field], name=case2, line=dict(width=2,),
                     mode='lines+markers', marker_size=10, marker_symbol=symbols[2], 
                     marker=dict(maxdisplayed=30)))



#limits
print(t)
plotLimit = False
if plotLimit == True:
    fig.add_trace(go.Scatter(
        x=[0.0, t[-1]+0.005],
        y=[6e8, 6e8],
        name="600 MPa",
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
#title="Max Von Mises: ",
title=field,

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


fig.update_yaxes(title_text="<b>Maximum Von Mises [Pa]</b>")
#fig.update_yaxes(title_text="<b>Temperature [degC]</b>")
fig.update_xaxes(title_text="<b>Time [s]</b>")


fig.show()