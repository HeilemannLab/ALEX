import numpy as np
import time


n = 100
iteration = int(1e6)
a = np.zeros([n*iteration, 2])
c = np.zeros([n*iteration, 2])
d = np.ones([iteration, 2])

t7 = time.time()
a = np.concatenate((a, d))
t8 = time.time()
t9 = t8 - t7
print("Concatenate %i %i shaped array once did take %f seconds." % ((n, iteration, t9)))
print(np.shape(a))

t4 = time.time()
c = np.append(c, d, axis=0)
t5 = time.time()
t6 = t5 - t4
print("Append %i %i shaped array once did take %f seconds." % ((n, iteration, t6)))
print(np.shape(c))
