#plots maxT point data from explicit user defined directories
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

#name of each PFC
pfc1 = '/home/tom/HEAT/data/sparc_000001_sweep7_axisymmetricT4_noEdge_1sQuad/openFoam/heatFoam/RevolveT4'
pfc2 = '/home/tom/HEAT/data/sparc_000001_sweep7_axisymmetricT4_noEdge_1sTriangle/openFoam/heatFoam/RevolveT4'

files = [pfc1, pfc2]


nombres = ['Quadratic80ms', 'Triangle']

data = []
maxTs = []
namesWithTag = []
for i,f in enumerate(files):
    outfile = f+"/postProcessing/cellMax(T)/0/volFieldValue.dat" #peak over cells
    tmp = pd.read_csv(outfile, names=['t', 'T'], skiprows=[0,1,2,3], delimiter='\t')
    maxTs.append(max(tmp['T'].values))
    data.append(tmp.values)
    namesWithTag.append(nombres[i])

print(maxTs)
idxMax = np.argmax(maxTs)
print("Maximum T occurs on PFC: " + nombres[idxMax])

fig = go.Figure()

#for printing all PFC max's
colors = []
symbols = ['x', 'star', 'diamond', 'asterisk', 'bowtie', 'hourglass', 'circle-x', 'hexagram' ]
dash = ['dash', None, 'dashdot', 'dot']
for i,df in enumerate(data):
    print(df[:,0])
    fig.add_trace(go.Scatter(x=df[:,0], y=df[:,1], name=nombres[i], line=dict(width=4,dash=dash[i]),
                         mode='lines', marker_size=4,))



#temperature limits
fig.add_trace(go.Scatter(
    x=[-0.05,  df[-1,0]+0.05],
    y=[1623, 1623],
    name="Recrystal. T (Pure)",
    line=dict(color='firebrick', width=3, dash='dash'),
    marker_symbol='circle',
    marker_size=15,
    mode="lines+markers+text",
    text=["Limit", "Limit"],
    textposition="top center",
    textfont=dict(family="Arial", size=24, color="firebrick"),

))

fig.update_layout(
title="Max T: ",

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
