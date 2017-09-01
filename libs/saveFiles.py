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
import libs.dictionary
import pickle
import libs.plotIllumination
import libs.HDFmask
import libs.saveHDF


class FileDialogue:
    """
    This class hosts several methods to save the dataset in differents file types.
    Currently only the saveDataToHDF works agreeable. Considering the expected size
    of datasets it is arguable if saving in .txt format makes sense.
    """
    def __init__(self):
        self._dict = libs.dictionary.UIsettings()
        self._plot = libs.plotIllumination.plotIllumination()
        self._mask = libs.HDFmask.HDFmask()
        self._saveHDF = libs.saveHDF.saveHDF5()
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
            if keyword == 'save':
                self.saveDict(filename)
            if keyword == 'txt':
                pass
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
        f.flush()   # do not know yet why one needs that, maybe clears allocated RAM
        f.close()
        t_end = time.time()
        t = t_end - t_start
        print("Rollover %i correction took %f seconds" % (N, t))

    def saveDataToHDF5(self, filename):
        """
        This method calls the rollover correction and currently reads the arrays into RAM in order to apply
        the 'merge_timestamps' method from Antonino Ingargiola. The merged dataset and the detector mask get
        then saved to another .hdf file.
        """
        if filename:
            # Save dict and alternation plot
            # self.saveDict(filename)
            self._mask.maskWindow()
            print(self._mask._dict)
            self.addArrays(filename)

        else:
            print("No valid filename.")

    def addArrays(self, filename):
            # Rollover correction
            # self.correctRollover(1)
            # self.correctRollover(2)

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

            # merge the two arrays into one, create detector mask
            data, detector_mask = self.merge_timestamps(rows1, rows2)

            # open to append rest oft required dict and convert to photon-hdf5
            self._mask._dict["timestamps_reference"] = data
            self._mask._dict["detectors_reference"] = detector_mask
            # self._mask._dict["acquisition_duration"] = self._dict._a["Duration"]

            self._saveHDF.assembleDictionary(self._mask._dict)
            self._saveHDF.saveAsHDF(filename)
            print("Array stored")

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
