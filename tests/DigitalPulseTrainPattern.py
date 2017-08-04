'''######################################################################
# File Name:
# Project:
# Version:
# Creation Date:
# Created By:
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import time


""" *********************************************/
// DAQmx Configure Code
********************************************* """
percentHighRed = 0.5
frequency = 10.00
highTime = (1.0 / frequency) * percentHighRed
lowTime = (1.0 / frequency) * (1 - percentHighRed)
initialDelay_green = highTime
highSil = 0.01 / 100000
lowSil = (1 / frequency) - (highSil)
# highSil = (9.9e-8) * (0.000999 / frequency)
# lowSil = (1.0 / frequency) *(1 - highSil)
initialDelay_sil1 = highTime - (0.3 * highSil)
initialDelay_sil2 = initialDelay_green - (0.3 * highSil)


pulse = Task()
pulse.CreateCOPulseChanFreq("Dev1/ctr0", "", DAQmx_Val_Hz, DAQmx_Val_Low, 0.0, frequency, 0.50)
pulse.CfgImplicitTiming(DAQmx_Val_ContSamps, 10)

red = Task()
red.CreateCOPulseChanTime(counter="Dev2/ctr3", nameToAssignToChannel="", units=DAQmx_Val_Seconds, idleState=DAQmx_Val_Low, initialDelay=0.00, lowTime=lowTime, highTime=highTime)
red.CfgDigEdgeStartTrig("/Dev2/PFI39", DAQmx_Val_Rising)
red.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

green = Task()
green.CreateCOPulseChanTime(counter="Dev2/ctr1", nameToAssignToChannel="", units=DAQmx_Val_Seconds, idleState=DAQmx_Val_Low, initialDelay=initialDelay_green, lowTime=highTime, highTime=lowTime)
green.CfgDigEdgeStartTrig("/Dev2/PFI39", DAQmx_Val_Rising)
green.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

sil1 = Task()
sil1.CreateCOPulseChanTime(counter="Dev2/ctr4", nameToAssignToChannel="", units=DAQmx_Val_Seconds, idleState=DAQmx_Val_Low, initialDelay=initialDelay_sil1, lowTime=lowSil, highTime=highSil)
sil1.CfgDigEdgeStartTrig("/Dev2/PFI39", DAQmx_Val_Rising)
sil1.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

sil2 = Task()
sil2.CreateCOPulseChanTime(counter="Dev2/ctr2", nameToAssignToChannel="", units=DAQmx_Val_Seconds, idleState=DAQmx_Val_Low, initialDelay=initialDelay_sil2, lowTime=lowSil, highTime=highSil)
sil2.CfgDigEdgeStartTrig("/Dev2/PFI39", DAQmx_Val_Rising)
sil2.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
""" *********************************************/
// DAQmx Start Code
********************************************* """
i = time.time()
pulse.StartTask()
red.StartTask()
green.StartTask()
sil1.StartTask()
sil2.StartTask()
j = time.time()
t = j - i
print(t)
# print("Starting unsuccessful")
time.sleep(60)

# printf("Generating pulse train. Press Enter to interrupt\n");
# getchar();

""" *********************************************/
// DAQmx Stop Code
********************************************* """
try:
    red.StopTask()
    green.StopTask()
    sil1.StopTask()
    sil2.StopTask()
    pulse.StopTask()
except:
    print("stopping unsuccessful")
k = time.time()
t = k - j
print(t)
red.ClearTask()
green.StopTask()
sil1.ClearTask()
sil2.ClearTask()
pulse.ClearTask()
