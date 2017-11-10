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
import anim
from multiprocessing import Queue as mpQueue
import time


duration = 10
signal = None


def gen_data(duration):
    for i in np.arange(duration):
        time.sleep(0.1)
        a = np.arange(1000)
        q1.put(a)
        q2.put(a)

q1 = mpQueue()
q2 = mpQueue()
anim = anim.Animation(q1, q2, duration, 1000)

anim.run()
gen_data(duration)
anim.animate()
anim.anim._stop()
