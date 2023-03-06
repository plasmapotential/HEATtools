#readSOLPSnetCDF.py
#reads SOLPS netCDF and saves data into python object.  plots grid with rad fluxes
import numpy as np
import pandas as pd
import SOLPSclass

cdfFile = "/home/tlooby/projects/xTarget/20230216_balanceXPT.nc"
contourFile = '/home/tlooby/SPARC/RZcontours/v2y.csv'
outFile = '/home/tlooby/projects/xTarget/Prad.csv'

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
fig = SOLPS.plotlyAllRadLines(d)
fig = SOLPS.addRZcontour(fig, contourFile)
fig.show()

#xtarget divertor box
box = [1.72, 1.9, -1.575, -1.38]

#scale the HF to 1 MW
Prad_target = 1.0e6 #[W]
Prad = SOLPS.Prad_all * Prad_target / SOLPS.Prad_sum
SOLPS.createHEATradCSV(Prad, file=outFile, boundBox=box)

