#pullCoilCurrents.py
#description:  example script that loads TSC data, then scrapes coil currents
#date:          Dec 2021
#engineer:      T Looby
import numpy as np
import tscClass
import plotly.graph_objects as go

#TSC outputa file
f = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/outputaV2h01a'
#read the file and get coil currents and voltages
tsc = tscClass.tscIO(f)
tsc.readCoilCurrents()

#plot simple coil names
coilNames = ['CS1', 'CS2', 'CS3', 'PF1', 'PF2', 'PF3', 'PF4', 'Div1', 'Div2']
fig = tsc.plotCoilCurrents(coilNames)
fig.show()

#plot all coil names
coilNames = [
             'CS1U','CS1L','CS2U','CS2L','CS3U','CS3L',
             'PF1U','PF1L','PF2U','PF2L','PF3U','PF3L','PF4U','PF4L',
             'Div1U','Div1L','Div2U','Div2L'
             ]

fig = tsc.plotCoilCurrents(coilNames)
fig.show()
#save csv
