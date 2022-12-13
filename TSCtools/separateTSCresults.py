#separateTSCresults.py
#description:   split a TSC run into multiple geqdsk files
#date:          Nov 2021
#engineer:      T Looby

import numpy as np
file = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/geqdskV2h01a'
outPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/v2h01a/'

print("reading file "+file )

i=0
with open(file, "r") as inF:
    for line in inF:
        if 'c...' in line:
            if i>0:
                outStream.close()
            outF = outPath + 'geqdsk_{:d}'.format(i)
            i+=1
            print(outF)
            outStream = open(outF, "a")
            outStream.write(line)
        else:
            outStream.write(line)


outStream.close()
