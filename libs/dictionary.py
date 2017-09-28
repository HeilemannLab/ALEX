'''######################################################################
# File Name: dictionary.py
# Project: ALEX
# Version:
# Creation Date: 2017/02/03
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''


class UIsettings:
    """
    The UIsetting class hosts a dictionary which holds all the key parameters to the measurement.
    Methods 'getitem' and 'setitem' are outdated.
    """
    def __init__(self):
        a = {}
        a["lpower red"] = 50.0
        a["lpower green"] = 50.0
        a["laser frequency"] = 10000.0
        a["Radio"] = 0
        a["Duration"] = 300
        a["laser percentageG"] = 50
        a["laser percentageR"] = 50
        self._folder = 'C:/'
        self._a = a

    def getitem(self, item):
        """
        Read the dict item by its key and return it.
        @param item: string
        """
        return self._a[item]

    def setitem(self, item, var):
        """
        Write value 'var' to the key 'item' into dict.
        @param item: string
        @param var: float
        """
        self._a[item] = var
