#plots maxT across all PFCs in an openFOAM directory
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np
#name of each PFC
#root = '/home/tom/results/sparc_1stRuns/sweep7/sparc_000001_sweep7/openFoam/heatFoam/'
#root = '/home/tom/HEAT/data/sparc_000001_sweep7/openFoam/heatFoam/'
#root = '/home/tom/results/SPARC/time2Recryst/'
#root = '/home/tom/HEAT/data/sparc_000001_sweep7_axisymmetricT4/openFoam/heatFoam/'
#root = '/home/tom/HEAT/data/sparc_000001_sweep7_10s_80msQuadTurn/openFoam/heatFoam/'
#root = '/home/tom/HEAT/data/sparc_000001_sweep7_/openFoam/heatFoam/'
#root = '/home/tom/HEAT/data/sparc_000001_sweep7_triangle/openFoam/heatFoam/'
#root = '/home/tom/HEAT/data/sparc_000001_sweep7_axisymmetricT4_1sQuad/openFoam/heatFoam/'
root = '/home/tom/HEAT/data/sparc_000001_sweep7_axisymmetricT4_noEdge_triangle/openFoam/heatFoam/'

nombres = [f.name for f in os.scandir(root) if f.is_dir()]
nombres.sort()
PFCname = 'T0'

#tag to plot
tag = 'lq1.5mm'

data = []
maxTs = []
namesWithTag = []
for i,name in enumerate(nombres):
#    if tag in name:
    outfile = root+name+"/postProcessing/cellMax(T)/0/volFieldValue.dat" #peak over cells
    tmp = pd.read_csv(outfile, names=['t', 'T'], skiprows=[0,1,2,3], delimiter='\t')
    maxTs.append(max(tmp['T'].values))
    data.append(tmp.values)
    namesWithTag.append(name)

idxMax = np.argmax(maxTs)
print("Maximum T occurs on PFC: " + nombres[idxMax])


fig = go.Figure()

#for printing max of multiple PFCs:
#df = data[idxMax]
#mask = df['field'] == 'T'
#t = df[mask].sort_values('# Time')['# Time'].values
#varMax = df[mask].sort_values('# Time')['max'].values
#varMax = np.insert(varMax, 0, 300)
#fig.add_trace(go.Scatter(x=t, y=varMax, name="Ion Optical", line=dict(color='rgb(17,119,51)', width=6, dash='dot'),
#                         mode='lines', marker_symbol='cross', marker_size=14))

#for printing all PFC max's
colors = []
symbols = ['x', 'star', 'diamond', 'asterisk', 'bowtie', 'hourglass', 'circle-x', 'hexagram' ]


for i,df in enumerate(data):
    fig.add_trace(go.Scatter(x=df[:,0], y=df[:,1], name=nombres[i], line=dict(width=4,),
                         mode='lines', marker_size=4,))


##temperature limits
fig.add_trace(go.Scatter(
    x=[-0.05, df[-1,0]+0.05],
    y=[1623, 1623],
    name="Recrystal. T (Pure)",
    line=dict(color='firebrick', width=3, dash='dash'),
    marker_symbol='circle',
    marker_size=15,
    mode="lines+markers+text",
    text=["Limit 1", "Limit 1"],
    textposition="top center",
    textfont=dict(family="Arial", size=24, color="firebrick"),
))

#fig.add_trace(go.Scatter(
#    x=[-0.05, t[-1]+0.05],
#    y=[1773, 1773],
#    name="Recrystal. T (La203 2%)",
#    mode="lines+markers",
#    line=dict(color='firebrick', width=3, dash='dash',),
#    marker_symbol='square',
#    marker_size=15,
##    mode="lines+markers+text",
##    text=["Limit 1", "Limit 1"],
##    textposition="top center",
##    textfont=dict(family="Arial", size=24, color="firebrick"),
#
#))
#fig.add_trace(go.Scatter(
#    x=[-0.05, t[-1]+0.05],
#    y=[1973, 1973],
#    name="Recrystal. T (Re 5%)",
#    mode="lines+markers",
#    line=dict(color='firebrick', width=3, dash='dash'),
#    marker_symbol='cross',
#    marker_size=15,
##    mode="lines+markers+text",
##    text=["Limit 1", "Limit 1"],
##    textposition="top center",
##    textfont=dict(family="Arial", size=24, color="firebrick"),
#))




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
