'''######################################################################
# File Name: save_to_photon_hdf5_test.py
# Project: ALEX
# Version:
# Creation Date: 31/08/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import libs.saveFiles
import sys
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    save = libs.saveFiles.FileDialogue()
    save.saveDataToHDF5('resultfile.hdf')
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
