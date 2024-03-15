#takes vtu files from Elmer that have been named with incrementing integers
#and converts the names to timesteps
import os


#where the files live:
rootDir = '/home/tlooby/HEAT/data/sparc_000001_sweepMEQ_T4_stress_lq1.5_S0.9/'
t0 = 5
dt = 5

#read all files with a prefix
prefix = 'case_'
nombres = sorted([f for f in os.listdir(rootDir) if (os.path.isfile(os.path.join(rootDir, f)) and prefix in f)])


for i,n in enumerate(nombres):
    t = i*dt + t0
    newName = rootDir + 'case_{:06d}.vtu'.format(t)
    os.rename(rootDir + n, newName)