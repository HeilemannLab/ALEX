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


filename = 'F:\\Karoline\\Messungen\\2017_12_19\\laser_intensities.txt'
array = np.loadtxt(filename, dtype=np.float, delimiter='\t', skiprows=2)
greenline, = plt.plot(array[:, 0], array[:, 1], 'g*', label='532 nm')
redline, = plt.plot(array[:, 0], array[:, 3], 'r+', label='640 nm')
plt.xlabel('Operating power [mW]')
plt.xticks(np.arange(2, 30 + 1, 2.0))
plt.yticks(np.arange(0, 250 + 1, 25.0))
mu = r'$\mu$'
ylabel = 'Intensity after fiber [{}W]'.format(mu)
plt.ylabel(ylabel)
plt.legend(handles=[greenline, redline])
plt.title('Laser intensities ARES, 19.12.2017\nFiltered before AOTF')
filename = pathlib.Path(filename)
figname = filename.parent / 'Laser_int.png'
print(figname)
plt.savefig(str(figname))
plt.show()
