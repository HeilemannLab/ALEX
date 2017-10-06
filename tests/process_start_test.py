'''######################################################################
# File Name: process_start_test.py
# Project: ALEX
# Version:
# Creation Date: 29/08/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import ctypes
import numpy as np
from multiprocessing import Process


class Counter:
    def __init__(self):
        self._freq = 1000
        self._task = None
        self._timing = None
        self._buffer = int(1e8)
        self._num = int(1e6)
        self._readArray = np.zeros([self._num], dtype=ctypes.c_uint32())
        self._read = int32()

        # self.InitCounter()
        # self.InitTiming()

    def InitCounter(self):
        self._task = Task()
        # Channel creation
        self._task.CreateCICountEdgesChan(counter="Dev2/ctr0",
                                          nameToAssignToChannel="",
                                          edge=DAQmx_Val_Rising,
                                          initialCount=0,
                                          countDirection=DAQmx_Val_CountUp)
        self._task.SetCICountEdgesTerm("", "/Dev2/100MHzTimebase")

        # Sampling
        self._task.CfgSampClkTiming(sampsPerChan=self._buffer,
                                    source="/Dev2/PFI39",
                                    rate=1000000,
                                    activeEdge=DAQmx_Val_Rising,
                                    sampleMode=DAQmx_Val_ContSamps)

        # Arm Start trigger
        self._task.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._task.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._task.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

    def InitTiming(self):
        self._timing = Task()
        # Init timing task
        self._timing.CreateCOPulseChanFreq(counter="Dev1/ctr0",
                                           nameToAssignToChannel="",
                                           units=DAQmx_Val_Hz,
                                           idleState=DAQmx_Val_Low,
                                           initialDelay=0.0,
                                           freq=self._freq,
                                           dutyCycle=0.50)
        # Sampling timing
        self._timing.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
        self._timing.ExportSignal(signalID=DAQmx_Val_CounterOutputEvent,
                                  outputTerminal="/Dev2/RTSI0")
        self._timing.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

    def starting(self):
        self.InitCounter()
        self.InitTiming()
        self._task.StartTask()
        self._timing.StartTask()

    def stopping(self):
        self._task.StopTask()
        self._timing.StopTask()
        self._task.ClearTask()
        self._timing.ClearTask()

    def count(self):
        self._task.ReadCounterU32(numSampsPerChan=self._num,
                                  timeout=100.0,
                                  readArray=self._readArray,
                                  arraySizeInSamps=self._num,
                                  sampsPerChanRead=self._read,
                                  reserved=None)


class Processor(Process):
    def __init__(self):
        super(Processor, self).__init__()
        self.daemon = True
        self._counter = Counter()

    def run(self):
        self._counter.starting()
        i = 50
        while i > 0:
            self._counter.count()
            i -= 1
            print(i, self._counter._readArray[0])
        self._counter.stopping()
        print("Measurement done, processor exits.")


if __name__=='__main__':
    process = Processor()
    process.start()
    process.join()
    if process.is_alive():
        print("Sorry still alive.")
    else:
        print("Joined!")
