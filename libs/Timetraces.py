'''######################################################################
# File Name: timetraces.py
# Project: ALEX
# Version:
# Creation Date: 07/11/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
import tables
import matplotlib.pyplot as plt
import pathlib
import seaborn as sns


class Timetrace:
    """
    The timetrace class provides a binned timetrace of
    raw data on hdf files. It is specially tailored to the
    application (file names). It contains methods to load
    data in RAM using numpy arrays, to correct for rollover
    in RAM, to bin timestamps in 10ms bins and adjust values
    to kHz, and to plot the data on a matplotlib/seaborn graph.
    """
    def __init__(self):
        self._green_trace = 0
        self._red_trace = 0
        self._num1 = 0
        self._num2 = 0

    def correctRollover(self, t1, t2):
        """
        Numpy arrays get corrected for rollover, using
        the rollover tracking. This applies specifically
        to 32bit counters.
        @param t1: ndarray
        @param t2: ndarray
        @return t1: ndarray
        @return t2: ndarray
        """
        int_32 = (2**32) - 1
        t1[:, 0] = t1[:, 0] + (int_32 * t1[:, 1])
        t2[:, 0] = t2[:, 0] + (int_32 * t2[:, 1])
        return t1, t2

    def binnedTrace(self, array):
        """
        Timestamps get binned in bins of the size 10ms.
        The parameter bins gets augmented as long the
        data is in the n*1e6 window. If it reaches the
        limit, bins gets written to trace and reset,
        and the window counter n gets augmented.
        @param array: ndarray
        @return trace: list
        @return n: int
        """
        trace = []
        n = 1
        bins = 0
        for i in range(len(array)):
            bins += 1
            if array[i] >= (n * 1e6):
                trace.append(bins)
                n += 1
                bins = 0
        return trace, n - 1

    def binnedTrace1(self, array):
        """
        n_bin calculate the expected bin number, used
        as size for trace. The data gets binned in 10 ms
        bins again, this time using a while loop. The
        advantage of this method is the ndarrays (better
        than list.append), disadvantage is a sensitivity
        to rollover errors (you'll see just zeros
        after the error)
        """
        n_bin = int(np.floor((array[-1] - array[0]) / (1e6)))
        trace = np.zeros([n_bin, 1], dtype=np.int64)
        j = 0
        for i in range(len(trace)):
            bins = 0
            t_m = (i + 1) * 1e6
            while (array[j] < t_m):    # and (array[j] >= t_m - (1e5)):
                bins += 1
                j += 1
            trace[i] = bins
        return trace, n_bin

    def doThings(self, directory):
        """
        Opens files in directory and reads timestamp arrays
        into RAM, the datatype np.float is an float64, so
        rollover corrections can take place (the data is
        stored intially in int32 in the files, making
        rollover correction impossible). Invoke methods
        process and plot on the arrays.
        @param directory: pathlib.Path
        """
        filename = str(directory / 'smALEX_APD1.hdf')
        f = tables.open_file(filename, 'r')
        self._green_trace = np.array(f.root.timestamps[:, :], dtype=np.float)
        f.flush()
        f.close()

        filename = str(directory / 'smALEX_APD2.hdf')
        f = tables.open_file(filename, 'r')
        self._red_trace = np.array(f.root.timestamps[:, :], dtype=np.float)
        f.flush()
        f.close()

        self.process()
        self.plot(directory)

    def process(self):
        """
        Corrects rollover and bins data, recalculates
        results to kHz. Converts number of bins into
        an array, as x-axis for the plot.
        """
        self._green_trace, self._red_trace = self.correctRollover(self._green_trace, self._red_trace)

        self._green_trace, self._num1 = self.binnedTrace(self._green_trace[:, 0])
        self._green_trace[:] = [x / 10.0 for x in self._green_trace]   # 10 ms bins
        self._num1 = np.arange(self._num1)

        self._red_trace, self._num2 = self.binnedTrace(self._red_trace[:, 0])
        self._red_trace[:] = [x / 10.0 for x in self._red_trace]
        self._num2 = np.arange(self._num2)

    def plot(self, directory):
        """
        Plots the data and saves the figure as *.png into directory
        @param directory: pathlib.Pat
        """
        sns.set_context('paper')
        with sns.axes_style("darkgrid", {'axes.facecolor': '0.7', 'figure.facecolor': '0.7'}):
            fig = plt.figure()
            ax1 = fig.add_subplot(2, 1, 1)
            ax1.plot(self._num1, self._green_trace, 'g')
            ax1.set_ylabel('kHz')
            ax1.set_xlabel('10 ms')

            ax2 = fig.add_subplot(2, 1, 2)
            ax2.set_xlabel('10 ms')
            ax2.set_ylabel('kHz')
            ax2.plot(self._num2, self._red_trace, 'r')

            fig.subplots_adjust(hspace=0.5)
            # the savefig should have white facecolor, but can be altered
            plt.savefig(str(directory / 'timetrace.png'))
            plt.show()
