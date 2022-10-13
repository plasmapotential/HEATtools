#readSOLPSoutput.py
#reads SOLPS output and saves data into python object.  plots grid with rad fluxes
import numpy as np
import pandas as pd
import SOLPSclass


#usually a b2ra.dat file
#radFile = '/home/tom/SPARC/SOLPSoutput/SPARC_Ne_seeded_22-05-06_11-13/b2ra.dat_P29MW_ne1p2e20_pedx0p010_Ne0e22'
#radFile = '/home/tom/SPARC/SOLPSoutput/SPARC_Ne_seeded_22-05-06_11-13/b2ra.dat_P29MW_ne1p2e20_pedx0p010_Ne0p075e21_odivpuff'
radFile = '/home/tom/SPARC/SOLPSoutput/v2y/b2ra.dat_case_10MW_6-9_high'
atomFile = '/home/tom/SPARC/SOLPSoutput/v2y/neutrad.dat_case_10MW_6-9_high'
TeFile = '/home/tom/SPARC/SOLPSoutput/SPARC_Ne_seeded_22-05-06_11-13/te.dat_P29MW_ne1p2e20_pedx0p010_Ne0e22'
#usually a b2fgmtry file
geomFile =  '/home/tom/SPARC/SOLPSoutput/v2y/b2fgmtry'

#RZ contourFile
contourFile = '/home/tom/work/CFS/GEQDSKs/v2y.csv'

#import SOLPS interface and read files
SOLPS = SOLPSclass.SOLPS_IO()
SOLPS.readGeometry(geomFile)
SOLPS.readLineRadiation(radFile)
SOLPS.readAtomRadiation(atomFile)
radOut = '/home/tom/source/dummyOutput/RZ_SOLPS.csv'
box=[1.5,1.8,-1.55,-1.25]
SOLPS.createHEATradCSV(file=radOut, species='all', boundBox=box)

#plot the grid
#fig = SOLPS.plotlyMeshPlot()

#plot the rad profiles
['D^{0}', 'D^{+1}', 'Ne^{0}', 'Ne^{+1}', 'Ne^{+2}', 'Ne^{+3}', 'Ne^{+4}', 'Ne^{+5}', 'Ne^{+6}', 'Ne^{+7}', 'Ne^{+8}', 'Ne^{+9}', 'Ne^{+10}']
#fig = SOLPS.plotlySingleRadLine(species='Ne^{+4}')

#plot all radiation lines
#fig = SOLPS.plotlyAllRadLines()

#plot all radiation lines + atom radiation
fig = SOLPS.plotlyAllRad()

#overlay a RZ contour line
fig = SOLPS.addRZcontour(fig, contourFile)


fig.show()

#calculate temperature and plot
#SOLPS.readTe(TeFile)
#fig = SOLPS.plotlyTe()
#fig.show()
