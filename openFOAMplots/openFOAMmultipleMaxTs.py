#plots maxT across all PFCs in an openFOAM directory
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np
#name of each PFC
#root = '/home/tom/results/sparc_1stRuns/sweep7/sparc_000001_sweep7/openFoam/heatFoam/'
#root = '/home/tom/HEAT/data/sparc_000001_sweep7/openFoam/heatFoam/'
#root = '/home/tom/HEAT/data/sparc_000001_rampup_TSCvh01a_1mm_1lq/openFoam/heatFoam/'
#root = '/media/tom/8f18dea0-fd98-4cd0-8dcf-0af04aad82c4/work/resultsCFS/TSC_rampup_dec2022/sparc_000001_rampup_TSCvh01a_ramped4MW_dt100ms/openFoam/heatFoam/'
#root = '/home/tlooby/HEAT/data/sparc_000001_ILIM_NX_ellipse1mm_1782_lq0.9_S0.45_temperature/openFoam/heatFoam/'
root = '/home/tlooby/HEAT/data/sparc_000001_ILIM_NX_ellipse1mm_1781_hybridPolBez2_PSOL10MW_temperature/openFoam/heatFoam/'

nombres = [f.name for f in os.scandir(root) if f.is_dir()]
nombres.sort()

nombres2 = ['Top', 'Middle', 'Bottom']

PFCname = 'Top'

#tag to plot
tag = 'lq1.5mm'

data = []
maxTs = []
namesWithTag = []
for i,name in enumerate(nombres):
#    if tag in name:
    outfile = root+name+'/postProcessing/fieldMinMax1/0/fieldMinMax.dat' #peak at any point
    tmp = pd.read_csv(outfile, header=1, delimiter="\t")
    tmp.columns = tmp.columns.str.strip()
    tmp = tmp.sort_values('field')
    tmp['field'] = tmp['field'].str.strip()
    use = tmp['field']=='T'
    maxTs.append(max(tmp[use]['max'].values))
    data.append(tmp)
    namesWithTag.append(name)

print("Using these directories:")
print(namesWithTag)

print(maxTs)
idxMax = np.argmax(maxTs)
print("Maximum T occurs on PFC: " + nombres[idxMax])
#idxMax2 = np.argmax(maxTs[:idxMax]+maxTs[idxMax+1:])
#print("2nd Maximum T occurs on PFC: " + nombres[idxMax2])

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
    mask = df['field'] == 'T'
    t = df[mask].sort_values('# Time')['# Time'].values
    varMax = df[mask].sort_values('# Time')['max'].values
    varMax = np.insert(varMax, 0, 300)
    fig.add_trace(go.Scatter(x=t-0.001, y=varMax, name=nombres[i], line=dict(width=2,),
                         mode='lines+markers', marker_size=10, marker_symbol=symbols[i], 
                         marker=dict(maxdisplayed=30)))
    
    


#temperature limits
fig.add_trace(go.Scatter(
    x=[0.0, t[-1]+0.0005 - 0.001],
    y=[1773, 1773],
    name="1500 degC",
    mode="lines+markers",
    line=dict(color='firebrick', width=3, dash='dash'),
    marker_symbol='circle',
    marker_size=15,
#    mode="lines+markers+text",
#    text=["Limit 1", "Limit 1"],
#    textposition="top center",
#    textfont=dict(family="Arial", size=24, color="firebrick"),

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
