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
import mainwindow as mw
from multiprocessing import freeze_support


def main():
    app = QApplication(sys.argv)
    mainWindow = mw.MainWindow()
    # mainWindow.initUI()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    freeze_support()
    main()
