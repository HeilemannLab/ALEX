'''######################################################################
# File Name: rectWave.py
# Project:
# Version:
# Creation Date: 2017/02/09
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
# from scipy import signal
from PyDAQmx import *
import dictionary
import time


class GenerateSignal():
    def __init__(self):
        self._sampFreq = 10
        self._redP = np.zeros([self._sampFreq])
        self._greenP = np.zeros([self._sampFreq])
        self.read = int32()
        self._dict = dictionary.UIsettings()
        self.redAmp = self._dict.getitem("lpower red")
        self.greenAmp = self._dict.getitem("lpower green")
        self._freq = self._dict.getitem("laser frequency")

    def refreshSettings(self, diction):
        self._dict = diction

    def pulseTrain(self):
        self.pulse = Task()
        self.pulse.CreateCOPulseChanFreq("Dev1/ctr0", "", DAQmx_Val_Hz, DAQmx_Val_Low, 0.0, self._freq, 0.50)
        self.pulse.CfgImplicitTiming(DAQmx_Val_ContSamps, 10)

    def calcSignal(self):
        self._redP[0:4] = 1
        self._greenP[5:9] = 1
        self._sig = [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        self._data = np.concatenate((self._redP, self._greenP, self._sig))

    def Analog(self):

        self.output = Task()
        self.output.CreateAOVoltageChan("Dev1/ao0", " ", -10.0, 10.0, DAQmx_Val_Volts, None)
        self.output.CreateAOVoltageChan("Dev1/ao1", " ", -10.0, 10.0, DAQmx_Val_Volts, None)
        self.output.CreateAOVoltageChan("Dev1/ao2", " ", -10.0, 10.0, DAQmx_Val_Volts, None)

        self.output.CfgSampClkTiming(" ", 8 * self._freq, DAQmx_Val_Rising, DAQmx_Val_ContSamps, self._sampFreq)
        self.output.CfgDigEdgeStartTrig("/Dev1/ctr0out", DAQmx_Val_Rising)

        self.output.WriteAnalogF64(numSampsPerChan=self._sampFreq, autoStart=False, timeout=-1, dataLayout=DAQmx_Val_GroupByChannel, writeArray=self._data, reserved=None, sampsPerChanWritten=byref(self.read))

    def Digital(self):

        self.output = Task()
        self.output.CreateDOChan("Dev1/port0/line0", " ", -10.0, 10.0, DAQmx_Val_Volts, None)
        self.output.CreateDOChan("Dev1/port0/line1", " ", -10.0, 10.0, DAQmx_Val_Volts, None)
        self.output.CreateDOChan("Dev1/port0/line2", " ", -10.0, 10.0, DAQmx_Val_Volts, None)

        self.output.CfgSampClkTiming(" ", 8 * self._freq, DAQmx_Val_Rising, DAQmx_Val_ContSamps, self._sampFreq)
        self.output.CfgDigEdgeStartTrig("/Dev1/ctr0out", DAQmx_Val_Rising)

        self.output.WriteDigitalU8(numSampsPerChan=self._sampFreq, autoStart=False, timeout=-1, dataLayout=DAQmx_Val_GroupByChannel, writeArray=self._data, reserved=None, sampsPerChanWritten=byref(self.read))

    def startLaser(self):
        print("laser started")
        # self.silenceAPD()
        self.calcSignal()
        self.pulseTrain()
        self.pulse.StartTask()
        self.Analog()
        self.analog_output.StartTask()

    def stopLaser(self):
        self.analog_output.StopTask()
        self.analog_output.ClearTask()
        self.pulse.StartTask()
        self.pulse.ClearTask()


g = GenerateSignal()
g.startLaser()
time.sleep(20)
g.stopLaser()
