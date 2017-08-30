'''######################################################################
# File Name: AnalogOutput.py
# Project: ALEX
# Version:
# Creation Date: 2017_07_13
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
import time
from PyDAQmx import *
import libs.dictionary


class GenerateSignal:
    """
    The AnalogOutput class makes the connection to the DAQmx card 6713 (which should be device 1 in NI MAX).
    Laser power sets the voltage height to a percentage between 0V and 5V. Stop method contains a short task
    that sets the channel to zero. It's necessary because tasks would sometimes not go back to zero in idle position.
    The voltages get delivered to pins 22 'Dev1/ao0' (Red) and 21 'Dev1/ao1' (Green).
    """
    def __init__(self):
        self._sampFreq = 2
        self._dict = libs.dictionary.UIsettings()
        self._freq = self._dict._a["laser frequency"]
        self._red = np.zeros([2])
        self._green = np.zeros([2])
        self.read = int32()
        self.redAmp = 0
        self.greenAmp = 0
        self._data = np.array([0])
        self.analog_output = None

    def refreshSettings(self, dictionary):
        self._dict._a.update(dictionary)

    def Intensities(self):
        """
        The laser powers get extracted from the dictionary and converted to values between 0V and 5V.
        The data arrays consist of two values, which are overwritten with the new laser power values.
        Due to bundling of the tasks, the arrays must be concatenated. The data gets written to the
        channels in the order as they are stacked respectively.
        """
        self.redAmp = self._dict._a["lpower red"]
        self.greenAmp = self._dict._a["lpower green"]

        self._red[:] = (self.redAmp * 5.0 / 100.0)
        self._green[:] = (self.greenAmp * 5.0 / 100.0)
        self._data = np.concatenate((self._red, self._green))

    def InitAnalog(self):
        """
        Analog tasks can be bundled and written with one sampling signal. The data is written to the
        channels in the order of the channels are created in the task. Sampling settings are internal
        clock and the laser alterantion frequency.
        """
        self.Intensities()
        self.analog_output = Task()
        self.analog_output.CreateAOVoltageChan(physicalChannel="Dev1/ao0",
                                               nameToAssignToChannel="",
                                               minVal=-10.0,
                                               maxVal=10.0,
                                               units=DAQmx_Val_Volts,
                                               customScaleName=None)
        self.analog_output.CreateAOVoltageChan(physicalChannel="Dev1/ao1",
                                               nameToAssignToChannel="",
                                               minVal=-10.0,
                                               maxVal=10.0,
                                               units=DAQmx_Val_Volts,
                                               customScaleName=None)

        self.analog_output.CfgSampClkTiming(source="",
                                            rate=self._freq,
                                            activeEdge=DAQmx_Val_Rising,
                                            sampleMode=DAQmx_Val_FiniteSamps,
                                            sampsPerChan=self._sampFreq)
        self.analog_output.CfgDigEdgeStartTrig(triggerSource="/Dev1/RTSI2",
                                               triggerEdge=DAQmx_Val_Rising)

        self.analog_output.WriteAnalogF64(numSampsPerChan=self._sampFreq,
                                          autoStart=0,
                                          timeout=-1,
                                          dataLayout=DAQmx_Val_GroupByChannel,
                                          writeArray=self._data,
                                          sampsPerChanWritten=byref(self.read),
                                          reserved=None)

    def startAnalog(self):
        self.analog_output.StartTask()

    def stopAnalog(self):
        """
        After stopping the measurement task, another short task is started and stopped immediately, to make sure
        that the channels are savely set back to zero.
        """
        self.analog_output.StopTask()
        self.analog_output.ClearTask()
        self._data[:] = 0
        self.InitAnalog()
        time.sleep(0.1)
        self.analog_output.StopTask()
        self.analog_output.ClearTask()
