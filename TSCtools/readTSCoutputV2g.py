"""
Alex Creely
2020.04.06

readTSCoutput.py

Python script to read an 'outputa' file from TSC.

For now just reads coil group currents.

"""

import numpy as np
import matplotlib.pyplot as plt
import sys


class tscOutput(object):

    def __init__(self,outputFileIn,coilGroupsIn):

        self.outputFile         = outputFileIn
        self.coilGroupNum       = coilGroupsIn
        self.currentTimes       = None
        self.fluxTime           = None
        self.flux               = None
        self.coilGroupCurrents  = None
        self.coilGroupVoltage   = None
        self.coilGroupPower     = None
        self.feedbackCurrents   = None
        self.feedbackVoltage    = None
        self.feedbackPower      = None
        self.totalPower         = None

        self.coilGroupCurrents2 = None
        self.coilGroupVoltage2  = None

        self.elongation         = None
        self.triangularity      = None
        self.R0                 = None
        self.a                  = None
        self.elongation95       = None
        self.triangularity95    = None
        self.shapeTime          = None
        
        self.zMag               = None
        self.xMag               = None
        self.Ip                 = None
        self.IpAtCurrentTimes   = None
        self.positionTime       = None

        self.Te                 = None
        self.ne                 = None
        self.rminor             = None
        self.profileTime        = None

        self.groupTurns         = None

        return

    def scrapeCoilGroupCurrents(self):

        self.coilGroupCurrents = None
        self.coilGroupVoltage = None
        self.currentTimes = None
        self.fluxTime = None
        self.flux = None
        self.feedbackCurrents = None
        self.feedbackVoltage = None

        self.coilGroupCurrents2 = None
        self.coilGroupVoltage2 = None

        self.groupTurns = np.zeros(self.coilGroupNum)

        index = 0
        turnIndex = 0
        intTurnIndex = 0
        voltIndex = 0
        fluxIndex = 0

        coilCurrentTemp = np.zeros([self.coilGroupNum])
        coilVoltageTemp = np.zeros([self.coilGroupNum])
        feedbackCurrentTemp = np.zeros([self.coilGroupNum])
        feedbackVoltageTemp = np.zeros([self.coilGroupNum])

        coilVoltageTemp2 = np.zeros([5])
        coilCurrentTemp2 = np.zeros([5])

        with open(self.outputFile) as f:

            for line in f:

                if index != 0:
                    
                    if index == 1 or index == 2:

                        index += 1

                    elif index in range(3,(self.coilGroupNum+3)):

                        coilCurrentTemp[index-3] = float(line[6:17])
                        coilVoltageTemp[index-3] = float(line[30:41])
                        feedbackCurrentTemp[index-3] = float(line[6:17])
                        feedbackVoltageTemp[index-3] = float(line[30:41])
                        index += 1

                    else:

                        if self.coilGroupCurrents is None:

                            self.coilGroupCurrents = coilCurrentTemp
                            self.coilGroupVoltage = coilVoltageTemp
                            self.feedbackCurrents = feedbackCurrentTemp
                            self.feedbackVoltage = feedbackVoltageTemp

                        else:
                        
                            self.coilGroupCurrents = np.vstack((
                                self.coilGroupCurrents,
                                coilCurrentTemp))
                            
                            self.coilGroupVoltage = np.vstack((
                                self.coilGroupVoltage,
                                coilVoltageTemp))

                            self.feedbackCurrents = np.vstack((
                                self.feedbackCurrents,
                                feedbackCurrentTemp))

                            self.feedbackVoltage = np.vstack((
                                self.feedbackVoltage,
                                feedbackVoltageTemp))

                        coilCurrentTemp = np.zeros([self.coilGroupNum])
                        coilVoltageTemp = np.zeros([self.coilGroupNum])
                        
                        feedbackCurrentTemp = np.zeros([self.coilGroupNum])
                        feedbackVoltageTemp = np.zeros([self.coilGroupNum])
                        
                        index = 0
                

                elif line[0:26] == ' coil curr (ka)  at cycle=':

                    if self.currentTimes is None:

                        self.currentTimes = np.array([float(line[42:])])

                    else:

                        self.currentTimes = np.append(self.currentTimes,
                                                  float(line[42:]))

                    index = 1

                #Turns for external coils

                elif line[0:39] == ' ngroup       resistance     inductance':

                    turnIndex = 1

                elif ((turnIndex != 0) & (turnIndex <= (self.coilGroupNum-6))):
                    
                    self.groupTurns[turnIndex-1] = float(line[73:86])

                    turnIndex += 1

                #Turns for internal coils

                elif line[0:27] == ' internal coil information:':

                    intTurnIndex = 1

                elif intTurnIndex == 1:

                    intTurnIndex = 2

                elif ((intTurnIndex >= 2) & (intTurnIndex <= 25)):

                    group = int(line[27:29])

                    if group < 18:

                        self.groupTurns[group-1] += np.abs(float(line[33:37]))

                    else:

                        self.groupTurns[group-1] += np.abs(float(line[33:37]))
                        
                    intTurnIndex += 1

                #Other count of voltages

                elif line[0:39] == ' ncoil  igroupc    ceg0(ka)     ceg(ka)':

                    voltIndex = 1

                elif voltIndex != 0:

                    if voltIndex in range(1,6):

                        coilCurrentTemp2[voltIndex-1] = float(line[19:29])
                        coilVoltageTemp2[voltIndex-1] = float(line[58:68])
                        voltIndex += 1

                    else:

                        if self.coilGroupCurrents2 is None:

                            self.coilGroupCurrents2 = coilCurrentTemp2
                            self.coilGroupVoltage2 = coilVoltageTemp2

                        else:
                        
                            self.coilGroupCurrents2 = np.vstack((
                                self.coilGroupCurrents2,
                                coilCurrentTemp2))
                            
                            self.coilGroupVoltage2 = np.vstack((
                                self.coilGroupVoltage2,
                                coilVoltageTemp2))

                        coilCurrentTemp2 = np.zeros(5)
                        coilVoltageTemp2 = np.zeros(5)
                        
                        feedbackCurrentTemp2 = np.zeros(5)
                        feedbackVoltageTemp2 = np.zeros(5)
                        
                        voltIndex = 0

                elif line[0:25] == ' special R. Taylor output':
                    
                    if self.fluxTime is None:

                        self.fluxTime = np.array([float(line[50:62])])

                    else:

                        self.fluxTime = np.append(self.fluxTime,
                                                  float(line[50:62]))

                        
                    fluxIndex = 1

                elif fluxIndex != 0:

                    if line[5:36] == '0.000E+00  0.000E+00  0.000E+00':

                        if self.flux is None:

                            self.flux = np.array([float(line[70:80])])

                        else:

                            self.flux = np.append(self.flux,
                                                  float(line[70:80]))

                        fluxIndex = 0

                    else:
                        pass

                else:
                    pass

        #print(self.groupTurns)

        self.coilGroupPower = (np.abs(self.coilGroupCurrents
                               *self.coilGroupVoltage))#/self.groupTurns)
        self.feedbackPower = np.abs(self.feedbackCurrents
                              *self.feedbackVoltage*self.groupTurns)

        self.coilGroupVoltage = self.coilGroupVoltage*self.groupTurns

        self.feedbackVoltage = self.feedbackVoltage*self.groupTurns

        self.feedbackCurrents = self.feedbackCurrents*self.groupTurns

        self.totalPower = ((self.coilGroupPower[:,0]) +
                           (self.coilGroupPower[:,1]) +
                           (self.coilGroupPower[:,2]) +
                           (self.coilGroupPower[:,3]) +
                           (self.coilGroupPower[:,4]) +
                           (self.coilGroupPower[:,5]) +
                           (self.coilGroupPower[:,6]) +
                           (self.coilGroupPower[:,7]) +
                           (self.coilGroupPower[:,8]) +
                           (self.coilGroupPower[:,9]) +
                           (self.coilGroupPower[:,10]) +
                           (self.coilGroupPower[:,11]) +
                           (self.coilGroupPower[:,12]) +
                           (self.coilGroupPower[:,13]) +
                           (self.coilGroupPower[:,14]) +
                           (self.coilGroupPower[:,15]) +
                           (self.coilGroupPower[:,16]) +
                           (self.coilGroupPower[:,17]) +
                           (self.coilGroupPower[:,18]) +
                           (self.coilGroupPower[:,19]))

        return

    def scrapeProfiles(self):

        index = 0
        timeTemp = 0

        self.Te = []
        self.ne = []
        self.rminor = []

        tiTemp = None
        teTemp = None
        rminorTemp = None

        with open(self.outputFile) as f:

            for line in f:

                #scrape profiles

                if index != 0:

                    if index == 1:

                        index += 1

                    elif index == 2:

                        if line[0:17] == '    j      ti(ev)':

                            index += 1

                            if self.profileTime is None:
                                
                                self.profileTime = np.array([timeTemp])

                            else:

                                self.profileTime = np.append(self.profileTime,
                                                             timeTemp)
                                

                        else:

                            index = 0

                    elif index >= 3:

                        if line[0:5] == '    1':

                            teTemp = np.array([float(line[7:17])])
                            neTemp = np.array([float(line[43:53])])
                            rminorTemp = np.array([float(line[154:164])])

                        elif line[0:2] == '  ':

                            teTemp = np.append(teTemp, float(line[7:17]))
                            neTemp = np.append(neTemp, float(line[43:53]))
                            rminorTemp = np.append(rminorTemp,
                                                   float(line[154:164]))


                        else:

                            self.Te.append(teTemp)
                            self.ne.append(neTemp)
                            self.rminor.append(rminorTemp)
                            
                            index = 0


                elif line[0:7] == '1 cycle':

                    index = 1

                    tiTemp = None
                    teTemp = None
                    rminorTemp = None

                    timeTemp = float(line[24:34])

                else:

                    pass
                

        return

    def scrapeShaping(self):

        index = 0

        with open(self.outputFile) as f:

            for line in f:

                #Scrape zMag

                if (len(line) == 130 and not ('X' in line)
                    and not ('. ' in line)):

                    if self.positionTime is None:

                        self.positionTime = np.array([float(line[8:18])])

                        self.zMag = np.array([float(line[51:61])])
                        self.xMag = np.array([float(line[95:105])])
                        self.Ip = np.array([float(line[73:84])])

                    else:

                        self.positionTime = np.append(self.positionTime,
                                                   [float(line[8:18])])

                        self.zMag = np.append(self.zMag,
                                              [float(line[51:61])])
                        self.xMag = np.append(self.xMag,
                                              [float(line[95:105])])
                        self.Ip = np.append(self.Ip,
                                              [float(line[73:84])])

                    

                #Scrape most shaping parameters

                if line[0:11] == '         r0':

                    index = 1

                elif index == 1:

                    if self.shapeTime is None:

                        self.R0 = np.array([float(line[0:11])])
                        self.a = np.array([float(line[11:20])])
                        self.triangularity = np.array([float(line[20:29])])
                        self.elongation = np.array([float(line[29:38])])

                    else:

                        self.R0 = np.append(self.R0,
                                            [float(line[0:11])])
                        self.a = np.append(self.a,
                                           [float(line[11:20])])

                        self.triangularity = np.append(self.triangularity,
                                                       [float(line[20:29])])

                        self.elongation = np.append(self.elongation,
                                                    [float(line[29:38])])

                    index += 1

                elif index == 2:

                    index += 1

                elif index == 3:

                    if line[0:19] == '     95% flux surf:':

                        if self.shapeTime is None:

                            self.triangularity95 = np.array(
                                [float(line[20:29])])
                            self.elongation95 = np.array([float(line[29:38])])

                        else:

                            self.triangularity95 = np.append(
                                self.triangularity95,[float(line[20:29])])
                            
                            self.elongation95 = np.append(self.elongation95,
                                                        [float(line[29:38])])

                        index += 1

                    else:
                        
                        pass

                elif index in range(4,8):

                    index += 1

                elif index == 8:

                    if self.shapeTime is None:

                        self.shapeTime = np.array([float(line[8:18])])

                    else:

                        self.shapeTime = np.append(self.shapeTime,
                                                   [float(line[8:18])])

                    index = 0

                else:

                    pass
                
        return

    def interpolateIp(self):


        self.IpAtCurrentTimes = np.interp(self.currentTimes, self.positionTime,
                                          self.Ip)

        return

    def estimateStartupCurrents(self, breakPoint = 0.10):

        rampSlopes = np.zeros(self.coilGroupNum)
        breakCurrent = np.zeros(self.coilGroupNum)
        tZeroCurrent = np.zeros(self.coilGroupNum)

        for i in range(0,self.coilGroupNum):

            rampSlopes[i] = ((self.coilGroupCurrents[-1,i]
                              - self.coilGroupCurrents[0,i])/
                             (self.currentTimes[-1] - self.currentTimes[0]))
    

            breakCurrent[i] = ((breakPoint - self.currentTimes[0])
                               *rampSlopes[i] + self.coilGroupCurrents[0,i])

            if i < 8:

                startupSlopeMult = 2.0

            else:

                startupSlopeMult = 1.0

            tZeroCurrent[i] = ((0.0 - breakPoint)
                               *rampSlopes[i]*startupSlopeMult
                              + breakCurrent[i])


        self.currentTimes = np.insert(self.currentTimes, 0, breakPoint)
        self.currentTimes = np.insert(self.currentTimes, 0, 0.0)

        self.coilGroupCurrents = np.insert(self.coilGroupCurrents, 0,
                                           breakCurrent,axis=0)
        self.coilGroupCurrents = np.insert(self.coilGroupCurrents, 0,
                                      tZeroCurrent,axis=0)

        self.feedbackCurrents = np.insert(self.feedbackCurrents, 0,
                                      np.zeros(self.coilGroupNum),axis=0)
        self.feedbackCurrents = np.insert(self.feedbackCurrents, 0,
                                      np.zeros(self.coilGroupNum),axis=0)

        self.IpAtCurrentTimes = np.insert(self.IpAtCurrentTimes, 0,
                                          breakPoint*2*1e6)
        self.IpAtCurrentTimes = np.insert(self.IpAtCurrentTimes, 0,
                                          0.0)

            

        return

    def estimateStartupVoltage(self, breakPoint = 0.10):

        breakVoltage = np.zeros(self.coilGroupNum)
        tZeroVoltage = np.zeros(self.coilGroupNum)

        for i in range(0,self.coilGroupNum):

            breakVoltage[i] = np.mean(self.coilGroupVoltage[:,i])

            if i < 8:

                tZeroVoltage[i] = breakVoltage[i]*2

            else:

                tZeroVoltage[i] = breakVoltage[i]

        self.coilGroupVoltage = np.insert(self.coilGroupVoltage, 0,
                                           breakVoltage,axis=0)
        self.coilGroupVoltage = np.insert(self.coilGroupVoltage, 0,
                                      tZeroVoltage,axis=0)

        self.feedbackVoltage = np.insert(self.feedbackVoltage, 0,
                                      np.zeros(self.coilGroupNum),axis=0)
        self.feedbackVoltage = np.insert(self.feedbackVoltage, 0,
                                      np.zeros(self.coilGroupNum),axis=0)

        return

    def plotCoilGroupCurrents(self):

        plt.figure()
        plt.axhline(y=0,color='black',linewidth=2)
        
        plt.plot(self.currentTimes,self.coilGroupCurrents[:,0]/1000,
                 color='red',label='CS1',linewidth=3)
        plt.plot(self.currentTimes,self.coilGroupCurrents[:,1]/1000,
                 color='orange',label='CS2',linewidth=3)
        plt.plot(self.currentTimes,self.coilGroupCurrents[:,2]/1000,
                 color='dodgerblue',label='CS3',linewidth=3)
        plt.plot(self.currentTimes,self.coilGroupCurrents[:,3]/1000,
                 color='blue',label='PF1',linewidth=3)
        plt.plot(self.currentTimes,self.coilGroupCurrents[:,4]/1000,
                 color='green',label='PF2',linewidth=3)
        plt.plot(self.currentTimes,self.coilGroupCurrents[:,5]/1000,
                 color='turquoise',label='PF3',linewidth=3)
        plt.plot(self.currentTimes,self.coilGroupCurrents[:,6]/1000,
                 color='purple',label='PF4',linewidth=3)
        plt.plot(self.currentTimes,self.coilGroupCurrents[:,7]/1000,
                 color='limegreen',label='Div1',linewidth=3)
        plt.plot(self.currentTimes,self.coilGroupCurrents[:,8]/1000,
                 color='teal',label='Div2',linewidth=3)

        axes = plt.gca()

        #axes.set_ylim(-40,40)

        axes.set_xlabel('Time (s)',fontsize=20,labelpad=-5)
        axes.set_ylabel('Current (MA)',fontsize=20,labelpad=-4)
        plt.tick_params(labelsize=16)

        plt.legend(fontsize=16)
        
        plt.show()

        return

    def saveCoilGroupCurrents(self,saveFileIn):

        np.save(saveFileIn + 'time', self.currentTimes)
        np.save(saveFileIn + 'currents', self.coilGroupCurrents)

        return

