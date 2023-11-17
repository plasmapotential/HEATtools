#readSOLPSnetCDF.py
#reads SOLPS netCDF and saves data into python object.  plots grid with rad fluxes
import numpy as np
import pandas as pd
import SOLPSclass

cdfFile = "/home/tlooby/projects/xTarget/20230216_balanceXPT.nc"
contourFile = '/home/tlooby/SPARC/RZcontours/v2y.csv'
outFile = '/home/tlooby/projects/xTarget/Prad_20230216_balanceXPT_1MW.csv'
imageOut ='/home/tlooby/projects/xTarget/Prad_20230216_balanceXPT_1MW.png' 


SOLPS = SOLPSclass.SOLPS_NC()
SOLPS.readAll(cdfFile)
SOLPS.getXYfromGeom()

a = SOLPS.getListOfVars()
#print(sorted(a))
#print('adf' in a)

for v in a:
    if 'adf11' in v:
        print(v)


d = SOLPS.getSingleVar('b2stel_she_bal')


#fig = SOLPS.plot1cell(0)
#fig.show()
#fig = SOLPS.plotlySingleRadLine(d[0].flatten())
fig = SOLPS.plotlyAllRadLines(d, multiplier=None)
#fig = SOLPS.addRZcontour(fig, contourFile)
#fig.show()

#xtarget divertor box
box = [1.72, 1.83, -1.575, -1.37]
dR = box[1] - box[0]
dZ = box[3] - box[2]

#scale the HF to 1 MW
Prad_target = 1.0e6 #[W]
mult = Prad_target / SOLPS.Prad_sum
Prad = SOLPS.Prad_all * mult
print(mult)

fig = SOLPS.plotlyAllRadLines(d, multiplier=mult, colorBar=False, zMax=5691.0)
fig = SOLPS.addRZcontour(fig, contourFile, scale=1)

#bound the plot
#fig.update_xaxes(range = [box[0],box[1]])
#fig.update_yaxes(range = [box[2],box[3]])
#fig.update_layout(title=None)

w=800
h = 1200
fig.update_layout(
    font=dict(
        size=34,
    ),
    legend=dict(
        x=0.4,
        y=0.1,
        traceorder='normal',
    ),
    width=w,
    height=h,
    margin=dict(l=10,r=10,b=10,t=100)
)


fig.show()

fig.write_image(imageOut)

#create a radiation profile CSV for HEAT
#SOLPS.createHEATradCSV(Prad, file=outFile, boundBox=box)

