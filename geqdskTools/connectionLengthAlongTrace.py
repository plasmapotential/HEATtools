#give a HEAT X,Y,Z magnetic field line trace, calculates connection length

import numpy as np

f = '/home/tom/HEAT/data/sparc_000001/0.000000000/trace2.dat'

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
print(d[-1])