def plotFullDischargeCurrents(outputs):

    plt.figure(figsize=(8,6))
    plt.axhline(y=0,color='black',linewidth=2)

    for i in range(0,len(outputs)):

        if i == 0:
    
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,0]/1000,
                     color='red',label='CS1U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,1]/1000,
                     color='red',label='CS1L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,2]/1000,
                     color='orange',label='CS2U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,3]/1000,
                     color='orange',label='CS2L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,4]/1000,
                     color='dodgerblue',label='CS3U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,5]/1000,
                     color='dodgerblue',label='CS3L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,6]/1000,
                     color='blue',label='PF1U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,7]/1000,
                     color='blue',label='PF1L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,8]/1000,
                     color='green',label='PF2U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,9]/1000,
                     color='green',label='PF2L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,10]/1000,
                     color='turquoise',label='PF3U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,11]/1000,
                     color='turquoise',label='PF3L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,12]/1000,
                     color='purple',label='PF4U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,13]/1000,
                     color='purple',label='PF4L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,14]/1000,
                     color='limegreen',label='Div1U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,15]/1000,
                     color='limegreen',label='Div1L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,16]/1000,
                     color='teal',label='Div2U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,17]/1000,
                     color='teal',label='Div2L',linewidth=3,linestyle='--')

            plt.plot(outputs[i].positionTime,
                     outputs[i].Ip/1.0e6,
                      color='black',label='Ip',linewidth=3)

        else:

            if outputs[i].currentTimes[0] > 1.0:

                linestyleA = '-'

            else:

                linestyleA = 'dotted'

            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,0]/1000,
                     color='red',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,1]/1000,
                     color='red',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,2]/1000,
                     color='orange',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,3]/1000,
                     color='orange',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,4]/1000,
                     color='dodgerblue',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,5]/1000,
                     color='dodgerblue',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,6]/1000,
                     color='blue',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,7]/1000,
                     color='blue',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,8]/1000,
                     color='green',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,9]/1000,
                     color='green',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,10]/1000,
                     color='turquoise',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,11]/1000,
                     color='turquoise',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,12]/1000,
                     color='purple',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupCurrents[:,13]/1000,
                     color='purple',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,14]/1000,
                     color='limegreen',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,15]/1000,
                     color='limegreen',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,16]/1000,
                     color='teal',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,17]/1000,
                     color='teal',linewidth=3,linestyle='--')

            plt.plot(outputs[i].positionTime,
                     outputs[i].Ip/1.0e6,
                      color='black',linewidth=3)
        
    axes = plt.gca()

    #axes.set_ylim(-45,45)

    axes.set_xlabel('Time (s)',fontsize=16,labelpad=0)
    axes.set_ylabel('Coil Current (MA)',fontsize=16,labelpad=-10)
    plt.tick_params(labelsize=16)

    plt.legend(fontsize=12, ncol=3)

    #plt.savefig('PFcurrentsV2c.png',format='png',dpi=600)

    return

