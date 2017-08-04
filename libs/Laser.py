'''######################################################################
# File Name: Laser.py
# Project: ALEX
# Version:
# Creation Date: 2017/07/21
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import libs.Illumination
import libs.Timing
from multiprocessing import Process


class LaserControl(Process):
    def __init__(self, running, dictionary):
        super(LaserControl, self).__init__()
        self.daemon = True
        self._laser = libs.Illumination.Illumination()
        self._timing = libs.Timing.SampleClock()
        self._running = running
        self._dict = dictionary

    def run(self):
        self._laser.refreshSettings(self._dict)
        self._timing.refreshSettings(self._dict)

        self._laser.startIllumination()
        self._timing.startClock()
        while self._running.is_set():
            pass
        self._laser.stopIllumination()
        self._timing.stopClock()
        print("Laser stopped and exits.")

    def __del__(self):
        print("Laser class instance has been removed.")
