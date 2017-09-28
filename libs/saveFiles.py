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
import time
import numpy as np
import tables
import libs.dictionary
import pickle
import libs.plotIllumination
import libs.HDFmask
import libs.saveHDF
import pathlib


class SaveFiles:
    """
    This class bundles functions to save datasets, measurements settings and additional
    measurement information in different file formats. It also contains functions to
    convert the raw datasets to photon-hdf5 needs. This means in particular rollover
    correction, merging and sorting the arrays from the two channels and creating a
    corresponding detector mask.
    """
    def __init__(self):
        self._dict = libs.dictionary.UIsettings()
        self._plot = libs.plotIllumination.plotIllumination()
        self._mask = libs.HDFmask.HDFmask()
        self._saveHDF = libs.saveHDF.saveHDF5()

    def refreshSettings(self, dictionary):
        """
        It refreshes the settings dictionary.
        @param dictionary: dict
        """
        self._dict._a.update(dictionary)

    def SortTasks(self, keyword, filename):
        """
        The tasks get sorted by their purpose with is defined by the keyword.
        @param keyword: str
        @param filename: double
        """
        if keyword == 'load':
            self._dict._a = self.loadSettings(filename)
            return self._dict._a
        else:
            if keyword == 'save':
                self.saveSettings(filename)
            elif keyword == 'hdf5':
                self.saveRawData(filename)
            else:
                pass
            return None

    def correctRollover(self, N):
        """
        Correct rollover in the file. It avoids reading all the items into the RAM this way.
        @param N: int
        """
        t_start = time.time()
        int_32 = (2**32) - 1
        filename = "smALEX_APD{}.hdf".format(N)
        f = tables.open_file(filename, 'a')
        f.root.timestamps[:, 0] = f.root.timestamps[:, 0] + (int_32 * f.root.timestamps[:, 1])
        f.flush()   # do not know yet why one needs that, maybe clears allocated RAM
        f.close()
        t_end = time.time()
        t = t_end - t_start
        print("Rollover %i correction took %f seconds" % (N, t))

    def saveRawData(self, path):
        """
        The directory gets specified by user and named by the tag. Then a special folder gets created.
        This should happen before the measurement starts. Also the used settings should be saved in this folder,
        before the measurement. This way it's guaranteed that the used settings are saved, even if the user
        changes settings during the measurement.
        @param path: str
        """
        path = pathlib.Path(path)
        print('2: ', path)
        # directory += time.strftime('%Y_%m_%d_%H_%M')
        folder = path.name
        folder += time.strftime('%Y_%m_%d_%H_%M')
        folder = pathlib.Path(path.parent, folder)
        print('3: ', type(folder), folder)
        folder.mkdir()

        self.saveSetsDict(folder, 'Measurement_settings')
        hdf_dict = self._mask.maskWindow()
        hdf_dict["filename"] = path.name
        self.saveHdfDict(hdf_dict, folder, 'HDF_additional_info')

        self._plot.refreshSettings(self._dict._a)
        self._plot.plot(str(folder) + '/Illumination_scheme.png')
        return folder

    def ConvertToPhotonHDF5(self, files):
        """
        This function does the converting from simple hdf5 files in one nice
        photon-hdf5 file fit for usage with Fretbursts. First the arrays get corrected
        for rollover seperatly in their file, then the arrays are loaded into RAM
        (maybe check size) merged and sorted, and the created one and its corresponding
        detector mask are written into a new hdf file. This one then gets enriched with
        metadata, checked for validity and saved as photon-hdf5 file.
        @param filename: str
        """
        # Rollover correction
        self.correctRollover(1)
        self.correctRollover(2)

        # The arrays have to be written to the RAM, because currently the merging only happens
        # in the RAM, until there's a solution writing on the hdf files only.
        # array 1
        f1 = tables.open_file('smALEX_APD1.hdf', 'r')
        rows1 = f1.root.timestamps[:, 0]
        f1.flush()
        f1.close()

        # array 2
        f2 = tables.open_file('smALEX_APD2.hdf', 'r')
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
        print("Data stored in photon-hdf5.")

    def merge_timestamps(self, t1, t2):
        """
        This method merges the timestamp arrays into one, so it fits to the needs of Fretbursts. In order
        to maintain the information, which timestamp came from which detector, a detector mask is created.
        Returns two ndarrays with sorted timestamps 'tm' and detector ID mask 'mask_t2'.
        @param t1: ndarray
        @param t2: ndarray
        """
        tm = np.hstack([t1, t2])
        index_sort = tm.argsort(kind='mergesort')  # stable sorting
        tm = tm[index_sort]
        mask_t2 = np.hstack([np.zeros(t1.size, dtype=bool),
                             np.ones(t2.size, dtype=bool)])[index_sort]
        return tm, mask_t2

    def saveHdfDict(self, dictionary, folder, filename):
        """
        Saves the additional information needed for photon-hdf5
        files. This should be written after saving the raw data
        and can be changes before converting to raw data files
        to photon-hdf5.
        @param dictionary: dict
        @param folder: str
        @param filename: str
        """
        path = pathlib.Path(folder, filename)
        filename = path.with_suffix('.p')
        with filename.open('wb') as f:
            pickle.dump(dictionary, f)

    def saveSetsDict(self, dictionary, folder, filename):
        """
        Saves the settings of the measurement as txt and pickle file.
        @param: dictionary: dict
        @param folder: str
        @param filename: str
        """
        self.refreshSettings(dictionary)
        path = pathlib.Path(folder, filename)
        # pickle file
        filename = path.with_suffix('.p')
        with filename.open('wb') as f:
            pickle.dump(self._dict._a, f)
        # text file
        filename = path.with_suffix('.txt')
        with filename.open('w') as f:
            f.write("Parameters:\n")
            for key in self._dict._a:
                line = key + '\t' + str(self._dict._a[key]) + '\n'
                f.write(line)

    def loadSetsDict(self, path):
        """
        Loads the dictionary containing measurement settings from a .p pickle file
        and returns a dictionary.
        @param fname: str
        """
        dictionary = None
        path = pathlib.Path(path)
        if not path.is_file():
            print("Error: Empty file or no valid .p file")
        else:
            with path.open("rb") as f:
                dictionary = pickle.load(f)
        return dictionary

if __name__ == '__main__':
    filename = 'saveFiletester.hdf'
    a = SaveFiles()
    a.saveDataToHDF5(filename)