def plotFullDischargeVoltage(outputs):

    plt.figure(figsize=(8,6))
    plt.axhline(y=0,color='black',linewidth=2)

    for i in range(0,len(outputs)):

        if i == 0:
    
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,0]/1.0,
                     color='red',label='CS1U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,1]/1.0,
                     color='red',label='CS1L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,2]/1.0,
                     color='orange',label='CS2U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,3]/1.0,
                     color='orange',label='CS2L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,4]/1.0,
                     color='dodgerblue',label='CS3U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,5]/1.0,
                     color='dodgerblue',label='CS3L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,6]/1.0,
                     color='blue',label='PF1U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,7]/1.0,
                     color='blue',label='PF1L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,8]/1.0,
                     color='green',label='PF2U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,9]/1.0,
                     color='green',label='PF2L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,10]/1.0,
                     color='turquoise',label='PF3U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,11]/1.0,
                     color='turquoise',label='PF3L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,12]/1.0,
                     color='purple',label='PF4U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,13]/1.0,
                     color='purple',label='PF4L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,14]/1.0,
                     color='limegreen',label='Div1U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,15]/1.0,
                     color='limegreen',label='Div1L',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,16]/1.0,
                     color='teal',label='Div2U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,17]/1.0,
                     color='teal',label='Div2L',linewidth=3,linestyle='--')

        else:

            if outputs[i].currentTimes[0] > 1.0:

                linestyleA = '-'

            else:

                linestyleA = 'dotted'

            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,0]/1.0,
                     color='red',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,1]/1.0,
                     color='red',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,2]/1.0,
                     color='orange',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,3]/1.0,
                     color='orange',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,4]/1.0,
                     color='dodgerblue',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,5]/1.0,
                     color='dodgerblue',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,6]/1.0,
                     color='blue',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,7]/1.0,
                     color='blue',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,8]/1.0,
                     color='green',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,9]/1.0,
                     color='green',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,10]/1.0,
                     color='turquoise',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,11]/1.0,
                     color='turquoise',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,12]/1.0,
                     color='purple',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,13]/1.0,
                     color='purple',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,14]/1.0,
                     color='limegreen',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,15]/1.0,
                     color='limegreen',linewidth=3,linestyle='--')
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,16]/1.0,
                     color='teal',linewidth=3,linestyle=linestyleA)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].coilGroupVoltage[:,17]/1.0,
                     color='teal',linewidth=3,linestyle='--')
        
    axes = plt.gca()

    #axes.set_ylim(-45,45)

    axes.set_xlabel('Time (s)',fontsize=16,labelpad=0)
    axes.set_ylabel('Voltage (kV)',fontsize=16,labelpad=-10)
    plt.tick_params(labelsize=16)

    plt.legend(fontsize=16)

    #plt.savefig('PFvoltagesV1d.png',format='png',dpi=100)

    return

