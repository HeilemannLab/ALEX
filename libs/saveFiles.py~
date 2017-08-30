'''######################################################################
# File Name: saveFiles.py
# Project: ALEX
# Version:
# Creation Date: 2017/07/30
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import os
import time
import numpy as np
import tables
from datetime import datetime
import libs.dictionary
import pickle
import libs.plotIllumination


class FileDialogue:
    """
    This class hosts several methods to save the dataset in differents file types.
    Currently only the saveDataToHDF works agreeable. Considering the expected size
    of datasets it is arguable if saving in .txt format makes sense.
    """
    def __init__(self):
        self._dict = libs.dictionary.UIsettings()
        self._plot = libs.plotIllumination.plotIllumination()
        self._planet = 0

    def refreshSettings(self, dictionary):
        self._dict._a.update(dictionary)

    def SortTasks(self, keyword, filename):
        """
        @param keyword: str
        @param filename: double
        """
        if keyword == 'load':
            self._dict._a = self.loadDict(filename)
            return self._dict._a
        else:
            # filename = self.createFolder(filename)
            if keyword == 'save':
                self.saveDict(filename)
            if keyword == 'txt':
                pass
                # self.saveDataToTxt(filename)
            elif keyword == 'hdf5':
                self.saveDataToHDF5(filename)
            return None

    def correctRollover(self, N):
        """
        Correct rollover in the file. It avoids reading all the items into the RAM this way.
        @param N: int
        """
        t_start = time.time()
        filename = "tempAPD{}.hdf".format(N)
        f = tables.open_file(filename, 'a')
        f.root.timestamps[:, 0] = f.root.timestamps[:, 0] + (4294967296.0 * f.root.timestamps[:, 1])
        f.flush()   # do not know yet why one needs that
        f.close()
        t_end = time.time()
        t = t_end - t_start
        print("Rollover %i correction took %f seconds" % (N, t))

    def saveDataToTxt(self, filename):
        """
        Saves data to .txt file. But therefore the whole array would have to be read into the RAM,
        which can cause severe problems. It's not completed yet.
        """
        self.correctRollover(1)
        self.correctRollover(2)
        """
        if len(data1) >= len(data2):
            data = np.zeros([len(data1), 2])
            data[:, 0] = data1[:, 0]
            data[0:len(data2), 1] = data2[:, 0]
            print("more green or equal")
        else:
            data = np.zeros([len(data2), 2])
            data[0:len(data1), 0] = data1[:, 0]
            data[:, 1] = data2[:, 0]
        """
        data = [0]
        header = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                     + "\nDuration: "
                     + str(self._dict._a["Duration"])
                     + " sec\nLaser alternation frequency: "
                     + str(self._dict._a["laser frequency"])
                     + " Hz\nPercentage illumination green: "
                     + str(self._dict._a["laser percentageG"])
                     + "\nIter\tGreen channel\tRed channel")

        if filename:
            np.savetxt(filename, data, fmt='%i', delimiter='\t\t', header=header)
        else:
            print("Something wrong with the filename.")

    def saveDataToHDF5(self, filename):
        """
        This method calls the rollover correction and currently reads the arrays into RAM in roder to apply
        the 'merge_timestamps' method from Antonino Ingargiola. The merged dataset and the detector mask get
        then saved to another .hdf file.
        """
        if filename:
            # Save dict and alternation plot
            self.saveDict(filename)
            # Rollover correction
            self.correctRollover(1)
            self.correctRollover(2)
            # The arrays have to be written to the RAM, because currently the merging only happens
            # in the RAM, until there's a solution writing on the hdf files only.
            # array 1
            f1 = tables.open_file('tempAPD1.hdf', 'r')
            rows1 = f1.root.timestamps[:, 0]
            f1.flush()
            f1.close()
            # array 2
            f2 = tables.open_file('tempAPD2.hdf', 'r')
            rows2 = f2.root.timestamps[:, 0]
            f2.flush()
            f2.close()
            # new array
            hour = '{:%H}'.format(datetime.now())
            minute = '{:%M}'.format(datetime.now())
            filename = "{}_{}_{}.hdf".format(filename, hour, minute)
            data, detector_mask = self.merge_timestamps(rows1, rows2)
            outFile = tables.open_file(filename, 'w')
            # atom = tables.UInt32Atom()
            filters = tables.Filters(complevel=6, complib='zlib')
            # photon_data group, timestamps and detector mask array creation
            outFile.create_group('/', 'photon_data')
            outFile.create_carray(where='/photon_data', name='timestamps', obj=data, filters=filters)
            outFile.create_carray(where='/photon_data', name='detectors', obj=detector_mask, filters=filters)

            # here antoninos save photon thing can happen, it also works an opened file and existing tables.arrays
            outFile.flush()
            outFile.close()
            print("Array stored, file closed")
        else:
            print("No valid filename.")

    def merge_timestamps(self, t1, t2):
        """
        This method merges the timestamp arrays into one, so it fits to the needs of Fretbursts. In order
        to maintain the information, which item came from which detector a detector mask is created, which
        also can be fed to Fretbursts.
        @param t1: ndarray
        @param t2: ndarray
        """
        tm = np.hstack([t1, t2])
        index_sort = tm.argsort(kind='mergesort')  # stable sorting
        tm = tm[index_sort]
        mask_t2 = np.hstack([np.zeros(t1.size, dtype=bool),
                             np.ones(t2.size, dtype=bool)])[index_sort]
        return tm, mask_t2

    def saveDict(self, fname):
        """
        Saves the parameters as pickle file (.p) and also as a readable .txt file.
        It further calls the plotIllumination class to create a .png file showing
        the laser illumination pattern.
        @param fname: str
        """
        with open(str(fname + '.p'), "wb") as f:
            pickle.dump(self._dict._a, f)
        with open(str(fname + '.txt'), 'w') as f:
            f.write("Parameters:\n")
        with open(str(fname + '.txt'), 'a') as f:
            for key in self._dict._a:
                line = key + '\t' + str(self._dict._a[key]) + '\n'
                f.write(line)

        self._plot.refreshSettings(self._dict._a)
        self._plot.plot(fname)

    def loadDict(self, fname):
        """
        Loads the dictionary from a .p pickle file and returns a dictionary.
        @param fname: str
        """
        if os.path.exists(fname):
            with open(fname, "rb") as f:
                dictionary = pickle.load(f)
            return dictionary
        else:
            print("Error: Empty file!")

if __name__ == '__main__':
    filename = 'saveFiletester.hdf'
    a = FileDialogue()
    a.saveDataToHDF5(filename)
