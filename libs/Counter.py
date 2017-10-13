'''######################################################################
# File Name: Counter.py
# Project: ALEX
# Version:
# Creation Date: 2017/03/13
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import libs.APD
import numpy as np
from multiprocessing import Process


class Counter(Process):
    """
    The counter class is a multiprocessing.Process subclass. It's core
    functionalty is to start the measurement via the APD class in a new
    process. The multiprocessing.Event variable 'running' is the control
    variable which enables control over the while loop from the mainwindow.
    """
    def __init__(self, running, dataQ, readArraySize, semaphore, N):
        """
        @param running: multiprocessing event
        @param dataQ: multiprocessing queue
        @param readArraySize: int
        @param semaphore: multiprocessing Semaphore
        @param: N: int
        """
        super(Counter, self).__init__()
        self.daemon = True
        self._running = running
        self._dataQ = dataQ
        self._readArraySize = readArraySize
        self._data = np.zeros([self._readArraySize, 2], dtype=int)
        self._sem = semaphore
        self._N = N
        self._apd = libs.APD.APD(self._readArraySize, self._N, self._sem)

    def run(self):
        """
        run() is obligatory for subprocesses. In the parent it gets
        called by start(). Here the APD class instance and the
        measurement get started.
        """
        self._apd.startCounting()
        self.Measurement()
        print("Counter %i sent all data and exits." % (self._N))

    def Measurement(self):
        """
        Measurement is conducted as long as self._running is True.
        ReadAPD() delivers a return value, therefore the splitting
        in two lines with the Q.put().
        """
        while self._running.is_set():
            self._data = self._apd.readAPD()
            self._dataQ.put(self._data)
        self._apd.stopCounting()
        self._dataQ.put('STOP')
        self._sem.release()

    def __del__(self):
        print("Counter class instance %i has been removed." % (self._N))
