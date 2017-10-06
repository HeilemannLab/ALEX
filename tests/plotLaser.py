'''######################################################################
# File Name:
# Project:
# Version:
# Creation Date:
# Created By:
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import dictionary


class plotLaser:
    def __init__(self):
        self._dict = dictionary.UIsettings()
        self.redAmp = self._dict.getitem("lpower red")
        self.greenAmp = self._dict.getitem("lpower green")
        self._sampFreq = 100
        self._t = np.linspace(0, 1, self._sampFreq, endpoint=False)
        self._redP = np.zeros([self._sampFreq, 1])
        self._greenP = np.zeros([self._sampFreq, 1])
        self._sig1 = np.zeros([self._sampFreq, 1])
        self._sig2 = np.zeros([self._sampFreq, 1])
        self._silence = np.zeros([self._sampFreq, 1])
        self._duty = 0.49
        self.fig = None

    def refreshSettings(self, dictionary):
        self._dict._a = dictionary

    def calcSignal(self):
        self.redAmp = self._dict.getitem("lpower red")
        self.greenAmp = self._dict.getitem("lpower green")

        self.silenceAPD()
        phi = np.pi
        self._redP = (self.redAmp / 100.0) * 2.5 * signal.square(2.0 * np.pi * 1.0 * self._t, self._duty) + (self.redAmp / 100.0) * 2.5
        self._greenP = (self.greenAmp / 100.0) * 2.5 * signal.square(2.0 * np.pi * 1.0 * self._t + phi, self._duty) + (self.greenAmp / 100.0) * 2.5
        self._data = np.concatenate((self._redP, self._greenP, self._silence))

    def silenceAPD(self):
        phi = np.pi
        self._sig1 = 2.5 * 1.0 * signal.square(2.0 * np.pi * 1.0 * (self._t + 0.01), 0.009) + 2.5
        self._sig2 = 2.5 * 1.0 * signal.square(2.0 * np.pi * 1.0 * (self._t + 0.01) + phi, 0.009) + 2.5
        self._silence = self._sig1 + self._sig2

    def plotSignal(self):
        self.silenceAPD()
        self.calcSignal()
        ylimit_red = (-1, 15 * (self.redAmp / 100.0))
        plt.subplot(4, 1, 1)
        plt.subplots_adjust(hspace=1.0)
        plt.step(self._t, self._redP)
        plt.title("Red laser")
        plt.ylim(ylimit_red)

        ylimit_green = (-1, 15 * (self.greenAmp / 100.0))
        plt.subplot(4, 1, 2)
        plt.step(self._t, self._greenP)
        plt.title("Green laser")
        plt.ylim(ylimit_green)

        plt.subplot(4, 1, 3)
        plt.step(self._t, self._silence)
        plt.title("Silence APD")
        plt.ylim(ylimit_red)

        plt.subplot(4, 1, 4)
        plt.step(self._t, self._redP, 'r', self._t, self._greenP, 'g', self._t, self._silence, 'b')
        plt.ylim(ylimit_red)

        return plt
