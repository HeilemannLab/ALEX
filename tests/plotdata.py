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
import matplotlib.pyplot as plt
import numpy as np


filename = 'resultsfile_selfTrigged.txt'
data = np.loadtxt(filename, usecols=0)

data2 = np.ones([np.size(data), 2])
data2[:, 0] = data[:]

plt.step(data2[:, 0], data2[:, 1])
# plt.axis([0, 100, 0, 1.5])
plt.show()