def plotTrimCurrents(outputs):

    plt.figure(figsize=(8,6))
    plt.axhline(y=0,color='black',linewidth=2)

    for i in range(0,len(outputs)):

        if i == 0:

            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,18],
                     color='black',label='VS1U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,19],
                     color='gray',label='VS1L',linewidth=3)

        else:

            if outputs[i].currentTimes[0] > 1.0:

                linestyle = '-'

            else:

                linestyle = '--'

            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,18],
                     color='black',label=None,linewidth=3,
                     linestyle = linestyle)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackCurrents[:,19],
                     color='gray',label=None,linewidth=3,
                     linestyle = linestyle)

        axes = plt.gca()

    #axes.set_ylim(-45,45)

    axes.set_xlabel('Time (s)',fontsize=16,labelpad=0)
    axes.set_ylabel('Current (kA)',fontsize=16,labelpad=-10)
    plt.tick_params(labelsize=16)

    plt.legend(fontsize=16)

    return

def plotTrimVoltage(outputs):

    plt.figure(figsize=(8,6))
    plt.axhline(y=0,color='black',linewidth=2)

    for i in range(0,len(outputs)):

        if i == 0:

            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackVoltage[:,18],
                     color='black',label='VS1U',linewidth=3)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackVoltage[:,19],
                     color='gray',label='VS1L',linewidth=3)

        else:

            if outputs[i].currentTimes[0] > 1.0:

                linestyle = '-'

            else:

                linestyle = '--'

            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackVoltage[:,18],
                     color='black',label=None,linewidth=3,
                     linestyle = linestyle)
            plt.plot(outputs[i].currentTimes,
                     outputs[i].feedbackVoltage[:,19],
                     color='gray',label=None,linewidth=3,
                     linestyle = linestyle)

        axes = plt.gca()

    #axes.set_ylim(-45,45)

    axes.set_xlabel('Time (s)',fontsize=16,labelpad=0)
    axes.set_ylabel('Voltage (kV)',fontsize=16,labelpad=-10)
    plt.tick_params(labelsize=16)

    plt.legend(fontsize=16)

    return

