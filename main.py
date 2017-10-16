'''######################################################################
# File Name: main.py
# Project: ALEX
# Version:
# Creation Date: 2017/02/02
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import sys

from PyQt5.QtWidgets import QApplication
from multiprocessing import freeze_support

import MainWindow as mw


def Main():
    """
    Main class launches Mainwindow, freeze_support
    helps with maintaining multiprocessing.
    """

    app = QApplication(sys.argv)
    mainWindow = mw.MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    freeze_support()
    Main()
