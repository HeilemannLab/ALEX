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
import tables
import time


def small_copy():
    filters = tables.Filters(complevel=6, complib='zlib')
    atom = tables.UInt32Atom()
    start = time.time()
    # File 1
    f1 = tables.open_file('tempAPD1.hdf', 'r')
    t1 = f1.root.timestamps

    f1_copy = tables.open_file('tempAPD1_copy.hdf', 'w')
    t1_copy = f1_copy.create_carray(f1_copy.root, name='timestamps', atom=atom, shape=(100000, 2), filters=filters)

    t1_copy[0:100000, :] = t1[0:100000, :]

    f1.close()
    f1_copy.close()
    print("File 1 took %f seconds." % (time.time() - start))

    # file 2
    start = time.time()
    f2 = tables.open_file('tempAPD2.hdf', 'r')
    t2 = f2.root.timestamps

    f2_copy = tables.open_file('tempAPD2_copy.hdf', 'w')
    t2_copy = f2_copy.create_carray(f2_copy.root, name='timestamps', atom=atom, shape=(100000, 2), filters=filters)

    t2_copy[0:100000, :] = t2[0:100000, :]

    f2.close()
    f2_copy.close()
    print("File 1 took %f seconds." % (time.time() - start))


small_copy()
