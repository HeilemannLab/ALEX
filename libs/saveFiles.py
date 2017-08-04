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
from datetime import datetime
import libs.dictionary
import pickle
import libs.plotIllumination


class FileDialogue():
    def __init__(self):
        self._dict = libs.dictionary.UIsettings()
        self._plot = libs.plotIllumination.plotIllumination()

    def refreshSettings(self, dictionary):
        self._dict._a = dictionary

    def SortTasks(self, keyword, filename, data1, data2):
        if keyword == 'load':
            self._dict._a = self.loadDict(filename)
        else:
            # filename = self.createFolder(filename)
            if keyword == 'save':
                self.saveDict(filename)
            if keyword == 'txt':
                self.saveDataToTxt(filename, data1, data2)
            elif keyword == 'hdf5':
                self.saveDataToHDF5(filename)
        return self._dict._a

    def correctRollover(self, data):
        t_start = time.time()
        for i in range(len(data)):
            data[i, 0] = data[i, 0] + (4294967296.0 * data[i, 1])
        t_end = time.time()
        t = t_end - t_start
        print("Rollover correction took %f seconds" % (t))
        return data

    def saveDataToTxt(self, filename, data1, data2):
        data1 = self.correctRollover(data1)
        data2 = self.correctRollover(data2)
        if len(data1) >= len(data2):
            data = np.zeros([len(data1), 2])
            data[:, 0] = data1[:, 0]
            data[0:len(data2), 1] = data2[:, 0]
            print("more green or equal")
        else:
            data = np.zeros([len(data2), 2])
            data[0:len(data1), 0] = data1[:, 0]
            data[:, 1] = data2[:, 0]
        header = datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "\nDuration: " + str(self._dict.getitem("Duration")) + " sec\nLaser alternation frequency: " + str(self._dict.getitem("laser frequency")) + " Hz\nPercentage illumination green: " + str(self._dict.getitem("laser percentageG")) + "\nIter\tGreen channel\tRed channel"
        if filename:
            np.savetxt(filename, data, fmt='%i', delimiter='\t\t', header=header)
        else:
            print("Something wrong with the filename")

    def saveDataToHDF5(self):
        self._planet = 1

    def saveDict(self, fname):
        with open(str(fname + '.p'), "wb") as f:
            pickle.dump(self._dict._a, f)
        with open(str(fname + '.txt'), 'w') as f:
            f.write("Parameters:\n")
        with open(str(fname + '.txt'), 'a') as f:
            for key in self._dict._a:
                line = key + '\t' + str(self._dict._a[key]) + '\n'
                f.write(line)

        self._plot.refreshSettings(self._dict)
        self._plot.plot(fname)

    def loadDict(self, fname):
        if os.path.exists(fname):
            with open(fname, "rb") as f:
                dictionary = pickle.load(f)
            return dictionary
        else:
            print("Error: Empty file!")

    def createFolder(self, filename):
        year = '{:%Y}'.format(datetime.now())
        month = '{:%m}'.format(datetime.now())
        day = '{:%d}'.format(datetime.now())
        folder_name = str(year + '_' + month + '_' + day)
        filename = os.path.split(filename)
        newpath = os.path.join(filename[0], folder_name)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        filename = os.path.join(newpath, filename[1])
        return filename
