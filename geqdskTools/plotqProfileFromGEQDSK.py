#plotqProfileFromGEQDSKs.py
#Engineer:      T Looby
#Date:          20240119
#description:
#plots q profile from GEQDSK

import numpy as np
import sys
import os
import shutil
import plotly.graph_objects as go

EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass

gFilePath = '/home/tlooby/source/sparc_Forced_VDE/Equilibria/originals/g000001.00001'
ep = MHDClass.setupForTerminalUse(gFile=gFilePath).ep

print(ep.g['qpsi'])
print(ep.g['psi'])


fig = go.Figure()
fig.add_trace(go.Scatter(x=ep.g['psiN'], y=np.abs(ep.g['q'])))
fig.update_layout(xaxis_title="$\psi_N$", yaxis_title="q", font=dict(size=20))

fig.show()

