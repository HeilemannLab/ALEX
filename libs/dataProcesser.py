'''######################################################################
# File Name: dataProcesser.py
# Project: ALEX
# Version:
# Creation Date: 2017/07/17
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
from multiprocessing import Process


class DataProcesser(Process):
    def __init__(self, dataQ, animDataQ, resultQ, readArraySize, N):
        super(DataProcesser, self).__init__()
        self.daemon = True
        self._dataQ = dataQ
        self._resultQ = resultQ
        self._readArraySize = readArraySize
        self._animDataQ = animDataQ
        self._N = N
        self._timestamps = np.zeros([1, 2], dtype=int)

    def run(self):
        self.dataProcessing()

    def dataProcessing(self):
        # DataQueue sends a string sentinel, first and last array entry get corrected by rollover count.
        # Count rate entry/dt is send via animQueue and lcdQ.
        array = object()
        for array in iter(self._dataQ.get, 'STOP'):
            self._timestamps = np.concatenate((self._timestamps, array))
            n1 = array[0, 0] + (4294967296.0 * array[0, 1])
            n2 = array[-1, 0] + (4294967296.0 * array[-1, 1])
            n3 = self._readArraySize / (n2 - n1)
            self._animDataQ.put(n3)

        self._resultQ.put(self._timestamps)
        print("DataProcesser %i sent all data and exits" % ((self._N)))

    def __del__(self):
        print("DataProcesser class instance %i has been removed." % ((self._N)))
