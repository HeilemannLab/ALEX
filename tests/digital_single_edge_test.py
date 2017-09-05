'''######################################################################
# File Name: digital_single_edge_test.py
# Project: ALEX
# Version:
# Creation Date: 03/09/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import time
import numpy as np
import ctypes


class DigitalEdge:
    def __init__(self):
        self._data = np.ones([2], dtype=ctypes.c_uint32)
        self._data[:] = [0, 10]
        self._written= int32()

    def configureTask(self):
        # *********************************************/
        # DAQmx Configure Code
        # *********************************************/
        self._task = Task()
        self._task.CreateDOChan(lines="Dev1/port0",
                                nameToAssignToLines="",
                                lineGrouping=DAQmx_Val_ChanForAllLines)
        """
        self._task.CfgSampClkTiming(source="/Dev1/20MHzTimebase",
                                    rate=10.0,
                                    activeEdge=DAQmx_Val_Rising,
                                    sampleMode=DAQmx_Val_FiniteSamps,
                                    sampsPerChan=10)
        """
        # *********************************************/
        # DAQmx Write Code
        # *********************************************/
        self._task.WriteDigitalU32(numSampsPerChan=2,
                                   autoStart=1,
                                   timeout=10.0,
                                   dataLayout=DAQmx_Val_GroupByChannel,
                                   writeArray=self._data,
                                   sampsPerChanWritten=self._written,
                                   reserved=None)

        # *********************************************/
        # DAQmx Start Code
        # *********************************************/
        self._task.StartTask()

    def stopTask(self):
        self._task.StopTask()
        self._task.ClearTask()

if __name__ == '__main__':
    a = DigitalEdge()
    a.configureTask()
    time.sleep(10)
    a.stopTask()
