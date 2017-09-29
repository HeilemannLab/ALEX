'''#######################################################################
# File Name: mainwindow.py
# Project: ALEX
# Version:
# Creation Date: 2017/03/14
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
########################################################################'''
import sys
import time
import os
import numpy as np

from threading import Thread
from matplotlib import pyplot as plt
from multiprocessing import freeze_support
from multiprocessing import Event as mpEvent
from multiprocessing import Queue as mpQueue
from multiprocessing import Semaphore

from PyQt5.QtWidgets import (QGroupBox, QMessageBox, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QPushButton, QStatusBar, QAction, QFileDialog, QSlider, QSpinBox,
                             QRadioButton, QProgressBar, QLabel, QGridLayout, QLCDNumber, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot

import libs.dictionary
import libs.Refresher
import libs.Animation
import libs.Counter
import libs.Laser
import libs.dataProcesser
import libs.saveFiles


class Communicate(QObject):
    """
    Signals make the base communication between Mainwindow and the waiter thread,
    which operates ProgressBar, Start/Stop and StatusBar. It also does communication
    between Mainwindow and animation, which in return feeds the lcd panels with values.

    measurementProgress: sends the iteration from waiter to the progressBar in mainwindow
    stopMeasurement: calls the stopBtn() method, when measurement is finite
                     and the measurement duration ends
    warning: sends a warning when the count rates exceed certain value (apd dependent)
    displayRates: sends the count rates from animation to LCDDisplay in mainwindow
    """

    def __init__(self):
        super(Communicate, self).__init__()

    measurementProgress = pyqtSignal(int)
    stopMeasurement = pyqtSignal()
    warning = pyqtSignal()
    displayRates = pyqtSignal(list)


class MainWindow(QMainWindow):
    """
    Mainwindow class operates the pyqt5 window and all of its widgets.
    It also hosts most of the basic methods connected to the widgets.
    There are start and stop methods, and a waiter thread that keeps an
    eye on the finite measurement. Settings typed by the user get stored
    in a dictionary class and get updated before each measurement call.
    Mainwindow launches all of the subprocesses connecting to the daqmx cards.
    Communication between threads and mainwindow is established via
    pyqtSignals, between mainwindow and subprocesses via multiprocessing queue.
    The main control variable for measurements is a multiprocessing event variable.
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        """
        Init hosts all the variables and UI related functionality. The following classes
        can not be initializes in here, because they inherit from multiprocessing.Process: libs.Counter,
        libs.Laser and libs.dataProcesser. Arguments have to be passed by inheritance, later there's no
        possibility, due to their separation from the main loop. libs.Animation also gets instanciated
        later, due to the window launching functionality in its init method.
        """
        self._dict = libs.dictionary.UIsettings()
        self._files = libs.saveFiles.SaveFiles()
        self._mode = self._dict.getitem("Radio")
        self._r = libs.Refresher.Refresh()
        self._readArraySize = int(1e6)    # 1e7 is ok, no more, 1e6 works better (with 1MHz sampling) leads to 1array/sec writing rate

        # Queues, Semaphores and Events all derived from the multiprocessing library
        self._dataQ1 = mpQueue()
        self._dataQ2 = mpQueue()
        self._animDataQ1 = mpQueue()
        self._animDataQ2 = mpQueue()
        self._running = mpEvent()
        self._semaphore = Semaphore(3)

        # pyqtSignals
        self.signal = Communicate()
        self.signal.stopMeasurement.connect(self.stopBtn)
        self.signal.measurementProgress.connect(lambda x: self.setProgressBar(x))
        self.signal.warning.connect(self.warnPopUp)
        self.signal.displayRates.connect(lambda x: self.displayRatesOnLCD(x))

        # ################## #
        # Window and widgets #
        # ################## #

        self.setGeometry(500, 300, 500, 200)    # x, y, width, height

        # ## Statusbar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("idle")

        # ## file menue
        # load app, loads laser settings from file
        self.loadApp = QAction('Load settings', self)
        self.loadApp.setShortcut('Ctrl+l')
        self.loadApp.triggered.connect(self.loadDict)

        # save app, saves measurement settings to file, folder is specified by the last load operation
        self.saveApp = QAction('Save settings', self)
        self.saveApp.setShortcut('Ctrl+s')
        # self.saveApp.triggered.connect(lambda: self.GetFileName('Save'))
        self.saveApp.triggered.connect(lambda: self._files.saveSetsDict(self._dict._a, self.getDirectory(), 'Measurement_settings'))

        # convert data to photon-hdf5
        self.convertData = QAction('Convert raw data to photon-hdf5', self)
        # self.convertData.triggered.connect(lambda: self.GetFileName('Convert'))
        self.convertData.triggered.connect(self._files.ConvertToPhotonHDF5)     # This is still not ready!!
                                                                                # A file dialog could hint the method
                                                                                # to the right folder, where it
                                                                                # searches for the temp files on its own

        # save Data to .hdf5 file in a manner that it can be processed by the FretBursts library
        self.saveDataHDF = QAction('This widget is free', self)
        self.saveDataHDF.triggered.connect(lambda: self.GetFileName('free'))

        # close the app
        self.closeApp = QAction('Close', self)
        self.closeApp.setShortcut('Ctrl+q')
        self.closeApp.triggered.connect(self.closeApplication)

        self.menueLayout()

        # ## GroupBox Directory:
        # Group contains:
        # - Location display QLineEdit
        # - Browse directories QPushButton

        filesGroup = QGroupBox('Directory')
        hbox12 = QHBoxLayout()
        filesGroup.setLayout(hbox12)

        self._location = QLineEdit()
        self._location.setMaxLength(50)
        self._location.setReadOnly(True)
        hbox12.addWidget(self._location)
        hbox12.setSpacing(10)

        self._browseButton = QPushButton('Browse', self)
        self._browseButton.clicked.connect(self.getFileLocation)
        hbox12.addWidget(self._browseButton)

        # ## label for different widgets
        self.label1 = QLabel("Laserpower green")
        self.label2 = QLabel("Laserpower red")
        self.label3 = QLabel("Ratio of illumination green/red")
        self.label4 = QLabel("Laser alternation \nfrequency [Hz]")
        self.label5 = QLabel("Measurement duration [s]")
        self.label6 = QLabel("Measurement mode")
        self.label7 = QLabel("Counts in green channel")
        self.label8 = QLabel("Counts in red channel")
        self.label9 = QLabel("% Green")
        self.label10 = QLabel("% Red")

        # ## GroupBox Laser:
        # Group contains:
        # - Laser power red slider
        # - Laser power red spinbox
        # - Laser power green slider
        # - Laser power green spinbox
        # - Laser period percentage slider
        # - Laser period percentage red spinbox
        # - Laser period percentage green spinbox

        laserGroup = QGroupBox("Laser settings")
        hbox1 = QHBoxLayout()
        hbox1.setSpacing(30)
        hbox2 = QHBoxLayout()
        hbox2.setSpacing(30)
        hbox9 = QHBoxLayout()
        hbox11 = QHBoxLayout()
        hbox11.setSpacing(30)
        hbox10 = QHBoxLayout()
        hbox10.setSpacing(30)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.label2)
        vbox1.addLayout(hbox1)
        vbox1.addStretch(1)
        vbox1.addWidget(self.label1)
        vbox1.addLayout(hbox2)
        vbox1.addStretch(1)
        vbox1.addWidget(self.label3)
        vbox1.addLayout(hbox9)
        vbox1.addStretch(1)
        vbox1.addLayout(hbox11)
        vbox1.addStretch(1)
        vbox1.addLayout(hbox10)
        vbox1.addStretch(1)
        laserGroup.setLayout(vbox1)

        hbox11.addWidget(self.label9)
        hbox11.addWidget(self.label10)

        # Laserpower slider red
        self.sld_red = QSlider(Qt.Horizontal, self)
        self.sld_red.setFocusPolicy(Qt.NoFocus)
        self.sld_red.setGeometry(80, 20, 50, 10)
        self.sld_red.setMinimum(0)
        self.sld_red.setMaximum(100)
        self.sld_red.setValue(50)
        self.sld_red.setTickPosition(QSlider.TicksBelow)
        self.sld_red.setTickInterval(20)
        self.sld_red.valueChanged.connect(lambda: self.refreshUI(0, 'sld_red', self.sld_red.value()))
        hbox1.addWidget(self.sld_red)

        # Laserpower QSpinBox red
        self.sb_red = QSpinBox(self)
        self.sb_red.setMinimum(0)
        self.sb_red.setMaximum(100)
        self.sb_red.setValue(50)
        self.sb_red.valueChanged.connect(lambda: self.refreshUI(1, 'sb_red', self.sb_red.value()))
        hbox1.addWidget(self.sb_red)

        # Laserpower slider green
        self.sld_green = QSlider(Qt.Horizontal, self)
        self.sld_green.setFocusPolicy(Qt.NoFocus)
        self.sld_green.setGeometry(160, 40, 100, 30)
        self.sld_green.setMinimum(0)
        self.sld_green.setMaximum(100)
        self.sld_green.setValue(50)
        self.sld_green.setTickPosition(QSlider.TicksBelow)
        self.sld_green.setTickInterval(20)
        self.sld_green.valueChanged.connect(lambda: self.refreshUI(0, 'sld_green', self.sld_green.value()))
        hbox2.addWidget(self.sld_green)

        # Laserpower QSpinBox green
        self.sb_green = QSpinBox(self)
        self.sb_green.setMinimum(0)
        self.sb_green.setMaximum(100)
        self.sb_green.setValue(50)
        self.sb_green.valueChanged.connect(lambda: self.refreshUI(1, 'sb_green', self.sb_green.value()))
        hbox2.addWidget(self.sb_green)

        # Illumination percentage slider
        self.sld_percentage = QSlider(Qt.Horizontal, self)
        self.sld_percentage.setFocusPolicy(Qt.NoFocus)
        self.sld_percentage.setGeometry(160, 40, 100, 30)
        self.sld_percentage.setMinimum(0)
        self.sld_percentage.setMaximum(100)
        self.sld_percentage.setTickPosition(QSlider.TicksBelow)
        self.sld_percentage.setTickInterval(10)
        self.sld_percentage.setValue(50)
        self.sld_percentage.valueChanged.connect(lambda: self.refreshUI(0, 'sld_percentage', self.sld_percentage.value()))
        hbox9.addWidget(self.sld_percentage)

        # Illumination percentage QSpinBox green
        self.sb_percentG = QSpinBox(self)
        self.sb_percentG.setMinimum(0)
        self.sb_percentG.setMaximum(100)
        self.sb_percentG.setValue(50)
        self.sb_percentG.valueChanged.connect(lambda: self.refreshUI(1, 'sb_percentG', self.sb_percentG.value()))
        hbox10.addWidget(self.sb_percentG)

        # Illumination QSpinBox red
        self.sb_percentR = QSpinBox(self)
        self.sb_percentR.setMinimum(0)
        self.sb_percentR.setMaximum(100)
        self.sb_percentR.setValue(50)
        self.sb_percentR.valueChanged.connect(lambda: self.refreshUI(1, 'sb_percentR', self.sb_percentR.value()))
        hbox10.addWidget(self.sb_percentR)

        # ## APD GroupBox
        # Group contains:
        # - Laser alternation frequency spinbox
        # - Measurement mode continuous radiobutton
        # - Measurement mode finite radiobutton
        # - Measurement duration spinbox

        apdGroup = QGroupBox("Measurement")
        hbox3 = QHBoxLayout()
        hbox3.setSpacing(30)
        hbox4 = QHBoxLayout()
        hbox4.setSpacing(30)
        hbox5 = QHBoxLayout()
        hbox5.setSpacing(30)
        vbox2 = QVBoxLayout()
        vbox2.addLayout(hbox3)
        vbox2.addStretch(1)
        vbox2.addLayout(hbox4)
        vbox2.addStretch(1)
        vbox2.addWidget(self.label6)
        vbox2.addLayout(hbox5)
        apdGroup.setLayout(vbox2)

        hbox3.addWidget(self.label4)
        hbox3.addWidget(self.label5)

        # Sample frequence QSpinBox
        self.sb_sampFreq = QSpinBox(self)
        self.sb_sampFreq.setMinimum(100)
        self.sb_sampFreq.setMaximum(100000)
        self.sb_sampFreq.setValue(10000)
        self.sb_sampFreq.valueChanged.connect(lambda: self.refreshUI(1, 'sb_sampFreq', self.sb_sampFreq.value()))
        hbox4.addWidget(self.sb_sampFreq)

        # Radiobutton Continuous Measurement
        self.rb_cont = QRadioButton("Continuous")
        self.rb_cont.setChecked(True)
        self.rb_cont.toggled.connect(lambda: self.refreshUI(2, self.rb_cont, self.rb_finite))
        hbox5.addWidget(self.rb_cont)

        # Radiobutton Finite Measurement
        self.rb_finite = QRadioButton("Finite")
        self.rb_finite.toggled.connect(lambda: self.refreshUI(2, self.rb_finite, self.rb_cont))
        hbox5.addWidget(self.rb_finite)

        # Measurement duration QSpinBox
        self.duration = QSpinBox(self)
        self.duration.setMinimum(0)
        self.duration.setMaximum(300)
        self.duration.setValue(300.0)
        self.duration.valueChanged.connect(lambda: self.refreshUI(1, 'duration', self.duration.value()))
        hbox4.addWidget(self.duration)

        # ## Button GroupBox:
        # Group contains:
        # - Start button
        # - Stop button
        # - ProgressBar

        buttonGroup = QGroupBox("Control")
        hbox6 = QHBoxLayout()
        hbox11 = QHBoxLayout()
        vbox3 = QVBoxLayout()
        vbox3.addLayout(hbox6)
        vbox3.addStretch(1)
        vbox3.addLayout(hbox11)
        vbox3.addStretch(1)
        buttonGroup.setLayout(vbox3)

        # Start button
        self.startButton = QPushButton("Start", self)
        self.startButton.clicked.connect(self.startBtn)
        hbox6.addWidget(self.startButton)

        # Stop button
        self.stopButton = QPushButton("Stop", self)
        self.stopButton.clicked.connect(self.stopBtn)
        hbox6.addWidget(self.stopButton)

        # Progress Bar
        self.progress = QProgressBar(self)
        self.progress.setAlignment(Qt.AlignHCenter)
        self.progress.setRange(0, 100)
        hbox11.addWidget(self.progress)

        # ## LCD display group:
        # Group contains widgets:
        # - LCD display green
        # - LCD display red

        lcdGroup = QGroupBox("Count rates")
        hbox7 = QHBoxLayout()
        hbox8 = QHBoxLayout()
        vbox4 = QVBoxLayout()
        vbox4.addLayout(hbox7)
        vbox4.addLayout(hbox8)
        lcdGroup.setLayout(vbox4)

        hbox7.addWidget(self.label7)
        hbox7.addWidget(self.label8)

        # Green channel count rate
        self.green_lcd = QLCDNumber(self)
        self.green_lcd.setNumDigits(12)
        hbox8.addWidget(self.green_lcd)

        # Red channel count rate
        self.red_lcd = QLCDNumber(self)
        self.red_lcd.setNumDigits(12)
        hbox8.addWidget(self.red_lcd)

        # ## General Layout settings:
        self.centralBox = QGroupBox("Settings")
        self.setCentralWidget(self.centralBox)

        # Arrange groups in grid:
        grid = QGridLayout()
        grid.addWidget(filesGroup, 0, 0, 1, 3)
        grid.addWidget(laserGroup, 1, 0, 2, 2)
        grid.addWidget(apdGroup, 1, 2, 1, 1)
        grid.addWidget(buttonGroup, 2, 2, 1, 1)
        grid.addWidget(lcdGroup, 3, 0, 1, 3)
        self.centralBox.setLayout(grid)

    def menueLayout(self):
        """
        Here the file menue gets evoked. The actions are widgets,
        which get connected to the GetFileName method. It directs
        then to different functionality in a separate class.
        """
        menubar = self.menuBar()
        fileMenue = menubar.addMenu('&File')
        fileMenue.addAction(self.loadApp)
        fileMenue.addAction(self.saveApp)
        fileMenue.addAction(self.convertData)
        fileMenue.addAction(self.saveDataHDF)
        fileMenue.addAction(self.closeApp)

    def getFilename(self):
        start = 'C:/Users/Karoline2'
        path = QFileDialog.getOpenFileName(None, 'Select file', start)
        return path[0]

    def getDirectory(self):
        start = 'C:/Users/Karoline2'
        path = QFileDialog.getExistingDirectory(None, 'Select directory', start, QFileDialog.ShowDirsOnly)
        return path

    def getFileLocation(self):
        path = self.getDirectory()
        self._location.setText(path)

    def loadDict(self):
        path = self.getFilename()
        new_dict = self._files.loadSetsDict(path)
        if new_dict is not None:
            self._dict._a.update(new_dict)
            self.refreshUI(3, self._dict._a, 0)
            self.statusBar.showMessage('Settings updatet!')
        else:
            self.statusBar.showMessage('No valid settings dictionary in that file!')

    def closeApplication(self):
        """Close the app and animation window via file menue."""

        choice = QMessageBox.question(self, 'Quit!', 'Really quit session?', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            try:
                self._anim.__del__()
            except:
                pass
            sys.exit(0)
        else:
            pass

    def closeEvent(self, event):
        """Close also the animation window when the red 'X' button is pressed."""
        try:
            self._anim.__del__()
        except:
            pass
        sys.exit(0)

    def refreshUI(self, changeType, changeKey, value):
        """
        This is the first connection to the widgets. Here the widgets identify
        by changeType (their type) and changeKey (individual key), and pass a value.
        The values can only be applied if the event variable self._running is set
        to False. Changes are processed in refresher.refreshUI method, which returns
        a whole new dictionary.
        :param changeType: str
        :param changeKey: str
        :param value: int or float
        """
        if self._running.is_set():
            self.statusBar.showMessage("Please don't change parameters during measurement. Stop and restart with new settings.")
        else:
            self._dict._a = self._r.refreshUI(changeType, changeKey, value)
            self.refreshAll()

    def refreshRadioButton(self):
        """The radio buttons need a setChecked update, hence the extra method."""
        state = self._dict._a["Radio"]
        if state == 0:
            self.rb_cont.setChecked(True)
        else:
            self.rb_finite.setChecked(True)

    def refreshAll(self):
        """All the widgets get updated with new values."""
        self.sld_red.setValue(self._dict._a["lpower red"])
        self.sld_green.setValue(self._dict._a["lpower green"])
        self.sb_red.setValue(self._dict._a["lpower red"])
        self.sb_green.setValue(self._dict._a["lpower green"])
        self.sb_sampFreq.setValue(self._dict._a["laser frequency"])
        self.duration.setValue(self._dict._a["Duration"])
        self.refreshRadioButton()
        self.sld_percentage.setValue(self._dict._a["laser percentageG"])
        self.sb_percentG.setValue(self._dict._a["laser percentageG"])
        self.sb_percentR.setValue(self._dict._a["laser percentageR"])

    def startBtn(self):
        if not self._running.is_set():
            self._running.set()
            try:
                plt.close(1)
                os.remove("tempAPD1.hdf", "tempAPD2.hdf")
            except:
                pass
            self.startProcesses()
        else:
            print("Already running!")
            self.statusBar.showMessage("Already running!")

    def finalLocation(self):
        """
        Calls the hdf mask, from which the sample name gets retrieved. Combined with
        actual date and time, it creates a new folder in the 'location' directory.
        Measurements settings and hdf info get saved into that new folder as .p and
        .txt files.
        """
        # Hdf information, also the sample name here is important!
        new_folder = None
        if self._location.text():
            new_folder = self._files.saveRawData(self._location.text(), self._dict._a)
        else:
            self.statusBar.showMessage('Please select a file directory!')
        return new_folder

    def startProcesses(self):
        """Get folder and start all processes and threads."""
        new_folder = self.finalLocation()
        if new_folder is None:
            self._running.clear()
            return

        # Initialize processes and waiter thread
        self._counter1 = libs.Counter.Counter(self._running, self._dataQ1, self._readArraySize,
                                              self._semaphore, 1)
        self._counter2 = libs.Counter.Counter(self._running, self._dataQ2, self._readArraySize,
                                              self._semaphore, 2)
        self._laser = libs.Laser.LaserControl(self._running, self._dict, self._semaphore)
        self._anim = libs.Animation.Animation(self._animDataQ1, self._animDataQ2, self.signal)
        self._dataProcesser1 = libs.dataProcesser.DataProcesser(self._dataQ1, self._animDataQ1,
                                                                self._readArraySize, 1, new_folder)
        self._dataProcesser2 = libs.dataProcesser.DataProcesser(self._dataQ2, self._animDataQ2,
                                                                self._readArraySize, 2, new_folder)
        self.statusBar.showMessage("Started!")
        self._anim.run()
        self._u = Thread(target=self.waiter, args=(), name='iterator', daemon=True)

        # Starting all processes and threads
        self._counter1.start()
        self._counter2.start()
        self._laser.start()
        self._u.start()
        self._dataProcesser1.start()
        self._dataProcesser2.start()
        self._anim.animate()    # this command is vicious, it seems everything following
                                # it gets delayed or not executed at all. Best always called last.

    def waiter(self):
        """
        Illumination and APDs acquire the semaphore after initialization of tasks,
        the waiter waits for the semaphore to have its internal counter down to zero
        (when als tasks are ready). Only then the waiter proceeds and does actually
        nothing (mode = 0 --> continuous mode) or starts the progressBar and timing
        (mode 1 --> finite mode). In case of finite mode, the waiter stops the measurement
        after the duration elapses. In continuous mode, the measuremt  must be stopped by
        the user In case of finite mode, the waiter stops the measurement after the
        duration elapses. In continuous mode, the measuremt  must be stopped by the user.
        """
        while self._semaphore.get_value() > 0:
            pass
        self._mode = self._dict._a["Radio"]
        if self._mode == 0:
            self.progress.setRange(0, 0)
        else:
            duration = self._dict._a["Duration"]
            duration_iter = np.arange(duration)
            self.progress.setRange(0, duration)
            for sec in duration_iter:
                time.sleep(1)
                self.signal.measurementProgress.emit(sec)
                if not self._running.is_set():
                    break
            else:
                self.signal.stopMeasurement.emit()

    @pyqtSlot(int)
    def setProgressBar(self, i):
        """Setting the progressbar, it gets called solely by a pyqtSignal from the waiter thread."""
        self.progress.setValue(i)

    @pyqtSlot(list)
    def displayRatesOnLCD(self, x):
        """Setting the lcd numbers with the count rates, it gets called solely by a pyqtSignal from the animation class."""
        self.red_lcd.display(x[1])
        self.green_lcd.display(x[0])

    @pyqtSlot()
    def warnPopUp(self):
        """
        Called from Animation if the count rate of one of the APDs is
        higher than 15000000 Hz (15Mc/s). It pops up a message window,
        informing the user. Currently no stop mechanism is included,
        so the user has to stop the measurement mechanically.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("APD count should not exceed 15 MHz!\nStop the measurement and check APDs and sample.")
        msg.setWindowTitle("APD Warning")
        msg.exec()

    @pyqtSlot()
    def stopBtn(self):
        """Try to stop animation and join all the processes/threads. Extensive checking can be shortened."""
        if self._running.is_set():
            self._running.clear()
            self._anim.anim._stop()
            self.progress.setRange(0, 1)
            while not self._semaphore.get_value() == 3:
                self._semaphore.release()
            # joining
            self.statusBar.showMessage("Stopped! Please wait while data is processed.")
            self._laser.join(timeout=3.0)
            self._u.join(timeout=3.0)
            self._counter1.join(timeout=10.0)
            self._counter2.join(timeout=10.0)
            self._dataProcesser1.join(10.0)
            self._dataProcesser2.join(10.0)
            # extensive checking for joining
            if self._dataProcesser1.is_alive():
                print("Processer 1 did not join.")
                del self._dataProcesser1
            elif self._dataProcesser2.is_alive():
                print("Processer 2 did not join.")
                del self._dataProcesser2
            elif self._counter1.is_alive():
                print("Counter 1 did not join.")
                del self._counter1
            elif self._counter2.is_alive():
                print("Counter 2 did not join.")
                del self._counter2
            elif self._u.is_alive():
                print("Waiter thread did not join.")
                del self._u
            elif self._laser.is_alive():
                print("Laser did not join.")
                del self._laser
            else:
                print("All workers have joined.")
            self.statusBar.showMessage("Stopped and idle!")
        else:
            print("not running at all!")
            self.statusBar.showMessage("Already stopped")
