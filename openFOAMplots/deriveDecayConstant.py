#derives exponential decay constant from fieldMinMax.dat data
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

#name of each PFC
pfc1 = '/home/tlooby/HEAT/data/sparc_000001_impulseResponse/openFoam/heatFoam/T006'
pfc2 = '/home/tlooby/HEAT/data/sparc_000001_impulseResponse2/openFoam/heatFoam/T006'
pfc3 = '/home/tlooby/HEAT/data/sparc_000001_impulseResponse2/openFoam/heatFoam/T006'
files = [pfc1, pfc2, pfc3]
#nombres = ['Quadratic80ms', 'Triangle']
nombres = ['T1', 'T2', 'T3']

data = []
maxTs = []
namesWithTag = []
for i,f in enumerate(files):
#    if tag in name:
    outfile = f + '/postProcessing/fieldMinMax1/0/fieldMinMax.dat' #peak at any point
    tmp = pd.read_csv(outfile, header=1, delimiter="\t")
    tmp.columns = tmp.columns.str.strip()
    tmp = tmp.sort_values('field')
    tmp['field'] = tmp['field'].str.strip()
    use = tmp['field']=='T'
    maxTs.append(max(tmp[use]['max'].values))
    data.append(tmp)
    namesWithTag.append(nombres[i])


#print(maxTs)
idxMax = np.argmax(maxTs)
#print("Maximum T occurs on PFC: " + nombres[idxMax])

def fit_exp_linear(t, y, C=0):
    y = y - C
    y = np.log(y)
    K, A_log = np.polyfit(t, y, 1)
    A = np.exp(A_log)
    return A, K

def model_func(t, A, K, C):
    return A * np.exp(K * t) + C

fig = go.Figure()

for i,df in enumerate(data):
    mask = df['field'] == 'T'
    t = df[mask].sort_values('# Time')['# Time'].values
    varMax = df[mask].sort_values('# Time')['max'].values
    varMax = np.insert(varMax, 0, 300.0)
    t = np.insert(t, 0, 0.0)


    idxPeak = np.argmax(varMax)+2
    C0 = np.min(np.floor(varMax[idxPeak:])) #initial temperature
    A, K = fit_exp_linear(t[idxPeak:], varMax[idxPeak:], C0)
    fit_y = model_func(t[idxPeak:], A, K, C0)

    fig.add_trace(go.Scatter(x=t[idxPeak:], y=varMax[idxPeak:], name=nombres[i]+"{:d}".format(i), line=dict(width=4,),
                         mode='lines', marker_size=4,))
    fig.add_trace(go.Scatter(x=t[idxPeak:], y=fit_y, name="Fit to T{:d}".format(i), line=dict(width=4,),
                         mode='lines', marker_size=4,))

    print("Decay Constant {:d}: {:f}".format(i, 1/K))


fig.update_yaxes(title_text="<b>Maximum PFC Temperature [K]</b>")
fig.update_xaxes(title_text="<b>Time [s]</b>")



fig.show()

