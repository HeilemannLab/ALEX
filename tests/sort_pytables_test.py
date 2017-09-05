'''######################################################################
# File Name: sort_pytables_test.py
# Project: ALEX
# Version:
# Creation Date: 05/09/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import tables
import numpy as np
import time


class TableDescription(tables.IsDescription):
    X = tables.UInt32Col(pos=1)


class Sort_Test:
    def __init__(self):
        self._planet = 0

    def openFiles(self):
        # file 1, apd1
        self.f1 = tables.open_file('tempAPD1.hdf', 'r')

        # file 2, apd2
        self.f2 = tables.open_file('tempAPD2.hdf', 'r')

        # file 3, merged and sorted file
        self.f3 = tables.open_file('sortedFile.hdf', mode='w')
        self.filters = tables.Filters(complevel=6, complib='zlib')
        f1_num = self.f1.root.timestamps.nrows   # nrows seems not to be a callable
        f2_num = self.f2.root.timestamps.nrows
        row_num = (f1_num + f2_num)

        det1 = np.zeros([f1_num])
        det2 = np.ones([f2_num])

        self.f3.create_group(self.f3.root, 'photon_data', filters=self.filters)

        # timestamps table
        start = time.time()
        ts_table = self.f3.create_table(self.f3.root,
                                        'timestamps_table',
                                        description=TableDescription,
                                        filters=self.filters,
                                        expectedrows=row_num,
                                        obj=None)
        ts_table.append(self.f1.root.timestamps[:, 0])
        ts_table.append(self.f2.root.timestamps[:, 0])
        ts_table.cols._f_col('X').create_csindex()
        ts_table.flush()
        end = time.time()
        print("Creating and indexing timestamps table took %f seconds." % (end - start))

        # detector table
        start = time.time()
        det_table = self.f3.create_table(self.f3.root,
                                         'detectors_table',
                                         description=TableDescription,
                                         filters=self.filters,
                                         expectedrows=row_num,
                                         obj=None)
        det_table.append(det1)
        det_table.append(det2)
        det_table.flush()
        detectors = self.f3.create_earray('/photon_data',
                                          'detectors',
                                          filters=self.filters,
                                          shape=(0, 1),
                                          atom=tables.Float64Atom())
        end = time.time()
        print("Creating detectors table took %f seconds." % (end - start))

        # copy both tables with in sorted way
        start = time.time()
        for row in det_table.itersorted(ts_table.cols._f_col('X')):
            # print("Got %i of type %s" % (row.__getitem__('X'), type(row.__getitem__('X'))))
            detectors.append(int(row.__getitem__('X')))
        end = time.time()
        print("Copying tables in sorted manner took %f seconds." % (end - start))

        # close files
        self.f1.close()
        self.f2.close()
        self.f3.close()

    """
    def mergesort_test(self):
        tm = np.hstack([t1, t2])
        index_sort = tm.argsort(kind='mergesort')  # stable sorting
        tm = tm[index_sort]
        mask_t2 = np.hstack([np.zeros(t1.size, dtype=bool),
                             np.ones(t2.size, dtype=bool)])[index_sort]
        return tm, mask_t2
    """
if __name__ == '__main__':
    a = Sort_Test()
    a.openFiles()
