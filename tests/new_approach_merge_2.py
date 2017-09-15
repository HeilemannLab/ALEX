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
import time
from numba import jit, uint32, int64
import numpy as np


# @jit('(uint32[:], uint32[:], uint32[:], uint32[:], uint32, uint32)')
def merge_files(ts_1, ts_2, ts, det, f1_num, f2_num):
    i = 0   # indices ts_1
    j = 0   # indices ts_2
    k = 0   # indices ts

    print("Starting iteration.")
    #    t1 = ts_1[0, 0]
    #    t2 = ts_2[0, 0]
    t1 = ts_1[i, 0]
    t2 = ts_2[j, 0]
    check = 1
    while check:
        [ts[k], i, j, check] = iterate(i, j, t1, t2, f1_num, f2_num, check)
    if i == f1_num:
        # t1 has ended first, rest of ts is ts_2
        for o in range(j, f2_num):
            ts[k] = ts_2[o, 0]
            det[k] = 0
            k += 1
    if j == f2_num:
        # t2 has ended first, rest is ts_1
        for p in range(i, f1_num):
            ts[k] = ts_1[p, 0]
            det[k] = 1
            k += 1


@jit('int64[4](uint32, uint32, uint32, uint32, uint32, uint32, uint32)', nopython=True, nogil=True, parallel=True)
def iterate(i, j, t1, t2, f1_num, f2_num, check):
    if t1 > t2:
        t = t2
        j += 1

    else:
        t = t1
        i += 1
    if (i == f1_num) or (j == f2_num):
        check = 0
    out = np.array([t, i, j, check])
    return out


"""Merging without rollover correction"""
# file 1, apd1
f1 = tables.open_file('tempAPD1.hdf', 'r')
ts_1 = f1.root.timestamps

# file 2, apd2
f2 = tables.open_file('tempAPD2.hdf', 'r')
ts_2 = f2.root.timestamps

# lengths
f1_num = f1.root.timestamps.nrows   # nrows seems not to be a callable
f2_num = f2.root.timestamps.nrows
row_num = (f1_num + f2_num)

# file 3, outfile
f3 = tables.open_file('sortedFile.hdf', mode='w')
f3.create_group(f3.root, name='photon_data')
filters = tables.Filters(complevel=6, complib='zlib')
atom1 = tables.Int64Atom()
atom2 = tables.Int8Atom()
ts = f3.create_carray('/photon_data', name='timestamps', atom=atom1, shape=(row_num, 1), filters=filters)
det = f3.create_carray('/photon_data', name='detectors', atom=atom2, shape=(row_num, 1), filters=filters)
start = time.time()
merge_files(ts_1, ts_2, ts, det, f1_num, f2_num)
print("Merging took %f seconds." % (time.time() - start))
f1.close()
f2.close()
f3.close()
