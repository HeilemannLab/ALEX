'''######################################################################
# File Name: readprint_csv.py
# Project: ALEX
# Version:
# Creation Date: 06/12/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
import matplotlib.pyplot as plt
import pathlib


filename = 'Y:\\Messungen\\2017_12_05\\laser.txt'
array = np.loadtxt(filename, dtype=np.float, delimiter='\t', skiprows=2)
greenline, = plt.plot(array[:, 0], array[:, 1], 'g*', label='532 nm')
redline, = plt.plot(array[:, 0], array[:, 3], 'r+', label='640 nm')
plt.xlabel('Operating power in mW')
mu = r'$\mu$'
ylabel = 'Intensity above objective in {}W'.format(mu)
plt.ylabel(ylabel)
plt.legend(handles=[greenline, redline])
plt.title('Laser intensities ARES, 05.12.2017')
filename = pathlib.Path(filename)
figname = filename.parent / 'Laser_int.png'
print(figname)
plt.savefig(str(figname))
plt.show()
