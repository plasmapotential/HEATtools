#InputFileFromGEQDSKs.py
#Description:   makes a HEAT input file from a dir of GEQDSKs.  also writes
#               batchFile with the input files included
#Date:          20220901
#engineer:      T Looby
import os
import numpy as np

#path where gfiles are read from and where we will save the batchFile.dat
#gPath = '/home/tom/work/CFS/GEQDSKs/TSCruns/TSC-V2h01/TSC-V2h01/corrected_v2y_Ip_Bt_psi_Fpol/interpolated_25ms/'
#outPath = '/home/tom/HEATruns/SPARC/rampup_TSCvh01a/inputFiles/'
gPath = '/home/tlooby/HEATruns/SPARC/vscShadows/sparc/'
outPath = '/home/tlooby/HEATruns/SPARC/vscShadows/otherData/'

#read all files with a prefix
prefix = 'g000001'
gFileList = sorted([f for f in os.listdir(gPath) if (os.path.isfile(os.path.join(gPath, f)) and prefix in f)])
print(gFileList)
input('Press any key to continue')

def writeInputFile(file, var):
    """
    edit this function to write var where you need it.  currently in Pinj
    """
    with open (file, 'w') as f:
        f.write("# Input file for HEAT\n")
        f.write("# Format is: Variable, Value\n")
        f.write("#=============================================================\n")
        f.write("#                IO Variables\n")
        f.write("#=============================================================\n")
        f.write("vtpMeshOut, True\n")
        f.write("vtpPCOut, False\n")
        f.write("csvOut, True\n")
        f.write("#=============================================================\n")
        f.write("#                CAD Variables\n")
        f.write("#=============================================================\n")
        f.write("gridRes, standard\n")
        f.write("#==============================================================\n")
        f.write("#                MHD Variables\n")
        f.write("#==============================================================\n")
        f.write("shot, 1\n")
        f.write("tmin, 0\n")
        f.write("tmax, 10262\n")
        f.write("traceLength, 20\n")
        f.write("dpinit, 0.25\n")
        f.write("plasma3Dmask, 0 #1=true, 0=false\n")
        f.write("#==============================================================\n")
        f.write("#                Optical HF Variables\n")
        f.write("#==============================================================\n")
        f.write("hfMode, eich\n")
        f.write("lqCN, 3.0\n")
        f.write("lqCF, 5.0\n")
        f.write("lqPN, 1.0\n")
        f.write("lqPF, 1.0\n")
        f.write("lqCNmode, eich\n")
        f.write("lqCFmode, None\n")
        f.write("lqPNmode, None\n")
        f.write("lqPFmode, None\n")
        f.write("S, 0.15\n")
        f.write("SMode, user\n")
        f.write("fracCN, 0.6\n")
        f.write("fracCF, 0.4\n")
        f.write("fracPN, 0.1\n")
        f.write("fracPF, 0.0\n")
        f.write("fracUI,0.0\n")
        f.write("fracUO,0.5\n")
        f.write("fracLI,0.0\n")
        f.write("fracLO,0.5\n")
        f.write("Pinj,{:0.4f}\n".format(var))
        f.write("coreRadFrac, 0.0\n")
        f.write("qBG, 0.0\n")
        f.write("fG, 0.37\n")
        f.write("qFilePath, None\n")
        f.write("qFileTag, None\n")
        f.write("#==============================================================\n")
        f.write("#                Ion Gyro Orbit HF Variables\n")
        f.write("#==============================================================\n")
        f.write("N_gyroSteps, 5\n")
        f.write("gyroDeg, 10\n")
        f.write("gyroT_eV, 100\n")
        f.write("N_vSlice, 1\n")
        f.write("N_vPhase, 1\n")
        f.write("N_gyroPhase, 1\n")
        f.write("ionMassAMU, 2.014\n")
        f.write("vMode, single\n")
        f.write("ionFrac,0.5\n")
        f.write("gyroSources, gyroSourcePlane\n")
        f.write("#==============================================================\n")
        f.write("#                Radiated Power HF Variables\n")
        f.write("#==============================================================\n")
        f.write("radFile, /home/tom/HEATruns/SPARC/xTargetRad/sparc/RZ_xTarget.csv\n")
        f.write("Ntor, 20\n")
        f.write("Nref, 1\n")
        f.write("phiMin, -1.0\n")
        f.write("phiMax, 2.67\n")
        f.write("#==============================================================\n")
        f.write("#                OpenFOAM Variables\n")
        f.write("#==============================================================\n")
        f.write("OFtMin, 0\n")
        f.write("OFtMax, 9000\n")
        f.write("deltaT, 0.05\n")
        f.write("writeDeltaT, 0.05\n")
        f.write("STLscale, 1.0\n")
        f.write("meshMinLevel, 2\n")
        f.write("meshMaxLevel, 3\n")
        f.write("material, TUNG_SPARC\n")
    return


#here we are scaling power linearly in the input files
power = np.linspace(0.5,4,len(gFileList))

for i,g in enumerate(gFileList):
    #write input file
    name = "SPARC_input_"+ g.split(".")[1] +".csv"
    outFile = outPath + name
    print(name)
    writeInputFile(outFile, power[i])

    #append line to batchFile
    line = 'sparc,vscShadowVDE, '+g+', vscShadows_160deg.step, PFCs.csv, SPARC_input.csv, hfOpt:psiN:bdotn\n'
    if i==0:
        with open(outPath + "batchFile.dat", "w") as myfile:
            myfile.write(line)
    else:
        with open(outPath + "batchFile.dat", "a") as myfile:
            myfile.write(line)


print("Wrote input files")
