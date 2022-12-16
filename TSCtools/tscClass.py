#tscClass.py
#description:   class object for TSC output file IO
#date:          Nov 2021
#engineer:      T Looby
import numpy as np

class tscIO:
    def __init__(self, aFile):
        """
        aFile is outputa file from TSC
        """
        self.aFile = aFile
        return


    def readRhoProfile(self):
        """
        read radial coordinate rho.

        generates rho, a list of arrays indexed to TSC write timesteps (self.ts)
        """
        print("Reading Rho Profiles...")
        switch = False
        self.rho = []
        with open(self.aFile, 'r') as f:
            for line in f:
                if switch == False:
                    if 'rho  HALe' in line:
                        switch = True
                        rho = []
                else:
                    lineData = line.split(' ')
                    if len(lineData) < 2.0:
                        self.rho.append(np.array(rho))
                        switch = False
                    else:
                        rho.append(float(lineData[0]))

        return


    def readRminor(self):
        """
        reads minor radius [m]

        generates rMinor, a list of arrays indexed to TSC write timesteps (self.ts)
        """
        print("Reading Radius Profiles...")
        switch = False
        self.rMinor = [] #[m]
        with open(self.aFile, 'r') as f:
            for line in f:
                if switch == False:
                    if 'j      ti(ev)' in line:
                        switch = True
                        r = []
                else:
                    if '1 cycle' in line:
                        self.rMinor.append(np.array(r))
                        switch = False
                    else:
                        r.append(float(line[153:164]))

        return

    def readRadialTprofilesRho(self):
        """
        reads T [eV] profile as a function of normalized radial coordinate, rho

        generates Te and Ti, lists of arrays indexed to TSC write timesteps (self.ts)
        """
        print("Reading Temperature Profiles...")
        switch = False
        self.Te = [] #[eV]
        self.Ti = [] #[eV]
        with open(self.aFile, 'r') as f:
            for line in f:
                if switch == False:
                    if 'rho  Te' in line:
                        switch = True
                        Te = []
                        Ti = []
                else:
                    lineData = line.split(' ')
                    if len(lineData[0]) < 2.0:
                        self.Te.append(np.array(Te))
                        self.Ti.append(np.array(Ti))
                        switch = False
                    else:
#                        Te.append(float(lineData[1]))
#                        Ti.append(float(lineData[2]))
                        Te.append(float(line[5:15]))
                        Ti.append(float(line[15:25]))

        return


    def readRadialTprofiles(self):
        """
        reads T [eV] profiles as a function of radius [m] from axis to sep

        generates Te and Ti, lists of arrays indexed to TSC write timesteps (self.ts)
        """
        print("Reading Temperature Profiles...")
        switch = False
        self.Te = [] #[eV]
        self.Ti = [] #[eV]
        with open(self.aFile, 'r') as f:
            for line in f:
                if switch == False:
                    if 'j      ti(ev)' in line:
                        switch = True
                        Te = []
                        Ti = []
                else:
#                    lineData = line.split(' ')
#                    lineData = [x for x in lineData if x != '']
                    if '1 cycle' in line:
                        self.Te.append(np.array(Te))
                        self.Ti.append(np.array(Ti))
                        switch = False
                    else:
#                        Te.append(float(lineData[1]))
#                        Ti.append(float(lineData[2]))
                        Ti.append(float(line[6:17]))
                        Te.append(float(line[18:29]))

        return


    def readRadialCurrentProfilesRho(self):
        """
        reads J [A/m^2] profile as a function of normalized radial coordinate, rho

        generates Jtot and Jbs, lists of arrays indexed to TSC write timesteps (self.ts)

        Jtot is total current density
        Jbs is bootstrap current density
        """
        print("Reading Current Profiles...")
        switch = False
        self.Jtot = [] #[A/m^2]
        self.Jbs = [] #[A/m^2]
        with open(self.aFile, 'r') as f:
            for line in f:
                if switch == False:
                    if 'rho  HALe' in line:
                        switch = True
                        Jtot = []
                        Jbs = []
                else:
                    lineData = line.split(' ')
                    if len(lineData) < 2.0:
                        self.Jtot.append(np.array(Jtot))
                        self.Jbs.append(np.array(Jbs))
                        switch = False
                    else:
                        Jtot.append(float(line[75:85]))
                        Jbs.append(float(line[65:75]))
        return


    def readRadialCurrentProfiles(self):
        """
        reads J [A/m^2] profile as a function of radius [m] from axis to sep

        generates J, list of arrays indexed to TSC write timesteps (self.ts)

        J is current density
        """
        print("Reading Current Profiles...")
        switch = False
        self.J = [] #[A/m^2]

        with open(self.aFile, 'r') as f:
            for line in f:
                if switch == False:
                    if 'j      ti(ev)' in line:
                        switch = True
                        J = []
                else:
#                    lineData = line.split(' ')
#                    lineData = [x for x in lineData if x != '']
                    if '1 cycle' in line:
                        self.J.append(np.array(J))
                        switch = False
                    else:
                        J.append(float(line[129:140]))

        return


    def readTimeSteps(self):
        """
        reads timesteps at which the profiles (and GEQDSKs?) are written

        can return an array that is a lesser length than the profiles because
        some timesteps can be repeated in the profile data
        """
        print("Reading Timesteps...")
        self.ts = [] #[s]
        cycles = []
        with open(self.aFile, 'r') as f:
            for line in f:
                if '1 cycle' in line and 'Sawtooth' not in line:
                    lineData = line.split(" ")
                    lineData = [x for x in lineData if x != '']
                    if lineData[2] not in cycles:
                        cycles.append(lineData[2])
                        self.ts.append(float(lineData[4]))

        return


    def readRadii(self):
        """
        reads major and minor radii at each write timestep

        generates r0 and a, lists of arrays indexed to TSC write timesteps (self.ts)
        """
        print("Reading Radii...")
        switch = False
        self.r0 = [] # major radius [m]
        self.a = [] # minor radius [m]
        with open(self.aFile, 'r') as f:
            for line in f:
                if switch == False:
                    if 'r0        a' in line:
                        switch = True
                else:
                    lineData = line.split(' ')
                    lineData = [x for x in lineData if x != '']
                    self.r0.append(float(lineData[0]))
                    self.a.append(float(lineData[1]))
                    switch = False

        return

    def readEQparams(self):
        """
        reads some of the EQ parameters at each timestep

        generates lists of arrays indexed to TSC write timesteps (self.ts)
        """
        print("Reading EQ Parameters")
        switch1 = False
        switch2 = False

        params1 = []
        params2 = []

        with open(self.aFile, 'r') as f:
            for line in f:
                if switch1 == False:
                    if 'q1          qe' in line:
                        switch1 = True
                else:
                    lineData = line.split(' ')
                    lineData = [x for x in lineData if x != '']
                    params1.append(lineData)
                    switch1 = False

                if switch2 == False:
                    if '1  cyc...' in line:
                        switch2 = True
                else:
                    lineData = line.split(' ')
                    lineData = [x for x in lineData if x != '']
                    params2.append(lineData)
                    switch2 = False

        allParams = np.hstack([np.array(params1), np.array(params2)])

        keys = ['q1','qe','betapol','li/2','li(GA d  ef)','vol', 'uint', 'npsit',
                '1 cyc...', 'time', 'dt', 'taue(ms)','i','j','tauekg','zmag(gzero)',
                'ekin','pl cur', 'amach', 'xmag', 'beta', 'loop v', 'iplim']

        self.EQdict = {}
        for i,row in enumerate(allParams.T):
            self.EQdict[keys[i]] = row

        return
