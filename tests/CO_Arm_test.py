'''######################################################################
# File Name: CO_Arm_test.py
# Project:
# Version:
# Creation Date: 2017_07_20
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import time

timingPuls = Task()
timingPuls.CreateCOPulseChanFreq(counter="Dev1/ctr0",
                                 nameToAssignToChannel="",
                                 units=DAQmx_Val_Hz,
                                 idleState=DAQmx_Val_Low,
                                 initialDelay=0.0,
                                 freq=10000,
                                 dutyCycle=0.50)
timingPuls.CfgImplicitTiming(DAQmx_Val_ContSamps, 10000)
timingPuls.ExportSignal(signalID=DAQmx_Val_CounterOutputEvent,
                        outputTerminal="/Dev2/RTSI0, /Dev2/PFI28")
timingPuls.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)


                
green = Task()
green.CreateCOPulseChanTime(counter="Dev2/ctr1",
                            nameToAssignToChannel="",
                            units=DAQmx_Val_Seconds,
                            idleState=DAQmx_Val_Low,
                            initialDelay=0.00,
                            lowTime=0.3,
                            highTime=0.7)
# green.CfgDigEdgeStartTrig("/Dev2/RTSI0", DAQmx_Val_Rising)
green.CfgImplicitTiming(DAQmx_Val_ContSamps, 10)

green.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
green.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
green.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

t1 = time.time()
green.StartTask()
timingPuls.StartTask()
print("Started")
time.sleep(30)

green.StopTask()
print("Stopped")
green.ClearTask()
timingPuls.StopTask()
timingPuls.ClearTask()
t2 = time.time()
print("30s sleeps means %f s in daqmx time" % (t2 - t1))
