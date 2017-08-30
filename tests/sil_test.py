'''######################################################################
# File Name: sil_test.py
# Project: ALEX
# Version:
# Creation Date: 28/08/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import time


frequency = 100000
rate1 = 0.75
rate2 = 1 - rate1
high = (1.0 / frequency) * rate1
low = (1.0 / frequency) * rate2
lowSil = (0.05 / 100000)
highSil = (1.0 / frequency) - lowSil
delaySig = high
delaySil1 = (0.4 * lowSil)
delaySil2 = delaySil1 + high

timing = Task()
timing.CreateCOPulseChanFreq(counter="Dev1/ctr0",
                             nameToAssignToChannel="",
                             units=DAQmx_Val_Hz,
                             idleState=DAQmx_Val_Low,
                             initialDelay=0.00,
                             freq=10,
                             dutyCycle=0.5)
timing.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
timing.ExportSignal(signalID=DAQmx_Val_CounterOutputEvent,
                    outputTerminal="/Dev2/RTSI0")
timing.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

signal1 = Task()
signal1.CreateCOPulseChanTime(counter="Dev2/ctr4",
                              nameToAssignToChannel="",
                              units=DAQmx_Val_Seconds,
                              idleState=DAQmx_Val_Low,
                              initialDelay=0.00,
                              lowTime=low,
                              highTime=high)
signal1.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
signal1.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
signal1.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
signal1.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

signal2 = Task()
signal2.CreateCOPulseChanTime(counter="Dev2/ctr5",
                              nameToAssignToChannel="",
                              units=DAQmx_Val_Seconds,
                              idleState=DAQmx_Val_Low,
                              initialDelay=high,
                              lowTime=high,
                              highTime=low)
signal2.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
signal2.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
signal2.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
signal2.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

sil1 = Task()
sil1.CreateCOPulseChanTime(counter="Dev2/ctr6",
                           nameToAssignToChannel="",
                           units=DAQmx_Val_Seconds,
                           idleState=DAQmx_Val_Low,
                           initialDelay=delaySil1,
                           lowTime=lowSil,
                           highTime=highSil)
sil1.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
sil1.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
sil1.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
sil1.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

sil2 = Task()
sil2.CreateCOPulseChanTime(counter="Dev2/ctr7",
                           nameToAssignToChannel="",
                           units=DAQmx_Val_Seconds,
                           idleState=DAQmx_Val_Low,
                           initialDelay=delaySil2,
                           lowTime=lowSil,
                           highTime=highSil)
sil2.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
sil2.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
sil2.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
sil2.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

signal1.StartTask()
signal2.StartTask()
sil1.StartTask()
sil2.StartTask()
timing.StartTask()
time.sleep(30)
timing.StopTask()
signal1.StopTask()
sil1.StopTask()
signal2.StopTask()
sil2.StopTask()

timing.ClearTask()
signal1.ClearTask()
sil1.ClearTask()
signal2.ClearTask()
sil2.ClearTask()
