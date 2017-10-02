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
    This class provides a raw interface to fill in the additional information, which is required to
    get a nice photon-HDF file. This library can be accessed from 'save Data' and 'Convert Data'.
    Always create a class instance and execute the window by calling 'instance.maskWindow()'. It is
    possible to pass an old dictionary.
    """
    def __init__(self):
        super(HDFmask, self).__init__()
        self._dict = {"author_affiliation": "Institute for Physical and Theoretical Chemistry, Goethe-University Frankfurt",
                      "author": "Your name",
                      "sample_name": "Sample",
                      "buffer_name": "Buffer",
                      "dye_names": "Dye names, seperated by comma",
                      "description": "Detailed description",
                      "num_dyes": int(2)}

        label1 = QLabel("Author")
        label2 = QLabel("Institute")
        label3 = QLabel("Sample name")
        label4 = QLabel("Buffer name")
        label5 = QLabel("Dyes")
        label6 = QLabel("Description")
        label8 = QLabel("Number of dyes")

        line1 = QLineEdit()
        line1.setPlaceholderText(self._dict["author"])
        line2 = QLineEdit()
        line2.setPlaceholderText(self._dict["author_affiliation"])
        line3 = QLineEdit()
        line3.setPlaceholderText(self._dict["sample_name"])
        line4 = QLineEdit()
        line4.setPlaceholderText(self._dict["buffer_name"])
        line5 = QLineEdit()
        line5.setPlaceholderText(self._dict["dye_names"])
        line6 = QLineEdit()
        line6.setPlaceholderText(self._dict["description"])
        line8 = QLineEdit()
        line8.setPlaceholderText(str(self._dict["num_dyes"]))

        line1.textChanged.connect(lambda: self.setitem("author", line1.text()))
        line2.textChanged.connect(lambda: self.setitem("author_affiliation", line2.text()))
        line3.textChanged.connect(lambda: self.setitem("sample_name", line3.text()))
        line4.textChanged.connect(lambda: self.setitem("buffer_name", line4.text()))
        line5.textChanged.connect(lambda: self.setitem("dye_names", line5.text()))
        line6.textChanged.connect(lambda: self.setitem("description", line6.text()))
        line8.textChanged.connect(lambda: self.setitem("num_dyes", int(line8.text())))

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveInfos)

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
        self.setWindowTitle("Additional measurements informations")

    def maskWindow(self, dictionary=None):
        if dictionary is None:
            print('Dict is None')
        else:
            self._dict.update(dictionary)
        self.exec_()
        return self._dict

    def saveInfos(self):
        self.close()

    def setitem(self, key, value):
        self._dict[key] = value
