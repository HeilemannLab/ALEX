'''######################################################################
# File Name: ChangeReadArray.py
# Project: ALEX
# Version:
# Creation Date: 13/10/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from PyQt5.QtGui import QIntValidator


class ChangeReadArray(QDialog):
    def __init__(self):
        super(ChangeReadArray, self).__init__()
        self.InitWindow()
        self.result = None

    def InitWindow(self):
        label = QLabel('This is a core feature of the program. '
                       'Only change it, if you are aware of the consequences.')

        self.line = QLineEdit()
        self.line.setPlaceholderText('Type in an integer')
        self.line.setValidator(QIntValidator())
        self.line.setMaxLength(6)
        self.line.setToolTip('The array size determines how many samples the card gathers '
                             'at once before passing the data to the program. Note that the '
                             'program will fail, if the number of samples available is '
                             'smaller than the array size. Default is 1e3.')
        self.save = QPushButton('Save', self)
        self.save.clicked.connect(self.saved)
        self.cancel = QPushButton('Cancel', self)
        self.cancel.clicked.connect(self.canceled)

        hbox = QHBoxLayout()
        hbox.addWidget(self.save)
        hbox.addWidget(self.cancel)

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(self.line)
        vbox.addLayout(hbox)

        self.setWindowTitle('Change read array size')
        self.setLayout(vbox)

    def saved(self):
        self.result = self.line.text()
        self.close()

    def canceled(self):
        self.result = None
        self.close()

    def showDialog(self):
        self.exec_()
        return self.result
