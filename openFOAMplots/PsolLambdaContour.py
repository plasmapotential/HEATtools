#plots a contour plot of Psol vs lambda_q, with colorbar of Temperature (or others)
#engineer:  T Looby
#date:      20230610

import numpy as np
import plotly.graph_objects as go
import pandas as pd

#user inputs
fIn = '/home/tlooby/HEATruns/SPARC/MEQscans/spicyLimits.csv'
region = 'T3'
zVar = 'Time to 1300degC [s]'
xVar = 'PSOL [MW]'
yVar = 'Lambda_q [mm]'
title = 'Time to Limit for Static Pulse on '+region+' (max 10s)'
#title = 'Time to Limit for 10s Static Pulse on All WHA Regions'




data = pd.read_csv(fIn).fillna(10.0)
x = data[data['Region']==region][xVar]
y = data[data['Region']==region][yVar]
z = data[data['Region']==region][zVar]

fig = go.Figure()
fig.add_trace(
    go.Contour(
        x=x,
        y=y,
        z=z,
        reversescale=True,
        colorbar={'title':'[s]'}
        )
    )

fig.update_xaxes(title=xVar)
if 'ambda_q' in yVar:
    yVar = r'$\huge{\lambda_q \quad \text{[mm]}}$'
fig.update_yaxes(title=yVar)

fig.update_layout(
    title=title,
    font=dict(
#        family="Courier New, monospace",
        size=30,
        ),
    
)

fig.show()