'''######################################################################
# File Name: Fb_main.py
# Project: Fretbursts for ALEX
# Version:
# Creation Date: 06/10/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import sys

from PyQt5.QtWidgets import QApplication

import FretburstsUI as ui


def Main():
    app = QApplication(sys.argv)
    window = ui.FretburstsUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    Main()
