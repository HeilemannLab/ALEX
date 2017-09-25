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
import fib2
print(fib2.fib.__doc__)


# a = numpy.zeros(8, 'd')
# fib1.fib(a)
# print(a)
i = np.array(3)
j = np.array(3)
t1 = 3
t2 = 3
check = 1
t = 0
f1 = 5
f2 = 5
t, check = fib2.fib(i, j, t1, t2, f1, f2)
# print(t)
print('i=%i, j=%i, t=%i, check=%i (should be 4, 3, 3, 1)' % (i, j, t, check))
