#===============================================================================
#                       Plot maxT, maxHF, etc.
#===============================================================================
#read data file
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

#use this to write an EPS file
writeEPS = False
epsFile = '/home/tom/phd/dissertation/diss/figures/castelTplot.eps'

nombres = ['Peak T']
names = ['Peak T']
root = '/home/tom/HEAT/data/sparc_000001_time2Recryst_2.59MW/openFoam'
data = []
for name in nombres:
    #GUI output
#    outfile = root+'/heatFoam/S029_0001665_00-Divertor_Assembly_Segment_2_Tile_4_Armor_Plates001/postProcessing/fieldMinMax1/0/minMaxTnoTab.dat'
#    tmp = pd.read_csv(outfile, header=1)
    #TUI output
    outfile = root+'/heatFoam/S029_0001665_00-Divertor_Assembly_Segment_2_Tile_4_Armor_Plates001/postProcessing/fieldMinMax1/0/fieldMinMax.dat'
    tmp = pd.read_csv(outfile, header=1, delimiter="\t")
    tmp.columns = tmp.columns.str.strip()
    tmp = tmp.sort_values('field')
    tmp['field'] = tmp['field'].str.strip()
    data.append(tmp)



fig = go.Figure()
#optical
df = data[0]
mask = df['field'] == 'T'
t = df[mask].sort_values('# Time')['# Time'].values
varMax = df[mask].sort_values('# Time')['max'].values
varMax = np.insert(varMax, 0, 300)
fig.add_trace(go.Scatter(x=t, y=varMax, name="Peak T on T4 Slices", line=dict(color='royalblue', width=6, dash='dot')))

fig.update_layout(
            #title='Time History of openFOAM FVM Variables',
            xaxis_title='<b>Time [s]</b>',
            yaxis_title='Peak Temperature',
            font=dict(
                family="Arial",
                size=24,
                color="Black"
                ),
                )

fig.add_trace(go.Scatter(
    x=[0.05, t[-1]],
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
fig.add_trace(go.Scatter(
    x=[0.05, t[-1]],
    y=[1773, 1773],
    name="Recrystal. T (La203 2%)",
    mode="lines+markers",
    line=dict(color='firebrick', width=3, dash='dash',),
    marker_symbol='square',
    marker_size=15,
#    mode="lines+markers+text",
#    text=["Limit 1", "Limit 1"],
#    textposition="top center",
#    textfont=dict(family="Arial", size=24, color="firebrick"),

))
fig.add_trace(go.Scatter(
    x=[0.05, t[-1]],
    y=[1973, 1973],
    name="Recrystal. T (Re 5%)",
    mode="lines+markers",
    line=dict(color='firebrick', width=3, dash='dash'),
    marker_symbol='cross',
    marker_size=15,
#    mode="lines+markers+text",
#    text=["Limit 1", "Limit 1"],
#    textposition="top center",
#    textfont=dict(family="Arial", size=24, color="firebrick"),
))

#optical peak arrow
#fig.add_annotation(x=5.01, y=2720,
#            text=r'$\text{Optical T}_{peak} = 2720 K$',
#            showarrow=True,
#            font=dict(
#                family="Courier New, monospace",
#                size=24,
#                color='rgb(17,119,51)'
#                ),
#            xanchor="right",
#            xshift=-5,
#            arrowhead=2,
#            arrowsize=3,
#            arrowcolor='rgb(17,119,51)',
#            ax=-80,
#            ay=-10,)
#
##gyro peak arrow
#fig.add_annotation(x=5.01, y=2631,
#            text=r'$\text{Gyro T}_{peak} = 2631 K$',
#            showarrow=True,
#            font=dict(
#                family="Courier New, monospace",
#                size=24,
#                color='royalblue'
#                ),
#            xanchor="right",
#            xshift=-5,
#            arrowhead=2,
#            arrowsize=3,
#            arrowcolor='royalblue',
#            ax=-30,
#            ay=100,)

fig.add_annotation(x=4.5, y=1500,
            text=r'$\text{T}_{peak} = 1627 K$',
            showarrow=False,
            font=dict(
                size=26,
                color='royalblue'
                ),
                )
#fig.update_yaxes(title_text="<b>Maximum PFC Temperature [K]</b>")

fig.update_layout(
#title="Temperature Probe Time Evolution",

margin=dict(
    l=5,
    r=5,
    b=5,
    t=5,
    pad=2
),
)

fig.update_layout(legend=dict(
    yanchor="middle",
    y=0.9,
    xanchor="left",
    x=0.1
))





fig.show()

if writeEPS==True:
    fig.write_image(epsFile)