def plotFullDischargePower(outputs):

    plt.figure(figsize=(8,6))
    plt.axhline(y=0,color='black',linewidth=2)

    for i in range(0,len(outputs)):

        if i == 0:
            
            plt.plot(outputs[i].currentTimes,
                     outputs[i].totalPower,
                     color='black',label='Total',linewidth=3)

            

        else:

            if outputs[i].currentTimes[0] > 1.0:

                linestyle = '-'

            else:

                linestyle = '--'

            plt.plot(outputs[i].currentTimes,
                     outputs[i].totalPower,
                     color='black',label=None,linewidth=3,
                     linestyle = linestyle)
            
        
    axes = plt.gca()


    #axes.set_ylim(-45,45)

    axes.set_xlabel('Time (s)',fontsize=16,labelpad=0)
    axes.set_ylabel('Power (MW)',fontsize=16,labelpad=-10)
    plt.tick_params(labelsize=16)

    plt.legend(fontsize=16)

    #plt.savefig('powerV1d.png',format='png',dpi=100)

    return

def plotFlux(outputs):

    plt.figure(figsize=(8,6))

    fluxOffset = outputs[0].flux[0]

    for i in range(0,len(outputs)):

        if outputs[i].fluxTime[0] > 5.0 or i == 0:
            
            fluxPlot = outputs[i].flux - fluxOffset

            linestyle = '-'

        else:

            fluxPlot = outputs[i].flux - outputs[i].flux[0]

            linestyle = '--'
        

        plt.plot(outputs[i].fluxTime, fluxPlot,
                 label='Flux (V-s)', color='dodgerblue',linewidth=2,
                     linestyle = linestyle)

    axes = plt.gca()

    axes.set_xlabel('Time (s)',fontsize=20,labelpad=0)
    axes.set_ylabel('Flux (V-s)',fontsize=20,labelpad=0)

    plt.tick_params(labelsize=16)

    #plt.savefig('fluxV1d.png',format='png',dpi=100)

    return


