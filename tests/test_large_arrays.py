import numpy as np
import tables


size = int(6e8)
array = np.ones([size, 2])

print("Array created, has shape ", np.shape(array))

f = tables.open_file('test_large_array1.hdf', mode='w')
atom = tables.Float64Atom()
filters = tables.Filters(complib='zlib', complevel=6)
f.create_carray(where=f.root, name='array', atom=atom, obj=array, filters=filters)
f.flush()
f.close()

print("File 1 has been created.")

g = tables.open_file('test_large_array2.hdf', mode='w')
atom = tables.Float64Atom()
filters = tables.Filters(complib='zlib', complevel=6)
array_c = g.create_carray(where=g.root, name='array', atom=atom, shape=(size, 2), filters=filters)
array_c = array
g.flush()
g.close()

print("File 2 has been created.")
