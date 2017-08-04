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
import ctypes
import numpy as np
import time


class CascadedCounters():
    def __init__(self):
        self._freq = 1000
        self._buffer = int(1e8)
        self.value1 = ctypes.c_ulong(0)
        self.roll1 = ctypes.c_ulong(0)
        self.type = ctypes.c_long(DAQmx_Val_Bit_TriggerUsageTypes_ArmStart)
        self.data = np.zeros([108001, 2])

    def TriggerPulse(self):
        self.trigger = Task()
        self.trigger.CreateCOPulseChanFreq("Dev1/ctr1", "", DAQmx_Val_Hz, DAQmx_Val_Low, 1.0, self._freq, 0.50)
        self.trigger.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
        self.trigger.ExportSignal(DAQmx_Val_CounterOutputEvent, "/Dev1/PFI9")
        self.trigger.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

    def CounterChannels(self):
        self.counter1 = Task()
        self.counter1.CreateCICountEdgesChan("Dev1/ctr0", "", DAQmx_Val_Rising, 0, DAQmx_Val_CountUp)
        self.counter1.SetCICountEdgesTerm("", "/Dev1/20MHzTimebase")

        self.rollover1 = Task()
        self.rollover1.CreateCICountEdgesChan("Dev1/ctr1", "", DAQmx_Val_Rising, 0, DAQmx_Val_CountUp)
        self.rollover1.SetCICountEdgesTerm("", "/Dev1/RTSI0")

    def CounterSampling(self):
        self.counter1.CfgSampClkTiming("/Dev1/PFI8", 1000, DAQmx_Val_Rising, DAQmx_Val_ContSamps, self._buffer)
        self.counter1.ExportSignal(DAQmx_Val_CounterOutputEvent, "/Dev1/RTSI0")
        self.counter1.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

        self.rollover1.SetCIDupCountPrevent("/Dev1/ctr1", True)
        self.rollover1.CfgSampClkTiming("/Dev1/PFI3", 1000, DAQmx_Val_Rising, DAQmx_Val_ContSamps, self._buffer)

    def CounterStartTrig(self):
        self.counter1.SetStartTrigType(DAQmx_Val_DigEdge)
        self.counter1.SetDigEdgeStartTrigSrc("/Dev1/ai/SampleClock")
        self.counter1.SetDigEdgeStartTrigEdge(DAQmx_Val_Rising)

        self.rollover1.SetStartTrigType(DAQmx_Val_DigEdge)
        self.rollover1.SetDigEdgeStartTrigSrc("/Dev1/ai/SampleClock")
        self.rollover1.SetDigEdgeStartTrigEdge(DAQmx_Val_Rising)

    def readCounter(self):
        i = 0
        y = 0
        while i <= 108000:
            self.rollover1.ReadCounterScalarU32(10.00, self.roll1, None)   # Note that 6713 has 24bit counters, 6602 has 32bit counters
            self.counter1.ReadCounterScalarU32(10.00, self.value1, None)
            self.data[i, 1] = self.roll1.value
            self.data[i, 0] = self.value1.value - y
            y = self.value1.value
            i += 1

    def StartCounters(self):
        self.TriggerPulse()
        self.CounterChannels()
        self.CounterStartTrig()
        self.CounterSampling()

        self.trigger.StartTask()
        self.counter1.StartTask()
        self.rollover1.StartTask()

        self.readCounter()

    def stopAll(self):
        self.rollover1.StopTask()
        self.counter1.StopTask()
        self.trigger.StopTask()

        self.rollover1.ClearTask()
        self.counter1.ClearTask()
        self.trigger.ClearTask()

a = CascadedCounters()
t1 = time.time()
a.StartCounters()
a.stopAll()
t2 = time.time()
np.savetxt('resultsfile_armtrig_absVal_1kHz_expSig.txt', a.data)
print(t2 - t1)