def plotShaping(outputs):

    plt.figure(figsize=(8,6))

    for i in range(0,len(outputs)):

        if outputs[i].shapeTime[0] > 1.0 or i == 0:

            linestyle = '-'

        else:

            linestyle = '--'

        plt.plot(outputs[i].shapeTime, outputs[i].triangularity95,
                 label='delta95', color='red',linewidth=2,
                 linestyle=linestyle)
        plt.plot(outputs[i].shapeTime, outputs[i].elongation95,
                 label='kappa95', color='blue',linewidth=2,
                 linestyle=linestyle)

    axes = plt.gca()

    #axes.set_ylim(-45,45)

    axes.set_xlabel('Time (s)',fontsize=20,labelpad=-5)
    plt.tick_params(labelsize=16)

    plt.legend(fontsize=16)

    """plt.figure()

    for i in range(0,len(outputs)):

        plt.plot(outputs[i].shapeTime, outputs[i].R0,
                 label='R0', color='red',linewidth=2)
        plt.plot(outputs[i].shapeTime, outputs[i].a,
                 label='a', color='blue',linewidth=2)

    axes = plt.gca()

    #axes.set_ylim(-45,45)

    axes.set_xlabel('Time (s)',fontsize=20,labelpad=-5)
    plt.tick_params(labelsize=16)

    plt.legend(fontsize=16)"""

    plt.figure()

    for i in range(0,len(outputs)):

        if outputs[i].positionTime[0] > 1.0 or i == 0:

            linestyle = '-'

        else:

            linestyle = '--'

        plt.plot(outputs[i].positionTime, outputs[i].zMag*1000.0,
                 label='Zmag', color='red',linewidth=2,
                 linestyle=linestyle)

    axes = plt.gca()

    axes.set_xlabel('Time (s)',fontsize=16,labelpad=-5)
    axes.set_ylabel('Zmag (mm)',fontsize=16,labelpad=0)
    plt.tick_params(labelsize=12)

    plt.legend(fontsize=16)

    plt.figure(figsize=(8,6))

    for i in range(0,len(outputs)):

        if outputs[i].shapeTime[0] > 1.0 or i == 0:

            linestyle = '-'

        else:

            linestyle = '--'

        plt.plot(outputs[i].shapeTime, outputs[i].R0,
                 label='Rgeo', color='red',linewidth=2,
                 linestyle=linestyle)

        plt.plot(outputs[i].positionTime, outputs[i].xMag,
                 label='Rmag', color='orange',linewidth=2,
                 linestyle=linestyle)

    axes = plt.gca()

    axes.set_xlabel('Time (s)',fontsize=20,labelpad=-5)
    axes.set_ylabel('R (m)',fontsize=20,labelpad=0)
    plt.tick_params(labelsize=16)

    plt.legend(fontsize=16)


    return


