#give a HEAT X,Y,Z magnetic field line trace, calculates connection length

import numpy as np

f = '/home/tlooby/HEAT/data/sparc_000001/0.000000000/struct_pt000.csv'
#index where we want to start this trace, 0 if we want entire trace
idxStart = 2616
#index where we want to stop this trace, -1 if we want entire trace
idxStop = 4570
#direction of trace (this will be opposite what is set in HEAT trace file)
traceDir = 1 #

test = np.logical_and(idxStop!=None, idxStart!=None)
if test == True:
    if traceDir == 1:
        trace = np.genfromtxt(f, delimiter=',', comments='#')[idxStart:idxStop]
    else:
        trace = np.genfromtxt(f, delimiter=',', comments='#')[idxStop:idxStart]
else:
    trace = np.genfromtxt(f, delimiter=',', comments='#')


def distance(traceData:np.ndarray):
    """
    Calculate distance along curve/wall (also called S) of ND points:
    """
    distance = np.cumsum(np.sqrt(np.sum(np.diff(traceData,axis=0)**2,axis=1)))
    distance = np.insert(distance, 0, 0)
    return distance


d = distance(trace)

print(trace[0])
print(trace[-1])
print(d[0])
print(d[0])
print("Average Step Size: {:f}".format(np.average(np.diff(d))))
print(d[-1] + np.average(np.diff(d)))
print("distance: {:f} [m]".format((d[-1] - d[0])/1000.0))