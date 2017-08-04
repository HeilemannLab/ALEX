'''######################################################################
# File Name: test_file_cprofile.py
# Project: ALEX
# Version:
# Creation Date: 2017_08_03
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import libs.Animation
import libs.Counter
import libs.dataProcesser
import libs.Laser
import libs.dictionary
from multiprocessing import Queue as mpQueue
from multiprocessing import Event as mpEvent
import time


class Tester():
    def __init__(self):
        self._dataQ = mpQueue()
        self._animDataQ = mpQueue()
        self._resultQ = mpQueue()
        self._running = mpEvent()
        self._readArraySize = 100
        self._signal = 1

        # self._dict = libs.dictionary.UIsettings()
        # self._animation = libs.Animation.Animation(self._running, self._animDataQ, self._signal)
        self._counter = libs.Counter.Counter(self._running, self._dataQ, self._readArraySize, 1)
        # self._dataProcesser = libs.dataProcesser.DataProcesser(self._dataQ, self._animDataQ, self._resultQ, self._readArraySize, 1)
        # self._illumination = libs.Laser.LaserControl(self._running, self._dict)

    def run(self):
        self._running.set()
        self._counter.start()
        time.sleep(30)
        self._running.clear()
        self._counter.join()


if __name__ == '__main__':
    a = Tester()
    a.run()
