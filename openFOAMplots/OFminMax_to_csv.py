#converts an openfoam fieldMinMax.dat file to a csv file
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

f = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_20231206_nominal_lq0.6_S0.6_fRadDiv20/fieldMinMax.dat'
fOut = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_20231206_nominal_lq0.6_S0.6_fRadDiv20/Tile032_TMax.csv'

tmp = pd.read_csv(f, header=1, delimiter="\t")
tmp.columns = tmp.columns.str.strip()
tmp = tmp.sort_values('field')
tmp['field'] = tmp['field'].str.strip()
use = tmp['field']=='T'
maxTs = max(tmp[use]['max'].values)

mask = tmp['field'] == 'T'
t = tmp[mask].sort_values('# Time')['# Time'].values
t = np.insert(t, 0, 0)
varMax = tmp[mask].sort_values('# Time')['max'].values
varMax = np.insert(varMax, 0, 300)
data = np.vstack([t,varMax]).T

head = 't[s], Tpeak[K]'
np.savetxt(fOut, data, delimiter=',', header=head)



fig = go.Figure()
fig.add_trace(go.Scatter(x=t-0.001, y=varMax, line=dict(width=2,),
                     mode='lines', marker_size=10, 
                     marker=dict(maxdisplayed=100)))


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