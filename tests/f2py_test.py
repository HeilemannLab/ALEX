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
import numpy
import fib2
print(fib2.fib.__doc__)



a = numpy.zeros(8,'d')
fib2.fib(a)
print(a)
