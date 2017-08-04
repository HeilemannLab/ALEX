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


class Refresh():
    def __init__(self):
        self._sets = libs.dictionary.UIsettings()

    def refreshUI(self, changeType, changeKey, value):
        if changeType == 0:
            self.refreshSliderSettings(changeKey, value)
        if changeType == 1:
            self.refreshBoxSettings(changeKey, value)
        if changeType == 2:
            self.changeRadioButton(changeKey)
            self.changeRadioButton(value)
        return self._sets._a

    # Input functions
    def changeRadioButton(self, b):
        if b.text() == 'Continuous':
            if b.isChecked():
                self._sets.setitem("Radio", 0)

        if b.text() == 'Finite':
            if b.isChecked():
                self._sets.setitem("Radio", 1)

    def refreshSliderSettings(self, changeKey, value):
        if changeKey == 'sld_red':
            self._sets.setitem("lpower red", value)
        elif changeKey == 'sld_green':
            self._sets.setitem("lpower green", value)
        elif changeKey == 'sld_percentage':
            self._sets.setitem("laser percentageG", value)

    def refreshBoxSettings(self, changeKey, value):
        if changeKey == 'sb_red':
            self._sets.setitem("lpower red", value)
        elif changeKey == 'sb_green':
            self._sets.setitem("lpower green", value)
        elif changeKey == 'sb_sampFreq':
            self._sets.setitem("laser frequency", value)
        elif changeKey == 'duration':
            self._sets.setitem("Duration", value)
        elif changeKey == "sb_percentG":
            self._sets.setitem("laser percentageG", value)
            self._sets.setitem("laser percentageR", (100.0 - value))
        elif changeKey == "sb_percentR":
            self._sets.setitem("laser percentageR", value)
            self._sets.setitem("laser percentageG", (100.0 - value))
