'''######################################################################
# File Name: new_approach_merge.py
# Project: ALEX
# Version:
# Creation Date: 07/09/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import tables
import sys
import numpy as np
import time


def merge_files():
    """Merging without rollover correction"""
    # file 1, apd1
    f1 = tables.open_file('tempAPD1.hdf', 'r')
    ts_1 = f1.root.timestamp

    # file 2, apd2
    f2 = tables.open_file('tempAPD2.hdf', 'r')
    ts_2 = f2.root.timestamps

    # lengths
    f1_num = self.f1.root.timestamps.nrows   # nrows seems not to be a callable
    f2_num = self.f2.root.timestamps.nrows
    row_num = (f1_num + f2_num)

    # file 3, outfile
    f3 = tables.open_file('sortedFile.hdf', mode='w')
    f3.create_group(f3.root, name='photon_data')
    filters = tables.Filters(complevel=6, complib='zlib')
    atom1 = Int64Atom()
    atom2 = UInt8Atom()
    ts = f3.create_carray('/photon_data', name='timestamps', atom=atom1, shape=(row_num, 1), filters=filters)
    det = f3.create_carray('/photon_data', name='detectors', atom=atom2, shape=(row_num, 1), filters=filters)

    i = 0   # indices ts_1
    j = 0   # indices ts_2
    k = 0   # indices ts

    print("Starting iteration.")
    start = time.time()
    t1 = ts_1[0]
    t2 = ts_2[0]
    while True:
        if t1 > t2:
            # t1 is greater than t2, t2 gets written, only j and t2 updates
            ts[k] = t2
            det[k] = 1
            j += 1
            t2 = ts_2[j]
        elif t2 > t1:
            # t2 is greater, t1 gets written, i and t1 updates
            ts[k] = t1
            det[k] = 0
            i += 1
            t1 = ts_2[i]
        else:
            # t1 == t2, t1 written first, t2 seconds, k updates intermediately, all update
            ts[k] = t1
            det[k] = 0
            i += 1
            t1 = ts_1[i]
            k += 1
            ts[k] = t2
            det[k] = 1
            j += 1
            t2 = ts_2[j]
        k += 1   # k updates each iteration
        if i > f1_num:
            # t1 has ended first, rest of ts is ts_2
            ts[k:row_num] = ts_2[j:f2_num]
            det[k:row_num] = np.zeros([row_num - k], dtype=np.uint8)
            break
        elif j > f2_num:
            # t2 has ended first, rest is ts_1
            ts[k:row_num] = ts_1[i:f1_num]
            det[k:row_num] = np.ones([row_num - k], dtype=np.uint8)
            break
    print("Merging took %f seconds." % (time.time() - start))

    f1.close()
    f2.close()
    f3.close()


merge_files()