def plotProfiles(outputs):

    plt.figure(figsize=(8,6))

    
    #plot electron temperature
    for i in range(0, len(outputs)):

        for j in range(0, len(outputs[i].profileTime)):

            plt.plot(outputs[i].rminor[j], (outputs[i].Te[j]/1000.0),
                     label=('%.2f s' % outputs[i].profileTime[j]))

    axes = plt.gca()

    axes.set_xlabel('r (m)',fontsize=16,labelpad=0)
    axes.set_ylabel('Te (keV)',fontsize=16,labelpad=0)
    plt.tick_params(labelsize=12)

    plt.legend(fontsize=10, loc = 'upper right')



    plt.figure(figsize=(8,6))

    #plot electron density
    for i in range(0, len(outputs)):

        for j in range(0, len(outputs[i].profileTime)):

            plt.plot(outputs[i].rminor[j], (outputs[i].ne[j]/1.0e20),
                     label=('%.2f s' % outputs[i].profileTime[j]))

    axes = plt.gca()

    axes.set_xlabel('r (m)',fontsize=16,labelpad=0)
    axes.set_ylabel('ne ($10^{20} m^{-3}$)',fontsize=16,labelpad=0)
    plt.tick_params(labelsize=12)

    plt.legend(fontsize=10, loc = 'upper right')


    return


