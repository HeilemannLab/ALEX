'''######################################################################
# File Name:
# Project: dictionary.py
# Version:
# Creation Date: 2017/02/03
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''


class UIsettings:

    def __init__(self):
        a = dict()
        a["lpower red"] = 100.0
        a["lpower green"] = 50.0
        a["laser frequency"] = 1000.0
        a["Radio"] = 0
        a["Duration"] = 300
        a["laser percentageG"] = 60
        a["laser percentageR"] = 40
        self._folder = 'C:/'
        self._a = a

    def getitem(self, item):
        return self._a[item]

    def setitem(self, item, var):
        self._a[item] = var
