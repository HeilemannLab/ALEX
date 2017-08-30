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
    """
    The laser class is a subclass of multiprocessing.Process. It serves to run the
    illumination class as long as the measurements takes place. It also starts and
    stops the timing task, which provides sampling and especially the trigger edge.
    """
    def __init__(self, running, dictionary, semaphore):
        """
        @param running: multiprocessing event
        @param dictionary: dictionary class instance
        @param semaphore: multiprocessing Semaphore
        """
        super(LaserControl, self).__init__()
        self.daemon = True
        self._sem = semaphore
        self._laser = libs.Illumination.Illumination(semaphore)
        self._timing = libs.Timing.SampleClock()
        self._running = running
        self._dict = dictionary

        self._laser.refreshSettings(self._dict._a)
        self._timing.refreshSettings(self._dict._a)

    def run(self):
        """
        The timing starts after the illumination because of the ArmStartTrigger, which makes the tasks wait
        for the next edge. So starting beforehands could desynchronize tasks. The while loop is rather a
        dummy thing, since it only passes by time until measurement is indicated as done by self._running.
        """
        self._timing.InitClock()

        self._laser.startIllumination()
        self._timing.startClock()
        while self._running.is_set():
            pass
        self._laser.stopIllumination()
        self._timing.stopClock()
        print("Laser stopped and exits.")

    def __del__(self):
        print("Laser class instance has been removed.")
