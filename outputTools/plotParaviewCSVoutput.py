#creates a plot from a paraview csv output

import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

field = 'max(temperature)'

f1 = '/home/tlooby/HEAT/data/sparc_000001_IOLIM_1353_S3_v1_lq0.6_elmer/elmer/T.csv'
data1 = pd.read_csv(f1)



fig = go.Figure()

colors = []
symbols = ['x', 'star', 'diamond', 'asterisk', 'bowtie', 'hourglass', 'circle-x', 'hexagram' ]


t = np.array(data1['Time'][:-1]*0.01+0.01)
#Elmer FEM data
fig.add_trace(go.Scatter(x=t, y=data1[field]-273.15, name='Peak T [degC]', line=dict(width=2,),
                     mode='lines', marker_size=10, marker_symbol=symbols[1], 
                     marker=dict(maxdisplayed=30)))



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


fig.update_yaxes(title_text="<b>Peak Temperature [degC]</b>")
#fig.update_yaxes(title_text="<b>Temperature [degC]</b>")
fig.update_xaxes(title_text="<b>Time [s]</b>")



fig.show()