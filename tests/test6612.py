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

# Task
task1 = Task()
task1.CreateCOPulseChanFreq("Dev1/ctr0", "", DAQmx_Val_Hz, DAQmx_Val_Low, 0.0, 10, 0.5)
task1.CfgImplicitTiming(DAQmx_Val_FiniteSamps, 1)
# task1.SetCOPulseIdleState("Dev1/ctr0", DAQmx_Val_Low)
task1.ExportSignal(DAQmx_Val_CounterOutputEvent, "/Dev2/RTSI0, /Dev1/PFI3")
task1.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

task2 = Task()
task2.CreateCOPulseChanFreq("Dev2/ctr0", "", DAQmx_Val_Hz, DAQmx_Val_Low, 0.0, 1000, 0.5)
task2.CfgDigEdgeStartTrig("/Dev2/RTSI0", DAQmx_Val_Rising)
task2.CfgImplicitTiming(DAQmx_Val_FiniteSamps, 1)
task2.SetStartTrigRetriggerable(True)

task1.StartTask()
task2.StartTask()
print("Started")
time.sleep(30)
task1.StopTask()
task2.StopTask()
task1.ClearTask()
task2.ClearTask()
print("Stopped")
