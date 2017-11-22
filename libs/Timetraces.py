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


class Timetrace:
    def __init__(self):
        self._green_trace = 0
        self._red_trace = 0
        self._num1 = 0
        self._num2 = 0

    def correctRollover(self, t1, t2):
        int_32 = (2**32) - 1
        t1[:, 0] = t1[:, 0] + (int_32 * t1[:, 1])
        t2[:, 0] = t2[:, 0] + (int_32 * t2[:, 1])
        return t1, t2

    def binnedTrace(self, array):
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
        n_bin = int(np.floor((array[-1] - array[0]) / (1e6)))
        print(n_bin, array[-1])
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
        self._green_trace, self._red_trace = self.correctRollover(self._green_trace, self._red_trace)
        # green_trace = correct2(green_trace)
        # red_trace = correct2(red_trace)

        self._green_trace, self._num1 = self.binnedTrace(self._green_trace[:, 0])
        self._green_trace[:] = [x / 10.0 for x in self._green_trace]   # 10 ms bins
        # green_trace[:] = [x * 10.0 for x in green_trace]   # 100 us bins
        self._num1 = np.arange(self._num1)

        self._red_trace, self._num2 = self.binnedTrace(self._red_trace[:, 0])
        self._red_trace[:] = [x / 10.0 for x in self._red_trace]
        # red_trace[:] = [x * 10.0 for x in red_trace]   # 100 us bins
        self._num2 = np.arange(self._num2)

    def plot(self, directory):
        sns.set_context('paper')
        with sns.axes_style("darkgrid", {'axes.facecolor': '0.7', 'figure.facecolor': '0.7'}):
            fig = plt.figure()
            ax1 = fig.add_subplot(2, 1, 1)
            ax1.plot(self._num1, self._green_trace, 'g')
            ax1.set_ylabel('kHz')
            ax1.set_xlabel('ms')

            ax2 = fig.add_subplot(2, 1, 2)
            ax2.set_xlabel('ms')
            ax2.set_ylabel('kHz')
            ax2.plot(self._num2, self._red_trace, 'r')

            fig.subplots_adjust(hspace=0.5)
            # the savefig should have white facecolor, but can be altered
            plt.savefig(str(directory / 'timetrace.png'))
            plt.show()