#calculateLoopV.py
#Description:   calculates loop voltage at a seperatrix using
#               a directory of GEQDSKs corresponding to time varying EQs
#Date:          20221216
#engineer:      T Looby
import os
import sys
import numpy as np
import plotly.graph_objects as go

EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

#===inputs, paths, etc.
rootPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/interpolated_100ms/'
outFile = rootPath + 'loopV.dat'
#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(rootPath) if (os.path.isfile(os.path.join(rootPath, f)) and prefix in f)])
#expicitly define gFileList
#gFileList = ['geqdsk_freegsu_run{:d}.geq_newWall_negPsi'.format(x) for x in np.arange(18)]

#===load EP objects
MHD = MHDClass.setupForTerminalUse(gFile=[rootPath+x for x in gFileList])

#Calculating psiSeps
psiSeps = []
ts = []
for eq in MHD.ep:
    psiSeps.append(2*np.pi*eq.g['psiSep']) #convert from Wb/rad to Wb
    ts.append(eq.g['time']/1000.0)

#calculating loop voltage
loopV = -1.0 * np.diff(psiSeps) / np.diff(ts)

print(psiSeps)
print(ts)


arr = np.vstack([ts[:-1], loopV]).T
head = "time[s],loopV[V]"
np.savetxt(outFile, arr, delimiter=",", fmt='%.10f', header=head)

#plot loop voltage
fig = go.Figure()
fig.add_trace(go.Scatter(x=ts, y=loopV))
fig.update_xaxes(title_text="<b>Time [s]</b>")
fig.update_yaxes(title_text="<b>Loop Voltage [V]</b>")
fig.update_layout(title='dt=100 [ms], V_average={:0.4f} [V]'.format(np.average(loopV)))
fig.show()

#plot flux
#fig = go.Figure()
#fig.add_trace(go.Scatter(x=ts, y=psiSeps))
#fig.update_xaxes(title_text="<b>Time [s]</b>")
#fig.update_yaxes(title_text="<b>Flux at Separatrix [Wb]</b>")
#fig.update_layout(title='dt=100 [ms]'.format(np.average(loopV)))
#fig.show()
