'''######################################################################
# File Name:
# Project:
# Version:
# Creation Date:
# Created By:
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
import makeHDF5
import checkHDF5

filename = 'F:/Karoline/Code/Fretbursts/resultsfile_selfTrigged.txt'
t1 = np.loadtxt(filename, usecols=0)
t2 = t1 + 1

tm = np.hstack([t1, t2])
index_sort = tm.argsort(kind='mergesort', axis=0)  # stable sorting
tm = tm[index_sort]
mask_t2 = np.hstack([np.zeros(t1.size, dtype=bool),
                     np.ones(t2.size, dtype=bool)])[index_sort]
print(tm)
dictionary = dict(
    description='nice file',
    buffer_name='water',
    dye_names='red, blue',
    sample_name='no name',
    num_dyes=2,
    datetime='today',
    author='me',
    author_affiliation='uni')
makeHDF5.makeHDF5(data=tm,
                  filename='testfile',
                  detectorMask=mask_t2,
                  frequency=10,
                  duration=10,
                  dictionary=dictionary)
checkHDF5.checkHDF5(filename='testfile.hdf5')