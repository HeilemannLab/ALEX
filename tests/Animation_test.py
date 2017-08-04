#######################################################################
# File Name: APD-count-Animation
# Project: smFRET
# Version: 1702
# Creation Date: 28.02.2017
# Created By Sebastian Malkusch
# <malkusch@chemie.uni-frankfurt.de>
# Goethe University of Frankfurt
# Physical and Theoretical Chemistry
# Single Molecule Biophysics
######################################################################## */
import sys
from PyQt5.QtWidgets import QGroupBox, QMessageBox, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
from queue import Queue
import threading
import APDcounters
import SampleClock


class AnimationWindow(QMainWindow):
    def __init__(self, figure):
        super(AnimationWindow, self).__init__()

        self.setGeometry(900, 300, 600, 600)
        self.figure = figure
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.figure)
        vbox1 = QVBoxLayout()
        vbox1.addLayout(hbox1)

        box1 = QGroupBox()
        box1.setLayout(vbox1)
        self.setCentralWidget(box1)


class Oszi(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self._parent = parent
        self._width = width
        self._height = height
        self._dpi = dpi
        self.initFigure()

    def initFigure(self):
        # set layout
        # plt.xkcd()
        # create figure with two subplots
        fig = Figure(figsize=(self._width, self._height), dpi=self._dpi)
        self.axes01 = fig.add_subplot(211)
        self.axes02 = fig.add_subplot(212)
        fig.subplots_adjust(hspace=1.0)

        FigureCanvas.__init__(self, fig)
        # self.setParent(self._parent)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._running = False
        self._maxt = 10
        self._dt = 0.1
        self._tdata = [0]
        self._redData = [0]
        self._greenData = [0]
        self.q = Queue()
        self._counter = APDcounters.Counters()
        self._clock = SampleClock.SampleClock()
        self.stop_request = threading.Event()

        self._startButtonHelpText = "This runs the application"
        self._stopButtonHelpText = "This stops the application"

        self.setGeometry(700, 300, 100, 100)
        vbox2 = QVBoxLayout()

        hbox2 = QHBoxLayout()
        self.startButton = QPushButton("start", self)
        self.startButton.setToolTip(self._startButtonHelpText)
        self.startButton.clicked.connect(self.startOszi)

        self.stopButton = QPushButton("stop", self)
        self.stopButton.setToolTip(self._stopButtonHelpText)
        self.stopButton.clicked.connect(self.stopOszi)

        hbox2.addWidget(self.startButton)
        hbox2.addWidget(self.stopButton)
        vbox2.addLayout(hbox2)

        box2 = QGroupBox()
        box2.setLayout(vbox2)
        self.setCentralWidget(box2)

    def initializeOszi(self):
        self.oszi = Oszi(self, width=6, height=5, dpi=100)
        [self.greenLine] = self.oszi.axes01.plot(self._tdata, self._greenData, animated=True, lw=2)
        [self.redLine] = self.oszi.axes02.plot(self._tdata, self._redData, animated=True, lw=2)

        self.greenLine.axes.set_xlim(0, self._maxt)
        self.greenLine.axes.set_ylim(-1, 10.0)
        self.redLine.axes.set_xlim(0, self._maxt)
        self.redLine.axes.set_ylim(10.0, -1)

        self.printLabels()

    def count(self):
        iteration = 0
        l = -1
        while not self.stop_request.is_set():
            g, r = self._counter.readAPD()
            self.q.put(g)
            self.q.put(r)

            iteration += 1
            l *= -1

    def printLabels(self):
        # Set titles of subplots
        self.greenLine.axes.set_title('green APD', fontsize=18)
        self.redLine.axes.set_title('red APD', fontsize=18)
        self.greenLine.axes.set_xlabel("time [s]", fontsize=12)
        self.greenLine.axes.set_ylabel("Intensity", fontsize=12)
        self.redLine.axes.set_xlabel("time [s]", fontsize=12)
        self.redLine.axes.set_ylabel("Intensity", fontsize=12)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.nw.close()
        else:
            event.ignore()

    def update_line(self, i):
        if self._tdata[-1] > self._tdata[0] + self._maxt:
            # self._tdata = [self._tdata[-1]]
            self._tdata = [0]
            self._greenData = [self._greenData[-1]]
            self._redData = [self._redData[-1]]
            self.greenLine.axes.set_xlim(self._tdata[0], self._maxt)
            self.redLine.axes.set_xlim(self._tdata[0], self._maxt)
            # self.oszi.figure.canvas.draw()

        t = self._tdata[-1] + self._dt
        self._tdata.append(t)
        self._greenData.append(self.q.get())
        self.greenLine.set_data(self._tdata, self._greenData)
        self._redData.append(self.q.get())
        self.redLine.set_data(self._tdata, self._redData)
        return self.greenLine, self.redLine

    def startOszi(self):
        if self._running:
            print("already running!")
        else:
            self.stop_request.clear()
            self.initializeOszi()
            self._clock.startClock()
            self._counter.startCounting()

            t = threading.Thread(target=self.count, args=(), name='worker')
            t.setDaemon(True)
            t.start()

            self.nw = AnimationWindow(figure=self.oszi)
            self.Ani = animation.FuncAnimation(self.oszi.figure, self.update_line, blit=True, frames=500, interval=10)
            self.oszi.figure.canvas.draw()
            self.nw.show()
            self._running = True
            print('Started!')

    def stopOszi(self):
        if self._running:
            self.stop_request.set()
            self.Ani._stop()
            self._counter.stopCounting()
            self._clock.stopClock()
            self._running = False
            print('Stopped!')
        else:
            print("not running at all!")


if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    aw = MainWindow()
    aw.show()
    sys.exit(qApp.exec_())
