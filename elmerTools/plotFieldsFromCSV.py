import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

f1 = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stress/IDEA_run/elmerOutput.csv'
data1 = pd.read_csv(f1)

f2 = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stress_lq1.5_S0.9/tempStressElmer.csv'
data2 = pd.read_csv(f2)


fig = go.Figure()

colors = []
symbols = ['x', 'star', 'diamond', 'asterisk', 'bowtie', 'hourglass', 'circle-x', 'hexagram' ]


t = np.array(data1['Time'][:-1]*0.005+0.005)
#Elmer FEM data
fig.add_trace(go.Scatter(x=t, y=data1['max(temperature)'], name='lq0.6, S0.6', line=dict(width=2,),
                     mode='lines+markers', marker_size=10, marker_symbol=symbols[1], 
                     marker=dict(maxdisplayed=30)))

fig.add_trace(go.Scatter(x=t, y=data2['max(temperature)'], name='lq1.5, S0.9', line=dict(width=2,),
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
title="Max Temperature: ",

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


#fig.update_yaxes(title_text="<b>Maximum Von Mises [Pa]</b>")
fig.update_yaxes(title_text="<b>Temperature [degC]</b>")
fig.update_xaxes(title_text="<b>Time [s]</b>")


fig.show()