def saveProfiles(outputs):

    np.save('outputaV2h01-densityProfile.npy', outputs[0].ne)
    np.save('outputaV2h01-temperatureProfile.npy', outputs[0].Te)
    np.save('outputaV2h01-minorRadius.npy', outputs[0].rminor)
    np.save('outputaV2h01-timeBasis.npy', outputs[0].profileTime)

    return

   

if __name__ == '__main__':

    numOutput = len(sys.argv) - 1

    tscOuts = []
    outputFiles = []

    for i in range(1,numOutput+1):

        outputFiles.append(sys.argv[i])

    for i in range(0,numOutput):

        outTemp = tscOutput(outputFiles[i],20)

        tscOuts.append(outTemp)

        tscOuts[i].scrapeCoilGroupCurrents()
        tscOuts[i].scrapeShaping()
        tscOuts[i].interpolateIp()
        tscOuts[i].scrapeProfiles()


    tscOuts[0].estimateStartupCurrents(breakPoint = 0.10)
    tscOuts[0].estimateStartupVoltage(breakPoint = 0.10)

    plotFullDischargeCurrents(tscOuts)
    plotFullDischargeVoltage(tscOuts)
    #plotFullDischargePower(tscOuts)

    plotTrimCurrents(tscOuts)
    plotTrimVoltage(tscOuts)

    plotFlux(tscOuts)
    
    plotProfiles(tscOuts)

    #plotShaping(tscOuts)

    #saveProfiles(tscOuts)

    plt.show()

    ###
    

    """with open('coilCurrentsV2h8T01.txt', 'w') as f:

        newline = '\n'

        f.write('Time (s)  CS1U (MA) CS1L (MA) CS2U (MA) CS2L (MA) CS3U (MA) '
        +'CS3L (MA) PF1U (MA) PF1L (MA) PF2U (MA) PF2L (MA) PF3U (MA) '
        +'PF3L (MA) PF4U (MA) PF4L (MA) Div1U(MA) Div1L(MA) Div2U(MA) '
        +'Div2L(MA) Ip (MA)')
        f.write(newline)

        for i in range(0,numOutput):          

            for j in range(0,len(tscOuts[i].currentTimes)):

                lineString = (('%.3f' % tscOuts[i].currentTimes[j]).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,0]
                                 /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,1]
                                 /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,2]
                                 /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,3]
                                 /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,4]
                                 /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,5]
                                 /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,6]
                                 /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,7]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,8]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,9]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,10]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,11]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,12]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,13]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,14]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,15]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,16]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupCurrents[j,17]
                         /1000)).ljust(10) +
                      ('%.3f' % (tscOuts[i].IpAtCurrentTimes[j]
                                 /1.0e6)).ljust(10)
                      )

                f.write(lineString)
                f.write(newline)"""

    """with open('coilVoltageV2g01.txt', 'w') as f:

        newline = '\n'

        f.write('Time (s)  CS1U (kV) CS1L (kV) CS2U (kV) CS2L (kV) CS3U (kV) '
        +'CS3L (kV) PF1U (kV) PF1L (kV) PF2U (kV) PF2L (kV) PF3U (kV) '
        +'PF3L (kV) PF4U (kV) PF4L (kV) Div1U(kV) Div1L(kV) Div2U(kV) '
        +'Div2L(kV)')
        f.write(newline)

        for i in range(0,numOutput):          

            for j in range(0,len(tscOuts[i].currentTimes)):

                lineString = (('%.3f' % tscOuts[i].currentTimes[j]).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,0]
                                 )).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,1]
                                 )).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,2]
                                 )).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,3]
                                 )).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,4]
                                 )).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,5]
                                 )).ljust(10) +
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,6]
                                 )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,7]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,8]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,9]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,10]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,11]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,12]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,13]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,14]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,15]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,16]
                         )).ljust(10) + 
                      ('%.3f' % (tscOuts[i].coilGroupVoltage[j,17]
                         )).ljust(10)
                      )

                f.write(lineString)
                f.write(newline)"""
                

                
