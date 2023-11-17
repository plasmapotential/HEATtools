#plots csv data that was exported from paraview
#using the find data feature in paraview enables user to slice data
#and plot maximum over time.  then you can export to CSV.
#here we plot that exported data

import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

f1 = '/home/tlooby/results/boundaryOps/T4slice/1mmSliceMid.csv'
f2 = '/home/tlooby/results/boundaryOps/T4slice/2mmSliceMid.csv'
f3 = '/home/tlooby/results/boundaryOps/T4slice/3mmSliceMid.csv'
f4 = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_20230525_1_max_6.09MWlowerOuter_lq0.6mm_S0.6mm/openFoam/heatFoam/A_objects087/postProcessing/fieldMinMax1/0/fieldMinMax.dat'

data1 = pd.read_csv(f1)
data2 = pd.read_csv(f2)
data3 = pd.read_csv(f3)

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

fig.add_trace(go.Scatter(x=t, y=varMax, name='0mm Depth', line=dict(width=2,),
                     mode='lines+markers', marker_size=10, marker_symbol=symbols[0], 
                     marker=dict(maxdisplayed=200)))
fig.add_trace(go.Scatter(x=data1['Time'], y=data1['max(T)'], name='1mm Depth', line=dict(width=2,),
                     mode='lines+markers', marker_size=10, marker_symbol=symbols[1], 
                     marker=dict(maxdisplayed=30)))
fig.add_trace(go.Scatter(x=data2['Time'], y=data2['max(T)'], name='2mm Depth', line=dict(width=2,),
                     mode='lines+markers', marker_size=10, marker_symbol=symbols[2], 
                     marker=dict(maxdisplayed=30)))
fig.add_trace(go.Scatter(x=data3['Time'], y=data3['max(T)'], name='3mm Depth', line=dict(width=2,),
                     mode='lines+markers', marker_size=10, marker_symbol=symbols[3], 
                     marker=dict(maxdisplayed=30)))



fig.add_trace(go.Scatter(
    x=[-0.05, data1['Time'].values[-1]+0.05],
    y=[1473, 1473],
    name="1400 degC",
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


fig.update_yaxes(title_text="<b>Maximum Slice Temperature [K]</b>")
fig.update_xaxes(title_text="<b>Time [s]</b>")







fig.show()
