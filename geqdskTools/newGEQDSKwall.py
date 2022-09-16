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
rootPath = '/home/tom/work/CFS/GEQDSKs/sweep7/'
gFileList = [
            'geqdsk_freegsu_run0.geq',
            'geqdsk_freegsu_run1.geq',
            'geqdsk_freegsu_run2.geq',
            'geqdsk_freegsu_run3.geq',
            'geqdsk_freegsu_run4.geq',
            'geqdsk_freegsu_run5.geq',
            'geqdsk_freegsu_run6.geq',
            'geqdsk_freegsu_run7.geq',
            'geqdsk_freegsu_run8.geq',
            'geqdsk_freegsu_run9.geq',
            ]


wallFile = '/home/tom/work/CFS/GEQDSKs/v2y.csv'
newSuffix = '_v2y_negPsi_negBt_negIp_negFpol'
newPath = '/home/tom/work/CFS/GEQDSKs/sweep7_v2y/'

shot = 1
df = pd.read_csv(wallFile, names=['R','Z'])

for gFile in gFileList:
    newGFile = gFile + '_newWall_negPsi'
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
