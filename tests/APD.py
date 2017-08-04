'''######################################################################
# File Name: APDcounters.py
# Project:
# Version:
# Creation Date: 2017/03/14
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import ctypes
# import libs.dictionary
import libs.dictionary


class APD():
    def __init__(self):

        self._dict = libs.dictionary.UIsettings()
        self.r1 = ctypes.c_ulong(0)
        self.r2 = 0
        self.r3 = 0
        self.g1 = ctypes.c_ulong(0)
        self.g2 = 0
        self.g3 = 0
        self._active = False
        self._freq = self._dict.getitem("laser frequency")
        self._time = self._dict.getitem("Duration")
        self._buf = int(100000000)
        # self.counting_green = Task()
        # self.counting_red = Task()

    def refreshSettings(self, dictionary):
        self._dict._a = dictionary

    def startCounting(self):
        self.counting_green = Task()
        self.counting_green.CreateCICountEdgesChan("Dev2/ctr1", "", DAQmx_Val_Rising, 0, DAQmx_Val_CountUp)
        self.counting_green.SetCICountEdgesTerm("", "/Dev2/PFI35")
        self.counting_green.CfgSampClkTiming("/Dev2/PFI39", 10000, DAQmx_Val_Rising, DAQmx_Val_ContSamps, self._buf)

        # PFI 39 für laser clock (ctr0 source), PFI 32 (ctr1 out)/ PFI 35 (ctr1 source) oder PFI 34 (ctr1 gate) für counter clock

        self.counting_red = Task()
        self.counting_red.CreateCICountEdgesChan("Dev2/ctr2", "", DAQmx_Val_Rising, 0, DAQmx_Val_CountUp)
        self.counting_red.SetCICountEdgesTerm("", "/Dev2/PFI31")
        self.counting_red.CfgSampClkTiming("/Dev2/PFI39", 10000, DAQmx_Val_Rising, DAQmx_Val_ContSamps, self._buf)

        self.counting_green.StartTask()
        self.counting_red.StartTask()

    def resetCounter(self):
        self.r2 = 0
        self.r3 = 0
        self.g2 = 0
        self.g3 = 0

    def readAPD(self):
        self.counting_green.ReadCounterScalarU32(10.00, self.g1, None)
        self.counting_red.ReadCounterScalarU32(10.00, self.r1, None)
        self.g3 = self.g1.value - self.g2
        self.r3 = self.r1.value - self.r2
        self.r2 = self.r1.value
        self.g2 = self.g1.value
        return self.g3, self.r3

    def stopCounting(self):
        self.counting_green.StopTask()
        self.counting_red.StopTask()

        self.counting_green.ClearTask()
        self.counting_red.ClearTask()
