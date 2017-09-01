'''######################################################################
# File Name: Refresher.py
# Project: ALEX
# Version:
# Creation Date: 2017/03/07
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import libs.dictionary


class Refresh:
    """
    The refresh class provides methods to set new values on the dictionary and match dependent values,
    like sliders with their corresponding spinbox.
    """
    def __init__(self):
        self._dict = libs.dictionary.UIsettings()

    def refreshUI(self, changeType, changeKey, value):
        """
        Sorts the type of change, passes changeKey and value
        @param changeType: str
        @param changeKey: Key
        @param value: int or float
        """
        if changeType == 0:
            self.refreshSliderSettings(changeKey, value)
        if changeType == 1:
            self.refreshBoxSettings(changeKey, value)
        if changeType == 2:
            self.changeRadioButton(changeKey)
            self.changeRadioButton(value)   # check if this here is necessary
        return self._dict._a

    # Input functions
    def changeRadioButton(self, b):
        if b.text() == 'Continuous':
            if b.isChecked():
                self._dict._a["Radio"] = 0

        if b.text() == 'Finite':
            if b.isChecked():
                self._dict._a["Radio"] = 1

    def refreshSliderSettings(self, changeKey, value):
        """
        This function could maybe merged with the next and simplified. Keywords could be
        red and green, or percentage.
        """
        if changeKey == 'sld_red':
            self._dict._a["lpower red"] = value
        elif changeKey == 'sld_green':
            self._dict._a["lpower green"] = value
        elif changeKey == 'sld_percentage':
            self._dict._a["laser percentageG"] = value

    def refreshBoxSettings(self, changeKey, value):
        if changeKey == 'sb_red':
            self._dict._a["lpower red"] = value
        elif changeKey == 'sb_green':
            self._dict._a["lpower green"] = value
        elif changeKey == 'sb_sampFreq':
            self._dict._a["laser frequency"] = value
        elif changeKey == 'duration':
            self._dict._a["Duration"] = value
        elif changeKey == "sb_percentG":
            self._dict._a["laser percentageG"] = value
            self._dict._a["laser percentageR"] = (100.0 - value)
        elif changeKey == "sb_percentR":
            self._dict._a["laser percentageR"] = value
            self._dict._a["laser percentageG"] = (100.0 - value)
