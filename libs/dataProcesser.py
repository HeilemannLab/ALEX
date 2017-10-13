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
import tables


class DataProcesser(Process):
    """
    The dataProcesser class is a subclass of multiprocessing.Process.
    It's main function is to process data in rates for animation and to
    write it into an hdf5 file, if mode is 'finite'. The hdf format is
    accessed by the pytables library, and features fast write rates and
    good compression. So overfilling the RAM is avoided and the data is
    secured. The files get stored in a loaction specified by the user.
    If the mode is 'continuous' not data gets saved.
    """
    def __init__(self, dataQ, animDataQ, readArraySize, N, folder):
        """
        @param dataQ: multiprocessing queue
        @param animDataQ: multiprocessing queue
        @param readArraySize: int
        @param N: int
        """
        super(DataProcesser, self).__init__()
        self.daemon = True
        self._dataQ = dataQ
        self._readArraySize = readArraySize
        self._animDataQ = animDataQ
        self._N = N
        self._folder = folder
        self._timestamps = np.zeros([1, 2], dtype=int)
        self._int_max = (2**32) - 1

    def run(self):
        """
        When folder is None, the measurement mode is continuous,
        so data must not be saved. If there's a folder, data gets
        saved there.
        """
        if (self._folder == 'Cont') or (self._folder is None):
            self.dataProcessing_cont()
        else:
            self.dataProcessing_finite()
        self._animDataQ.close()

    def dataProcessing_cont(self):
        """
        DataQ sends a string sentinel, first and last array entry get corrected
        by rollover count. Count rate entry/dt is send via animDataQ and lcdQ.
        Data does NOT get saved.
        """
        for array in iter(self._dataQ.get, 'STOP'):
            n1 = array[0, 0] + (self._int_max * array[0, 1])
            n2 = array[-1, 0] + (self._int_max * array[-1, 1])
            self._animDataQ.put(self._readArraySize / (n2 - n1))
        print("DataProcesser %i sent all data and exits" % self._N)

    def dataProcessing_finite(self):
        """
        DataQ sends a string sentinel, first and last array entry get corrected
        by rollover count. Count rate entry/dt is send via animDataQ and lcdQ.
        Array gets appended to hdf file array.
        """
        filename = str(self._folder / "smALEX_APD{}.hdf".format(self._N))
        f = tables.open_file(filename, mode='w')
        atom = tables.UInt32Atom()
        filters = tables.Filters(complevel=6, complib='zlib')
        timestamps = f.create_earray(f.root,
                                     'timestamps',
                                     atom=atom,
                                     shape=(0, 2),
                                     filters=filters)
        for array in iter(self._dataQ.get, 'STOP'):
            timestamps.append(array)
            n1 = array[0, 0] + (self._int_max * array[0, 1])
            n2 = array[-1, 0] + (self._int_max * array[-1, 1])
            self._animDataQ.put(self._readArraySize / (n2 - n1))
        f.flush()
        f.close()
        print("DataProcesser %i sent all data and exits" % self._N)

    def __del__(self):
        print("DataProcesser class instance %i has been removed." % self._N)
