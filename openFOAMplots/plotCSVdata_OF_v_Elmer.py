#plots csv data to compare openFOAM to Elmer FEM

import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

#f1 = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stress/IDEA_run/elmerOutput.csv'
f1 = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stressReX_lq0.6_S0.6_fRadDiv70/elmer_T0_293K/elmerData.csv'
f4 = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stressReX_lq0.6_S0.6_fRadDiv70/elmer_T0_293K/fieldMinMax_OF20230525_lq0.6_S0.6_fRadDiv70_middleT4.dat'
data1 = pd.read_csv(f1)


T4data = []
data4 = pd.read_csv(f4, header=1, delimiter="\t")
data4.columns = data4.columns.str.strip()
data4 = data4.sort_values('field')
data4['field'] = data4['field'].str.strip()
use = data4['field']=='T'
T4data.append(max(data4[use]['max'].values))

fig = go.Figure()
mask = data4['field'] == 'T'
t = data4[mask].sort_values('# Time')['# Time'].values
varMax = data4[mask].sort_values('# Time')['max'].values
varMax = np.insert(varMax, 0, 300)







colors = []
symbols = ['x', 'star', 'diamond', 'asterisk', 'bowtie', 'hourglass', 'circle-x', 'hexagram' ]

#only plot up to 1 second
tUse = np.where(t<=1.0)[0]

#openFOAM data
fig.add_trace(go.Scatter(x=t[tUse], y=varMax[tUse] - 273.15, name='openFOAM', line=dict(width=2,),
                     mode='lines+markers', marker_size=10, marker_symbol=symbols[0], 
                     marker=dict(maxdisplayed=200)))

#Elmer FEM data
fig.add_trace(go.Scatter(x=data1['Time'][:-1]*0.005+0.005, y=data1['max(temperature)']-273.15, name='Elmer', line=dict(width=2,),
                     mode='lines+markers', marker_size=10, marker_symbol=symbols[1], 
                     marker=dict(maxdisplayed=30)))




#overlay temperature limit
#fig.add_trace(go.Scatter(
#    x=[-0.05, t[tUse]+0.05],
#    y=[1473, 1473],
#    name="1400 degC",
#    mode="lines+markers",
#    line=dict(color='firebrick', width=3, dash='dash'),
#    marker_symbol='circle',
#    marker_size=15,
##    mode="lines+markers+text",
##    text=["Limit 1", "Limit 1"],
##    textposition="top center",
##    textfont=dict(family="Arial", size=24, color="firebrick"),
#
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


fig.update_yaxes(title_text="<b>Maximum Slice Temperature [degC]</b>")
fig.update_xaxes(title_text="<b>Time [s]</b>")







fig.show()
