import numpy as np
import tables
from multiprocessing import Queue
import time


# Init
dataQ = Queue()
size = int(1e6)
x = np.ones([size, 2])

#  Fill the queue
t_start = time.time()
for i in range(10):
    dataQ.put(x)
dataQ.put('Stop')
t_end = time.time()
t1 = t_end - t_start

# Write the file
t_start = time.time()
f = tables.open_file('test.hdf', mode='w')
atom = tables.IntAtom() # Look into types, that can be used or is used by daqmx respectively
array_c = f.create_earray(f.root, 'array_c', atom=atom, shape=(0, 2))
# 
for array in iter(dataQ.get, 'Stop'):
    array_c.append(array)
f.close()
t_end = time.time()
t2 = t_end - t_start

print("Queued in %f and written in %f seconds." % (t1, t2))
