'''######################################################################
# File Name: APD.py
# Project: ALEX
# Version:
# Creation Date: 2017_07_13
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import ctypes
import numpy as np


class APD:
    """
    This class generates the interface to the 6612 card, in detail
    the counter input tasks. The 6612 card should be 'Device 2'.
    The number passed by the 'N' parameter determines which counter
    configuration gets initialized and run. The mainwindow starts
    this class twice, once with N=1 for counters 0 and 1, which count
    the signal from the green APD, and with N=2, for counters 2 and 3.
    These ones collect the photons from the red APD.
    """
    def __init__(self, readArraySize, N, semaphore):
        self._sampNumber = readArraySize
        self._N = N
        self._sem = semaphore
        self._buffer = int(1e8)    # 1e8 is possible, no more
        self._value1 = np.zeros([self._sampNumber], dtype=ctypes.c_uint32())
        self._value2 = np.zeros([self._sampNumber], dtype=ctypes.c_uint32())
        self._roll1 = np.zeros([self._sampNumber], dtype=ctypes.c_uint32())
        self._roll2 = np.zeros([self._sampNumber], dtype=ctypes.c_uint32())
        self._data = np.zeros([self._sampNumber, 2])
        self._read = int32()
        self._counter1 = None
        self._counter2 = None
        self._rollover1 = None
        self._rollover2 = None

    def startCounting(self):
        """
        Four counters are set up in pairs, all counting edges.
        Counters 0 and 1 work together, and so do counters 2
        and 3. They form 'cascaded counters' or a '64bit counter'.
        Counters 0 and 2 count the card's internal 100MHzTimebase
        on their source terminal, which acts as time source for
        timestamps. The counters are gated by the TTL signal from
        the APDs. That means they count up the internal clock and
        everytime a photon-TTL arrives, the current count gets
        written to the buffer. The counters fill up an array with
        those values and return it to the computer. The size of
        the array is the 'readArraySize' parameter, which can be
        changed in the main loop. The counters are 32bit ones, so
        precisely every 42.95 seconds (2**32 / 100000000) they roll
        over, which means they start at zero again. The counters 1
        and 3 track the rollover by the 'terminal count' pulse,
        which a counters emit prior to a rollover event. The
        counters 0 and 1, and 2 and 3 are gated by the same APD, so
        for every timestamp entry in an array there is tracked, how
        many rollovers have taken place before. The size of the array
        also determines, how much the measured time deviates from
        the given measurement duration, since the card can only be
        stopped after finishing an array. Also a semaphore gets
        passed to the instances and the internal lock gets acquired.
        The main loop can count the times the semaphore lock got
        acquired, so it senses when the laser and the two detectors
        subprocesses got initialized.
        """
        if self._N == 1:
            self.InitializeCounter1()
            self.SamplingCounter1()
            self.ArmStartCounter1()
            self._sem.acquire()
            self._rollover1.StartTask()
            self._counter1.StartTask()
        else:
            self.InitializeCounter2()
            self.SamplingCounter2()
            self.ArmStartCounter2()
            self._sem.acquire()
            self._rollover2.StartTask()
            self._counter2.StartTask()
        # Important note for arm start trigger:
        # Always start trigger pulse AFTER counter tasks, else NO SYNC!

    def InitializeCounter1(self):
        """
        Task channels get configured to count edges. Counter 0 exports
        its signal to the counter 1 source PFI so that 1 recognizes the
        'terminal count' signal. Configuring the exported signal to
        'pulse is important, since default is 'toggle', which just
        changes the state of the digital line. NI recommends to configure
        the 'Duplicate count prevention' for edge counting tasks, that
        have an unstable sample clock (gate). The 'Sample Clock Overrun
        Behavior' prevents an unusual behavior when gating signal arrives
        faster than the source signal (internal clock).
        """
        self._counter1 = Task()
        self._counter1.CreateCICountEdgesChan(counter="Dev2/ctr0",
                                              nameToAssignToChannel="",
                                              edge=DAQmx_Val_Rising,
                                              initialCount=0,
                                              countDirection=DAQmx_Val_CountUp)
        self._counter1.SetCICountEdgesTerm("", "/Dev2/100MHzTimebase")

        self._rollover1 = Task()
        self._rollover1.CreateCICountEdgesChan(counter="Dev2/ctr1",
                                               nameToAssignToChannel="",
                                               edge=DAQmx_Val_Rising,
                                               initialCount=0,
                                               countDirection=DAQmx_Val_CountUp)
        self._rollover1.SetCICountEdgesTerm("", "/Dev2/PFI35")

        self._counter1.SetCIDupCountPrevent("/Dev2/ctr0", True)
        self._rollover1.SetCIDupCountPrevent("/Dev2/ctr1", True)

        self._counter1.ExportSignal(signalID=DAQmx_Val_CounterOutputEvent,
                                    outputTerminal="/Dev2/PFI35")
        self._counter1.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

        self._counter1.SetSampClkOverrunBehavior(data=DAQmx_Val_IgnoreOverruns)
        self._rollover1.SetSampClkOverrunBehavior(data=DAQmx_Val_IgnoreOverruns)

    def InitializeCounter2(self):
        """
        Configures the same functionality as the method above, but for
        counters 2 and 3
        """
        self._counter2 = Task()
        self._counter2.CreateCICountEdgesChan(counter="Dev2/ctr2",
                                              nameToAssignToChannel="",
                                              edge=DAQmx_Val_Rising,
                                              initialCount=0,
                                              countDirection=DAQmx_Val_CountUp)
        self._counter2.SetCICountEdgesTerm("", "/Dev2/100MHzTimebase")

        self._rollover2 = Task()
        self._rollover2.CreateCICountEdgesChan(counter="Dev2/ctr3",
                                               nameToAssignToChannel="",
                                               edge=DAQmx_Val_Rising,
                                               initialCount=0,
                                               countDirection=DAQmx_Val_CountUp)
        self._rollover2.SetCICountEdgesTerm("", "/Dev2/PFI27")

        self._counter2.SetSampClkOverrunBehavior(data=DAQmx_Val_IgnoreOverruns)
        self._rollover2.SetSampClkOverrunBehavior(data=DAQmx_Val_IgnoreOverruns)

        self._counter2.SetCIDupCountPrevent("/Dev2/ctr2", True)
        self._rollover2.SetCIDupCountPrevent("/Dev2/ctr3", True)

        self._counter2.ExportSignal(signalID=DAQmx_Val_CounterOutputEvent,
                                    outputTerminal="/Dev2/PFI27")
        self._counter2.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

    def SamplingCounter1(self):
        """
        Sampling of all four counters is set to external sample clock,
        which is the signal of their APD respectively. The signal should
        be received by the gate terminal. The 'sampsPerChanToAcquire'
        parameter keyword is shortened to 'sampsPerChan' by the pydaqmx
        library.
        This method samples counters 0 and 1
        """
        self._counter1.CfgSampClkTiming(sampsPerChan=self._buffer,
                                        source="/Dev2/PFI38",
                                        rate=10000000,
                                        activeEdge=DAQmx_Val_Rising,
                                        sampleMode=DAQmx_Val_ContSamps)
        self._rollover1.CfgSampClkTiming(sampsPerChan=self._buffer,
                                         source="/Dev2/PFI38",
                                         rate=10000000,
                                         activeEdge=DAQmx_Val_Rising,
                                         sampleMode=DAQmx_Val_ContSamps)

    def SamplingCounter2(self):
        """
        This method contains the same functionality as the one above,
        but for counters 2 and 3.
        """
        self._counter2.CfgSampClkTiming(source="/Dev2/PFI30",
                                        rate=10000000,
                                        activeEdge=DAQmx_Val_Rising,
                                        sampleMode=DAQmx_Val_ContSamps,
                                        sampsPerChan=self._buffer)

        self._rollover2.CfgSampClkTiming(source="/Dev2/PFI30",
                                         rate=10000000,
                                         activeEdge=DAQmx_Val_Rising,
                                         sampleMode=DAQmx_Val_ContSamps,
                                         sampsPerChan=self._buffer)

    def ArmStartCounter1(self):
        """
        Arm start trigger makes the counters wait for an external signal
        before starting. Trigger signal is the timing task from the 6713
        card over a RTSI. But counters should all be started first,
        otherwise they maybe start at different edges or wait infinitely.
        This method configures trigger for counters 0 and 1.
        """
        self._counter1.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._rollover1.SetArmStartTrigType(data=DAQmx_Val_DigEdge)

        self._counter1.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._rollover1.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)

        self._counter1.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._rollover1.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

    def ArmStartCounter2(self):
        """
        This method configures trigger for counters 2 and 3.
        """
        self._counter2.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._rollover2.SetArmStartTrigType(data=DAQmx_Val_DigEdge)

        self._counter2.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._rollover2.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)

        self._counter2.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._rollover2.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

    def readAPD(self):
        """
        Full arrays get passed to the computer and timestamps and
        their rollover track get aligned.
        """
        if self._N == 1:
            self.actualCounting(self._rollover1, self._roll1)
            self.actualCounting(self._counter1, self._value1)
            self._data[:, 1] = self._roll1[:]
            self._data[:, 0] = self._value1[:]
        else:
            self.actualCounting(self._rollover2, self._roll2)
            self.actualCounting(self._counter2, self._value2)
            self._data[:, 1] = self._roll2[:]
            self._data[:, 0] = self._value2[:]
        return self._data

    def actualCounting(self, task, readArray):
        """
        Read the data from the cards queue into 'readArray'.
        Timeout is the time to wait until the last samples are
        written. Returns the readArray.
        @param task: task name
        @param readArray: ndarray
        """
        task.ReadCounterU32(numSampsPerChan=self._sampNumber,
                            timeout=50.0,
                            readArray=readArray,
                            arraySizeInSamps=self._sampNumber,
                            sampsPerChanRead=self._read,
                            reserved=None)
        return readArray

    def stopCounting(self):
        """Stop and clear tasks."""
        if self._N == 1:
            self._rollover1.StopTask()
            self._counter1.StopTask()
            self._rollover1.ClearTask()
            self._counter1.ClearTask()
        else:
            self._rollover2.StopTask()
            self._counter2.StopTask()
            self._rollover2.ClearTask()
            self._counter2.ClearTask()
