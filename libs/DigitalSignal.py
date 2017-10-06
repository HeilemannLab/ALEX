'''######################################################################
# File Name: Illumination.py
# Project: ALEX
# Version:
# Creation Date: 2017/07/21
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import libs.UIsettings
import libs.AnalogSignal


class DigitalSignal:
    """
    The Illumination class serves the purpose to create the laser alternation
    pattern as a digital signal, which can then be used to control the AOTF.
    Also the digital silencer pulse for the APDs is generated here. It should
    go directly to the APD, which can take in a digital signal. All counter tasks
    can be configured to start on a ArmStartTrigger, so the synchronization is optimal.
    The signal will be output on the ctrNout pins.
    """
    def __init__(self, semaphore):
        self._sem = semaphore
        self._dict = libs.UIsettings.UIsettings()
        self._analog = libs.AnalogSignal.AnalogSignal()
        self._percentHighGreen = 0
        self._percentHighRed = 0
        self._frequency = 0
        self._highTime = 0
        self._lowTime = 0
        self._initialDelay_red = 0
        self._highSil = 0
        self._lowSil = 0
        self._initialDelay_sil1 = 0
        self._initialDelay_sil2 = 0
        self._green = None
        self._red = None
        self._sil1 = None
        self._sil2 = None

    def refreshSettings(self, dictionary):
        """
        refreshes settings of this class and of the SignalIntensity class.
        @param dictionary: dict
        """
        self._dict._a.update(dictionary)
        self._analog.refreshSettings(self._dict._a)

    def calcSignal(self):
        """
        The signal is generated on the base of daqmx COPulseChanTime task, which
        suits the need of interleaved signal perfectly. A high and a low Time can
        be configured, so an initial delay can, which make the alternation possible.
        All values are in seconds (As far as nidaqmx documentation states, there's
        no smaller possibility). The digital signal does not take into account at
        which power percentage the lasers should be operated. The height of the signal
        is 5V(TTL). The silencer runs at doubled frequency, so the APDs get muted on
        all transitions from laser to laser.
        """
        self._percentHighGreen = (self._dict._a["laser percentageG"] / 100.0)
        self._percentHighRed = (self._dict._a["laser percentageR"] / 100.0)
        self._frequency = self._dict._a["laser frequency"]
        self._highTime = (1.0 / self._frequency) * self._percentHighGreen
        self._lowTime = (1.0 / self._frequency) * self._percentHighRed
        self._initialDelay_red = self._highTime
        self._lowSil = (0.05 / 100000)      # The silencer takes 10% off the illumination/detection time
                                            # at 100kHz (50/50), at 1kHz 0.001%
        self._highSil = (1.0 / self._frequency) - (self._lowSil)
        self._initialDelay_sil1 = (0.4 * self._lowSil)
        self._initialDelay_sil2 = self._initialDelay_sil1 + self._highTime

    def InitIllumination(self):
        """
        The counter output tasks are configured as PulseChanTime, which is fairly
        flexible. The tasks are triggered by an ArmStartTrigger, which makes it wait
        for the next trigger edge. Also the analog signal gets started here. The
        semaphore indicates, that initiation is done.
        """
        self.calcSignal()
        self._analog.InitAnalog()

        self._green = Task()
        self._green.CreateCOPulseChanTime(counter="Dev2/ctr4",
                                          nameToAssignToChannel="",
                                          units=DAQmx_Val_Seconds,
                                          idleState=DAQmx_Val_Low,
                                          initialDelay=0.00,
                                          lowTime=self._lowTime,
                                          highTime=self._highTime)
        self._green.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

        self._red = Task()
        self._red.CreateCOPulseChanTime(counter="Dev2/ctr5",
                                        nameToAssignToChannel="",
                                        units=DAQmx_Val_Seconds,
                                        idleState=DAQmx_Val_Low,
                                        initialDelay=self._initialDelay_red,
                                        lowTime=self._highTime,
                                        highTime=self._lowTime)
        self._red.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

        self._sil = Task()
        self._sil.CreateCOPulseChanTime(counter="Dev2/ctr6",
                                        nameToAssignToChannel="",
                                        units=DAQmx_Val_Seconds,
                                        idleState=DAQmx_Val_Low,
                                        initialDelay=self._initialDelay_sil1,
                                        lowTime=self._lowSil,
                                        highTime=self._highSil)
        self._sil.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

        self._sil2 = Task()
        self._sil2.CreateCOPulseChanTime(counter="Dev2/ctr7",
                                         nameToAssignToChannel="",
                                         units=DAQmx_Val_Seconds,
                                         idleState=DAQmx_Val_Low,
                                         initialDelay=self._initialDelay_sil2,
                                         lowTime=self._lowSil,
                                         highTime=self._highSil)
        self._sil2.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

        self.triggerIllumination()
        self._sem.acquire()

    def startIllumination(self):
        """
        Inits the digital tasks, start analogue signal and after that starts digital tasks.
        """
        self.InitIllumination()
        self._analog.startAnalog()

        self._green.StartTask()
        self._red.StartTask()
        self._sil.StartTask()
        self._sil2.StartTask()

    def triggerIllumination(self):
        """ArmStartTrigger for all tasks. Source from RTSI0, which is provided by the timing class."""
        self._green.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._red.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._sil.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._sil2.SetArmStartTrigType(data=DAQmx_Val_DigEdge)

        self._green.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._red.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._sil.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._sil2.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)

        self._green.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._red.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._sil.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._sil2.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

    def stopIllumination(self):
        """Stops analog and digital laser signals."""
        self._green.StopTask()
        self._red.StopTask()
        self._sil.StopTask()
        self._sil2.StopTask()

        self._green.ClearTask()
        self._red.ClearTask()
        self._sil.ClearTask()
        self._sil2.ClearTask()

        self._analog.stopAnalog()
