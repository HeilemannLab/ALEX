'''######################################################################
# File Name: HDFmask.py
# Project: ALEX
# Version:
# Creation Date: 2017/04/11
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyQt5.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QPushButton, QDialog


class HDFmask(QDialog):
    """
    This class provides a raw interface to fill in the measurement variables, which are needed to
    get a nice photon-HDF file, as it is desired by Fretbursts. This is not ready yet.
    """
    def __init__(self):
        super(HDFmask, self).__init__()
        self._dict = {"author_affiliation": "Institute for Physical and Theoretical Chemistry, Goethe-University Frankfurt",
                      "author": "author name",
                      "sample_name": "sampleX",
                      "buffer_name": "buffer",
                      "dye_names": "dye1, dye2",
                      "description": "Experiment X",
                      "num_dyes": int(2)}

        label1 = QLabel("author")
        label2 = QLabel("institute")
        label3 = QLabel("sample")
        label4 = QLabel("buffer")
        label5 = QLabel("dyes")
        label6 = QLabel("description")
        label8 = QLabel("number dyes")

        line1 = QLineEdit()
        line1.setPlaceholderText("Your name")
        line2 = QLineEdit()
        line2.setPlaceholderText("Institute for Physical and Theoretical Chemistry, Goethe-University Frankfurt")
        line3 = QLineEdit()
        line3.setPlaceholderText("Sample name")
        line4 = QLineEdit()
        line4.setPlaceholderText("Buffer name")
        line5 = QLineEdit()
        line5.setPlaceholderText("Dye names, separated by comma")
        line6 = QLineEdit()
        line6.setPlaceholderText("detailed description")
        line8 = QLineEdit()
        line8.setPlaceholderText("Number of dyes")

        line1.textChanged.connect(lambda: self.setitem("author", line1.text()))
        line2.textChanged.connect(lambda: self.setitem("author_affiliation", line2.text()))
        line3.textChanged.connect(lambda: self.setitem("sample_name", line3.text()))
        line4.textChanged.connect(lambda: self.setitem("buffer_name", line4.text()))
        line5.textChanged.connect(lambda: self.setitem("dye_names", line5.text()))
        line6.textChanged.connect(lambda: self.setitem("description", line6.text()))
        line8.textChanged.connect(lambda: self.setitem("num_dyes", int(line8.text())))

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveFile)

        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(line1)
        vbox.addWidget(label2)
        vbox.addWidget(line2)
        vbox.addWidget(label3)
        vbox.addWidget(line3)
        vbox.addWidget(label4)
        vbox.addWidget(line4)
        vbox.addWidget(label8)
        vbox.addWidget(line8)
        vbox.addWidget(label5)
        vbox.addWidget(line5)
        vbox.addWidget(label6)
        vbox.addWidget(line6)
        vbox.addWidget(saveButton)

        self.setLayout(vbox)
        self.setWindowTitle("hdf5 mask")

    def maskWindow(self):
        self.exec_()
        # self.show()

    def saveFile(self):
        self.close()
        # self.accept()
        # self.done(0)

    def setitem(self, key, value):
        self._dict[key] = value
