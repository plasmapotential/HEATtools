#pullEQparams.py
#description:  example script that loads TSC data, then builds dict with some
#              MHD EQ plasma params
#date:          Nov 2021
#engineer:      T Looby
import numpy as np
from scipy.interpolate import interp1d
import scipy.integrate as integrate
import tscClass

#TSC outputa file
f = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/outputaV2h01a'
#read the file and get some profiles
tsc = tscClass.tscIO(f)

#get the dictionary
tsc.readEQparams()

#dictionary is tsc.EQdict.  example to print all keys:
print(tsc.EQdict.keys())

#example to print betapol
print(tsc.EQdict['betapol'])

#example to save betapol to file with timesteps
outFile = 'betapol.csv' #change to desired path
arr = np.vstack([tsc.EQdict['time'], tsc.EQdict['betapol']]).T
head = "time[s],betapol"
np.savetxt(outFile, arr, delimiter=",", fmt='%.10f', header=head)
