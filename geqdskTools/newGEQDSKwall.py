import sys
import shutil
import numpy as np
import pandas as pd
#set up python environment
#dev machine
EFITPath = '/home/tom/source'
HEATPath = '/home/tom/source/HEAT/github/source'
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
rootPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/v2h01a/'
#sweep7
gFileList = [
            'geqdsk_0',
            'geqdsk_1',
            'geqdsk_2',
            'geqdsk_3',
            'geqdsk_4',
            'geqdsk_5',
            'geqdsk_6',
            'geqdsk_7',
            'geqdsk_8',
            'geqdsk_9',
            'geqdsk_10',
            ]


wallFile = '/home/tom/work/CFS/GEQDSKs/v2y.csv'
newSuffix = '_v2y_negPsi_negBt_negIp_negFpol'
newPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/'

shot = 1
df = pd.read_csv(wallFile, names=['R','Z'])

for gFile in gFileList:
    newGFile = gFile + newSuffix
    #copy file to tmp location with new name so that EP class can read it
    gRenamed = newPath+'g000001.00001'
    shutil.copyfile(rootPath+gFile, gRenamed)

    MHD = MHDClass.setupForTerminalUse(gRenamed)
    MHD.ep.g['Nwall'] = len(df['R'].values)
    MHD.ep.g['wall'] = np.vstack([df['R'].values, df['Z'].values]).T

    #flip psi
    MHD.ep.g['psiRZ'] = -1.0*MHD.ep.g['psiRZ']
    MHD.ep.g['psiSep'] = -1.0*MHD.ep.g['psiSep']
    MHD.ep.g['psiAxis'] = -1.0*MHD.ep.g['psiAxis']

    #flip Ip
    MHD.ep.g['Ip'] *= -1.0

    #flip Bt0
    MHD.ep.g['Bt0'] *= -1.0

    #flip Fpol
    MHD.ep.g['Fpol'] *= -1.0

    MHD.writeGfile(newPath + newGFile)
