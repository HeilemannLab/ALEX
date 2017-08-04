'''######################################################################
# File Name: Trigtest.py
# Project:
# Version:
# Creation Date: 2017/07/17
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import time


class Trigtest():
    def __init__(self):
        self._freq = 0.5
        self._sampNumber = int(1e3)
        self._buffer = int(1e8)

    def Trigger(self):
        self.trig = Task()
        self.trig.CreateCOPulseChanFreq(counter="Dev2/ctr1",
                                        nameToAssignToChannel="",
                                        units=DAQmx_Val_Hz,
                                        idleState=DAQmx_Val_Low,
                                        initialDelay=0.0,
                                        freq=100,
                                        dutyCycle=0.5)
        self.trig.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
        self.trig.ExportSignal(signalID=DAQmx_Val_CounterOutputEvent,
                               outputTerminal="/Dev2/RTSI0")
        self.trig.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

    def RetrigPuls(self):
        self.retrig = Task()
        self.retrig.CreateCOPulseChanFreq(counter="Dev2/ctr2",
                                          nameToAssignToChannel="",
                                          units=DAQmx_Val_Hz,
                                          idleState=DAQmx_Val_Low,
                                          initialDelay=0.0,
                                          freq=10000,
                                          dutyCycle=0.5)
        self.retrig.CfgDigEdgeStartTrig("/Dev2/RTSI0", DAQmx_Val_Rising)
        self.retrig.CfgImplicitTiming(DAQmx_Val_FiniteSamps, 10)
        self.retrig.SetStartTrigRetriggerable(True)

        # self.retrig.ExportSignal(DAQmx_Val_CounterOutputEvent, "/Dev2/RTSI1, /Dev2/RTSI2, /Dev2/RTSI3, /Dev2/RTSI4")
        # self.retrig.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

a = Trigtest()
a.Trigger()
a.RetrigPuls()

a.trig.StartTask()
a.retrig.StartTask()
time.sleep(30)
a.retrig.StopTask()
a.trig.StopTask()
a.retrig.ClearTask()
a.trig.ClearTask()
