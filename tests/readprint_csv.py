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
import csv
import matplotlib.pyplot as plt


file1 = 'F:\\Karoline\\Scripts\\Thesis\\Graphics\\cyanines\\Cy3.csv'
file2 = 'F:\\Karoline\\Scripts\\Thesis\\Graphics\\cyanines\\Cy5.csv'

a1 = np.zeros([701, 3])
a2 = np.zeros([701, 3])
with open(file1, 'r') as f:
    cy3 = csv.reader(f)
    print('cy3')
    i = 0
    for row in cy3:
        a1[i, :] = row
        i += 1


with open(file2, 'r') as f:
    cy5 = csv.reader(f)
    print('cy5')
    i = 0
    for row in cy5:
        a2[i, :] = row
        i += 1

greenline, = plt.plot(a1[100:, 0], a1[100:, 1], 'g-', label='Cy3 excitation')
greenline2, = plt.plot(a1[100:, 0], a1[100:, 2], 'g--', label='Cy3 emission')
redline, = plt.plot(a2[100:, 0], a2[100:, 1], 'r-', label='Cy5 excitation')
redline2, = plt.plot(a2[100:, 0], a2[100:, 2], 'r--', label='Cy5 emission')


plt.axvspan(662.5, 737.5, ymin=0.075, alpha=0.2, color='r')
plt.axvline(532, ymin=0.075, color='g', linestyle=':')
# plt.axvline(640, color='r')

plt.xlim([400, 850])
plt.ylim([-10, 125])
plt.xlabel('Wavelength in nm')
plt.ylabel('Excitation/emission in a.u.')
# plt.legend(handles=[greenline, redline, greenline2, redline2], loc=2)
plt.title('Spectra Cy3 Cy5')
figname = 'F:\\Karoline\\Scripts\\Thesis\\Graphics\\cyanines\\cyanines.eps'
plt.savefig(str(figname))
print(figname)
plt.savefig(str(figname))
plt.show()
