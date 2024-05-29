import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

field = 'max(vonmises)'

cases = [
#    'oscillation_fixedSP_lq0.6_S1.25_fRadDiv70',
    'slowSweep_lq0.6_S1.25_fRadDiv70_dt10ms_fixedSP',
#    'slowSweep_lq0.6_S1.25_fRadDiv70_vSP200mm_120mm_dt10ms',
#    'slowSweep_lq0.6_S1.25_fRadDiv70_vSP300mm_150mm_dt10ms',
#    'slowSweep_lq0.6_S1.25_fRadDiv70_vSP400mm_150mm_dt10ms',
#    'oscillation_fixedSP_lq0.6_S1.25_fRadDiv70_mesh500um',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_10mm_100Hz',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_20mm_100Hz',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_30mm_100Hz',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_20mm_50Hz',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_20mm_10Hz',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_20mm_200Hz',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_20mm_100Hz_T0573K',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_40mm_100Hz',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_20mm_200Hz_mesh500um',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_40mm_100Hz_mesh500um',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_40mm_100Hz_mesh300um',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_20mm_100Hz_mesh500um',
#    'oscillation_sweep_lq0.6_S1.25_fRadDiv70_20mm_100Hz_dt500us',
#    'slowSweep_lq0.6_S1.25_fRadDiv70_vSP100mm_120mm',
#    'slowSweep_lq0.6_S1.25_fRadDiv70_vSP200mm_120mm',
#    'slowSweep_lq0.6_S1.25_fRadDiv70_vSP200mm_120mm_dt5ms',
    'slowSweep_lq0.6_S1.25_fRadDiv70_dt10ms_vSP100mmps',
    'slowSweep_lq0.6_S1.25_fRadDiv70_dt10ms_vSP300mmps',
    'slowSweep_lq0.6_S1.25_fRadDiv70_dt10ms_vSP500mmps',
    'slowSweep_lq0.6_S1.25_fRadDiv70_dt10ms_vSP700mmps',
#    'slowSweep_lq0.6_S1.25_fRadDiv70_dt10ms_vSP1000mmps',
#    'slowSweep_lq0.6_S1.25_fRadDiv70_dt10ms_vSP1200mmps',    
#    'slowSweep_lq0.6_S1.25_fRadDiv70_dt10ms_vSP1200mmps',
    ]

names = [
#    'fixedSP',
    'fixedSP',
#    'slowSweep_0.2m/s_dt10ms',
#    'slowSweep_0.3m/s_dt10ms',
#    'slowSweep_0.4m/s_dt10ms',
#    'fixedSP_500um',
#    '10mm_100Hz',
#    '20mm_100Hz_dt1ms',
#    '30mm_100Hz',
#    '20mm_50Hz',
#    '20mm_10Hz',
#    '20mm_200Hz',
#    '20mm_100Hz_T0573K',
#    '40mm_100Hz_1mm',
#    '20mm_200Hz_500um',
#    '40mm_100Hz_500um',
#    '40mm_100Hz_300um',
#    '20mm_100Hz_500um',
#    '20mm_100Hz_dt500us',
#    'slowSweep_0.1m/s',
#    'slowSweep_0.2m/s',
#    'slowSweep_0.2m/s_dt5ms',
    'vSP=0.1m/s',
    'vSP=0.3m/s',
    'vSP=0.5m/s',
    'vSP=0.7m/s',
#    'vSP1000mmps',
#    'vSP1200mmps',    
]


#for no offsets
offsets = np.zeros((len(names)))
#for custom offsets
#offsets = np.array([
#    0.0,
#    -0.15,
#    -0.11,
#    0.0,
#    -0.176,
#    -0.1,
#    ])



fig = go.Figure()

colors = []
symbols = ['x', 'star', 'diamond', 'asterisk', 'bowtie', 'hourglass', 'circle-x', 'hexagram', 'square' ]

for i,c in enumerate(cases):
    f = '/home/tlooby/HEAT/data/sparc_000001_'+c+'/elmer/max_T_stress.csv'
    #f = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stressReX_'+c+'/elmer/maxPrincipal.csv'
    data = pd.read_csv(f)
    if i<5: #for cases when you ran at 10ms time resolution
        t = np.array(data['Time'][:-1]*0.01+offsets[i])
    #elif i==1: #for cases when you ran at 10ms time resolution
    #    t = np.array(data['Time'][:-1]*0.01)
    #elif i == len(cases)-1: #for cases when you ran at 0.5ms time resolution
    #    t = np.array(data['Time'][:-1]*0.0005+0.0005)
    #elif i == len(cases)-1: #for cases when you ran at 5ms time resolution
    #    t = np.array(data['Time'][:-1]*0.005+0.005)
    else: #for 1ms time resolution
        t = np.array(data['Time'][:-1]*0.001+offsets[i])

    print(i)
    print(names[i])

    #Elmer FEM data
    fig.add_trace(go.Scatter(x=t, y=data[field], name=names[i], line=dict(width=2,),
                         mode='lines+markers', marker_size=10, marker_symbol=symbols[i], 
                         marker=dict(maxdisplayed=30)))


#limits
plotLimit = False
if plotLimit == True:
    fig.add_trace(go.Scatter(
        x=[0.0, t[-1]+0.005],
        y=[1.1667E-4, 1.1667E-4],
        name="1 pulse limit",
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
title="Max Von Mises: ",
#title="Max Temperature: ",

margin=dict(
    l=100,
    r=100,
    b=100,
    t=100,
    pad=2
),
)

fig.update_layout(
    legend=dict(
    yanchor="bottom",
    y=0.02,
    xanchor="right",
    x=0.98
    ),
    font=dict(
#        family="Courier New, monospace",
        size=30,
    )
#
    )

fig.update_xaxes(range = [0.0,1.1])
fig.update_yaxes(exponentformat = 'power')

fig.update_yaxes(title_text="<b>Maximum Von Mises [Pa]</b>")
#fig.update_yaxes(title_text="<b>Maximum Principal [Pa]</b>")
#fig.update_yaxes(title_text="<b>Maximum ReX Fraction</b>")
#fig.update_yaxes(title_text="<b>Temperature [degC]</b>")
fig.update_xaxes(title_text="<b>Time [s]</b>")


fig.show()