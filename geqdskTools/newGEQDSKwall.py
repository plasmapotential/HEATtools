import sys
import shutil
import numpy as np
import pandas as pd
#set up python environment
#dev machine
EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'
#appImage machine
#if you extract appImage you can point to these files directly in:
# <APPDIR>/usr/src/
#where AppDir is location of extracted files
#
#EFITPath = '/home/tom/source/HEAT/AppDir/usr/src'
#HEATPath = '/home/tom/source/HEAT/AppDir/usr/src'
sys.path.append(EFITPath)
sys.path.append(HEATPath)
import MHDClass


#edit these
rootPath = '/home/tlooby/projects/dummy/staging/'
#sweep7
gFileList = [
            'sparc_1655.geqdsk',
            ]


wallFile = '/home/tlooby/SPARC/RZcontours/v3c.csv'
newSuffix = '_psiOver2pi_negBt_negIp_negFpol_v3c'
newPath = rootPath

shot = 1
df = pd.read_csv(wallFile, names=['R','Z'])

for gFile in gFileList:
    newGFile = gFile + newSuffix
    #copy file to tmp location with new name so that EP class can read it
    gRenamed = newPath+'g000001.00001'
    shutil.copyfile(rootPath+gFile, gRenamed)

    MHD = MHDClass.setupForTerminalUse(gRenamed)
    MHD.ep.g['Nwall'] = len(df['R'].values)
    MHD.ep.g['wall'] = np.vstack([df['R'].values/1000.0, df['Z'].values/1000.0]).T

    #flip psi
    #MHD.ep.g['psiRZ'] = -1.0*MHD.ep.g['psiRZ']
    #MHD.ep.g['psiSep'] = -1.0*MHD.ep.g['psiSep']
    #MHD.ep.g['psiAxis'] = -1.0*MHD.ep.g['psiAxis']

    #normalize psi
    MHD.ep.g['psiRZ'] = MHD.ep.g['psiRZ'] / (2*np.pi)
    MHD.ep.g['psiSep'] = MHD.ep.g['psiSep'] / (2*np.pi)
    MHD.ep.g['psiAxis'] = MHD.ep.g['psiAxis'] / (2*np.pi)

    #flip Ip
    MHD.ep.g['Ip'] *= -1.0

    #flip Bt0
    MHD.ep.g['Bt0'] *= -1.0

    #flip Fpol
    MHD.ep.g['Fpol'] *= -1.0

    MHD.writeGfile(newPath + newGFile)
