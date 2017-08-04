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
import numpy as np
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QGroupBox, QMessageBox, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QStatusBar, QAction, QFileDialog, QSlider, QSpinBox, QRadioButton, QProgressBar, QLabel, QGridLayout, QLCDNumber
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot
from multiprocessing import Event as mpEvent
from multiprocessing import Queue as mpQueue
from multiprocessing import freeze_support
from threading import Thread
import libs.dictionary
import libs.Refresher
import libs.Animation
import libs.Counter
import libs.Laser
import libs.dataProcesser
import libs.saveFiles


class Communicate(QObject):
    def __init__(self):
        super(Communicate, self).__init__()

    measurementProgress = pyqtSignal(int)
    startMeasurement = pyqtSignal()
    stopMeasurement = pyqtSignal()
    warning = pyqtSignal()
    displayRates = pyqtSignal(list)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._sets = libs.dictionary.UIsettings()
        self._files = libs.saveFiles.FileDialogue()
        self._data1 = 0
        self._data2 = 0
        self._mode = self._sets.getitem("Radio")
        self._r = libs.Refresher.Refresh()
        self._readArraySize = int(1e6)    # 1e7 is ok, no more, 1e6 works better (1MHz sampling)

        # Queues and Events
        self._dataQ1 = mpQueue()
        self._dataQ2 = mpQueue()
        self._animDataQ1 = mpQueue()
        self._animDataQ2 = mpQueue()
        self._resultQ1 = mpQueue()
        self._resultQ2 = mpQueue()
        self._running = mpEvent()

        # pyqtSignals
        self.signal = Communicate()
        self.signal.stopMeasurement.connect(self.stopBtn)
        self.signal.measurementProgress.connect(lambda x: self.setProgressBar(x))
        self.signal.warning.connect(self.warnPopUp)
        self.signal.startMeasurement.connect(self.startProcesses)
        self.signal.displayRates.connect(lambda x: self.displayRatesOnLCD(x))

        # ##################
        # Window and widgets
        # ##################

        self.setGeometry(500, 300, 500, 200)

        # Statusbar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("idle")

        # file menue
        # load app, loads laser settings from file
        self.loadApp = QAction('Load session', self)
        self.loadApp.setShortcut('Ctrl+l')
        self.loadApp.triggered.connect(lambda: self.GetFileName('Load'))

        # save app, saves laser settings to file, folder is specified by the last load operation
        self.saveApp = QAction('Save session', self)
        self.saveApp.setShortcut('Ctrl+s')
        self.saveApp.triggered.connect(lambda: self.GetFileName('save'))

        # save Data to .txt file
        self.saveData = QAction('Save Data to .txt', self)
        self.saveData.triggered.connect(lambda: self.GetFileName('txt'))

        # save Data to .hdf5 file
        self.saveDataHDF = QAction('Save data to .hdf5', self)
        self.saveDataHDF.triggered.connect(lambda: self.GetFileName('hdf5'))

        # close app
        self.closeApp = QAction('Close', self)
        self.closeApp.setShortcut('Ctrl+q')
        self.closeApp.triggered.connect(self.closeApplication)

        self.menueLayout()

        # label
        # self.label1.setAlignment(Qt.AlignVCenter)
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

        # GroupBox Laser:
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
        vbox1.addWidget(self.label1)
        vbox1.addLayout(hbox1)
        vbox1.addWidget(self.label2)
        vbox1.addLayout(hbox2)
        vbox1.addWidget(self.label3)
        vbox1.addLayout(hbox9)
        vbox1.addLayout(hbox11)
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
        self.sld_red.setTickPosition(QSlider.TicksBelow)
        self.sld_red.setTickInterval(20)
        self.sld_red.valueChanged.connect(lambda: self.refreshUI(0, 'sld_red', self.sld_red.value()))
        hbox1.addWidget(self.sld_red)

        # Laserpower QSpinBox red
        self.sb_red = QSpinBox(self)
        self.sb_red.setMinimum(0)
        self.sb_red.setMaximum(100)
        self.sb_red.valueChanged.connect(lambda: self.refreshUI(1, 'sb_red', self.sb_red.value()))
        hbox1.addWidget(self.sb_red)

        # Laserpower slider green
        self.sld_green = QSlider(Qt.Horizontal, self)
        self.sld_green.setFocusPolicy(Qt.NoFocus)
        self.sld_green.setGeometry(160, 40, 100, 30)
        self.sld_green.setMinimum(0)
        self.sld_green.setMaximum(100)
        self.sld_green.setTickPosition(QSlider.TicksBelow)
        self.sld_green.setTickInterval(20)
        self.sld_green.valueChanged.connect(lambda: self.refreshUI(0, 'sld_green', self.sld_green.value()))
        hbox2.addWidget(self.sld_green)

        # Laserpower QSpinBox green
        self.sb_green = QSpinBox(self)
        self.sb_green.setMinimum(0)
        self.sb_green.setMaximum(100)
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

        # APD GroupBox
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
        self.sb_sampFreq.setMinimum(10)
        self.sb_sampFreq.setMaximum(100000)
        self.sb_sampFreq.setValue(1000)
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

        # Button GroupBox
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
        self.startButton = QPushButton("start", self)
        self.startButton.clicked.connect(self.startBtn)
        hbox6.addWidget(self.startButton)

        # Stop button
        self.stopButton = QPushButton("stop", self)
        self.stopButton.clicked.connect(self.stopBtn)
        hbox6.addWidget(self.stopButton)

        # Progress Bar
        self.progress = QProgressBar(self)
        self.progress.setAlignment(Qt.AlignHCenter)
        self.progress.setRange(0, 100)
        hbox11.addWidget(self.progress)

        # Count rates on LCD
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

        # General Layout settings
        self.centralBox = QGroupBox("Settings")
        self.setCentralWidget(self.centralBox)

        grid = QGridLayout()
        grid.addWidget(laserGroup, 0, 0, 2, 2)
        grid.addWidget(apdGroup, 0, 2, 1, 1)
        grid.addWidget(buttonGroup, 1, 2, 1, 1)
        grid.addWidget(lcdGroup, 2, 0, 1, 3)
        self.centralBox.setLayout(grid)

    def menueLayout(self):
        menubar = self.menuBar()
        fileMenue = menubar.addMenu('&File')
        fileMenue.addAction(self.loadApp)
        fileMenue.addAction(self.saveApp)
        fileMenue.addAction(self.saveData)
        fileMenue.addAction(self.saveDataHDF)
        fileMenue.addAction(self.closeApp)

    def GetFileName(self, keyword):
        f = 'C:\Karoline2\Code'
        filename = QFileDialog.getSaveFileName(self, 'File dialogue', f)
        self._files.refreshSettings(self._sets._a)
        self._sets._a = self._files.SortTasks(keyword, filename[0], self._data1, self._data2)
        self.refreshAll()
        self.statusBar.showMessage("Beware that only data from finite measurements can be saved. Don't change parameters during a measurement!")

    def closeApplication(self):
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
        try:
            self._anim.__del__()
        except:
            pass
        sys.exit(0)

    def refreshUI(self, changeType, changeKey, value):
        if self._running.is_set():
            self.statusBar.showMessage("Please don't change parameters during measurement. Stop and restart with new settings.")
        else:
            self._sets._a = self._r.refreshUI(changeType, changeKey, value)
            self.refreshAll()

    def refreshRadioButton(self):
        state = self._sets.getitem("Radio")
        if state == 0:
            self.rb_cont.setChecked(True)
        else:
            self.rb_finite.setChecked(True)

    def refreshAll(self):
        self.sld_red.setValue(self._sets.getitem("lpower red"))
        self.sld_green.setValue(self._sets.getitem("lpower green"))
        self.sb_red.setValue(self._sets.getitem("lpower red"))
        self.sb_green.setValue(self._sets.getitem("lpower green"))
        self.sb_sampFreq.setValue(self._sets.getitem("laser frequency"))
        self.duration.setValue(self._sets.getitem("Duration"))
        self.refreshRadioButton()
        self.sld_percentage.setValue(self._sets.getitem("laser percentageG"))
        self.sb_percentG.setValue(self._sets.getitem("laser percentageG"))
        self.sb_percentR.setValue(self._sets.getitem("laser percentageR"))

    def startBtn(self):
        if not self._running.is_set():
            self._running.set()
            try:
                plt.close(1)
            except:
                pass
            self.startProcesses()
            self.statusBar.showMessage("Started!")
        else:
            print("Already running!")
            self.statusBar.showMessage("Already running!")

    def startProcesses(self):
        # Initialize processes and waiter thread
        self._counter1 = libs.Counter.Counter(self._running, self._dataQ1, self._readArraySize, 1)
        self._counter2 = libs.Counter.Counter(self._running, self._dataQ2, self._readArraySize, 2)
        self._laser = libs.Laser.LaserControl(self._running, self._sets)
        self._anim = libs.Animation.Animation(self._animDataQ1, self._animDataQ2, self.signal)
        self._dataProcesser1 = libs.dataProcesser.DataProcesser(self._dataQ1, self._animDataQ1, self._resultQ1, self._readArraySize, 1)
        self._dataProcesser2 = libs.dataProcesser.DataProcesser(self._dataQ2, self._animDataQ2, self._resultQ2, self._readArraySize, 2)
        self._anim.run()
        self._u = Thread(target=self.waitForIteration, args=(), name='iterator', daemon=True)

        # Starting all processes and threads
        self._counter1.start()
        self._counter2.start()
        self._laser.start()
        self._u.start()
        self._dataProcesser1.start()
        self._dataProcesser2.start()
        self._anim.animate()    # this command is vicious, it seems everything after it gets delayed or not executed at all. best always called last.

    def waitForIteration(self):
        time.sleep(3)
        self._mode = self._sets.getitem("Radio")
        if self._mode == 0:
            self.progress.setRange(0, 0)
        else:
            duration = self._sets.getitem("Duration")
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
        self.progress.setValue(i)

    @pyqtSlot(list)
    def displayRatesOnLCD(self, x):
        self.red_lcd.display(x[1])
        self.green_lcd.display(x[0])

    @pyqtSlot()
    def warnPopUp(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("APD count should not exceed 800 kHz")
        msg.setWindowTitle("APD warning")
        msg.exec()

    @pyqtSlot()
    def stopBtn(self):
        if self._running.is_set():
            self._running.clear()
            self._anim.anim._stop()
            self.progress.setRange(0, 1)
            try:
                self._data1 = self._resultQ1.get(timeout=5.0)
                self._data2 = self._resultQ2.get(timeout=5.0)
            except:
                print("No results queued")
            self._laser.join(timeout=1.0)
            self._u.join(timeout=1.0)
            self._counter1.join(timeout=1.0)
            self._counter2.join(timeout=1.0)
            self._dataProcesser1.join(timeout=2.0)
            self._dataProcesser2.join(timeout=2.0)
            if self._dataProcesser2.is_alive() or self._dataProcesser1.is_alive():
                print("Not joined.")
                del self._dataProcesser1, self._dataProcesser2, self._anim
            else:
                print("All workers have joined.")
            self.statusBar.showMessage("Stopped!")
        else:
            print("not running at all!")
            self.statusBar.showMessage("Already stopped")


if __name__ == "__main__":
    freeze_support()
    qApp = QApplication(sys.argv)
    aw = MainWindow()
    aw.show()
    sys.exit(qApp.exec_())
