'''######################################################################
# File Name: Animation.py
# Project: ALEX
# Version:
# Creation Date: 2017/03/16
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from matplotlib import pyplot, animation
from matplotlib.lines import Line2D
import seaborn as sns


class Animation:
    """
    Animation class is designed specially to make the
    matplotlib.animation.FuncAnimation method work. The plots
    are Line2D graphs, also data can be plotted in two subplots
    ('plot2'), or in one ('plot') as it's usual for FRET. The
    'updateAnimation' also feeds data to the LCD Panels in the
    mainwindow via pyqtSignal.
    """
    def __init__(self, animDataQ1, animDataQ2, signal):
        """
        @param animDataQ1: multiprocessing queue
        @param animDataQ2: mulitprocessing queue
        @param signal: class instance
        """
        self._animDataQ1 = animDataQ1
        self._animDataQ2 = animDataQ2
        self._signal = signal
        self._dt = 0.1
        self._tdata = [0]
        self._greenData = [0]
        self._redData = [0]
        self._greenLine = 0
        self._redLine = 0
        self._figure = pyplot.figure()
        self.anim = 0
        self._axLimit = 1e3

    def run(self):
        """
        To start animation a run method is necessary. Therefore
        it's most certainly a threading.Thread subclass.
        """
        self.plot()

    def plot(self):
        """
        This plot function provides one plot, where both datasets
        are plotted into. The red APD data is multiplied with -1.
        The style is a seaborn one.
        """
        # pyplot.style.use('seaborn-deep')
        sns.set()   # seaborn plot style
        ax = self._figure.add_subplot(111)

        self._greenLine = Line2D([], [], color='green')
        self._redLine = Line2D([], [], color='red')

        ax.add_line(self._greenLine)
        ax.add_line(self._redLine)

        ax.set_xlim(0, 10)
        ax.set_ylim(-self._axLimit, self._axLimit)

        ax.set_xlabel("time")
        ax.set_ylabel("counts/sec")

    def plot2(self):
        """
        This plot function provides two subplots with the red
        channel data on the second plotting it in negative direction.
        """
        pyplot.style.use('seaborn-deep')

        ax_green = self._figure.add_subplot(2, 1, 1)
        ax_red = self._figure.add_subplot(2, 1, 2)

        self._greenLine = Line2D([], [], color='green')
        self._redLine = Line2D([], [], color='red')

        ax_green.add_line(self._greenLine)
        ax_red.add_line(self._redLine)

        ax_green.set_xlim(0, 10)
        ax_red.set_xlim(0, 10)
        ax_green.set_ylim(-30, 10000000)
        ax_red.set_ylim(1000000, -30)

        ax_green.set_xlabel("time in [s]")
        ax_red.set_xlabel("time in [s]")
        ax_green.set_ylabel("counts")
        ax_red.set_ylabel("counts")

        ax_green.set_title("Green channel")
        ax_red.set_title("Red channel")

        # pyplot.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        self._figure.subplots_adjust(left=0.2, bottom=0.1, right=0.8,
                                     top=0.9, wspace=0.1, hspace=0.8)

    def initAnimation(self):
        """
        'initAnimation' creates the initial Window for the
        'funcAnimation' method. It it passed as a parameter,
        but it's optional, so this can be skipped. But note
        that the LinePlot has to be initialized then otherwise.
        """
        self._greenLine.set_data([], [])
        self._redLine.set_data([], [])
        return self._greenLine, self._redLine,

    def updateAnimation(self, i):
        """
        The data is retrieved from the queues in an try/except
        block to avoid errors/blocking. In there also the signal
        'displayRates' gets emitted with a two-item-list[green, red].
        @param i: iterable
        This parameter is necessary for the animation, it passes the
        'frames' argument as an iterator somehow. Documtation does
        not entirely reveal how this works.
        """
        if self._tdata[-1] > 10:
            self._tdata = [0]
            self._greenData = [self._greenData[-1]]
            self._redData = [self._redData[-1]]
        # This try/except section looks ugly, but it works good for unstable data influx.
        # The print error statement in except can be neglected in real mesurements.
        try:
            green = float(1e8) * self._animDataQ1.get(timeout=1.0)
            if (green >= 15000000):
                self._signal.warning.emit()
        except:
            green = 0
            # print("error getting data for animation")
            # pass
        try:
            red = float(1e8) * (-1) * self._animDataQ2.get(timeout=1.0)
            if ((-1 * red) >= 15000000):
                self._signal.warning.emit()
        except:
            red = 0
        self._greenData.append(green)
        self._redData.append(red)
        x = [int(green), int(-1 * red)]
        self._signal.displayRates.emit(x)

        self._tdata.append(self._tdata[-1] + self._dt)
        self._greenLine.set_data(self._tdata, self._greenData)
        self._redLine.set_data(self._tdata, self._redData)
        return self._greenLine, self._redLine,

    def animate(self):
        """
        FuncAnimation updates #(frames), in #(interval) milliseconds.
        It's using blitting, therefore the axis will not get updated.
        """
        self.anim = animation.FuncAnimation(self._figure,
                                            self.updateAnimation,
                                            init_func=self.initAnimation,
                                            frames=100,
                                            interval=100,
                                            blit=True,
                                            repeat=True)
        pyplot.show()

    def __del__(self):
        """
        Use to control program flow
        """
        print("Animation class instance removed")
