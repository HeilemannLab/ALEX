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
# from fretbursts import *
import fretbursts as fb
import phconvert
import lmfit
import numpy as np
import fretburstsUI_docu
lmfit.__version__
phconvert.__version__


# For detailed function description and paramters, consult
# http://fretbursts.readthedocs.io/en/latest/reference_manual.html

class BurstAnalysis():
    def __init__(self):
        self._d = None
        self._info = fretburstsUI_docu.FretburstsUIinfo()

        # Parameter default dictionaries:
        self._corrFParam = {"Leakage": 0.11,
                             "Direct excitation": 0.04,
                             "Gamma": 1.}
        self._ALEXparam = {"ALEX period": 4000,
                           "Donor period start": 2180,
                           "Donor period end": 3900,
                           "Acceptor period start": 200,
                           "Acceptor period end": 1800,
                           "Offset": 700}

        self._timetraceParams = {"Binwidth": 0.001,
                                 "T_min": 0,
                                 "T_max": 200,
                                 "Show AexAem": "True",
                                 "Legend": "False"}

        self._backgroundParam = {"Time": 30,
                                 "Min tail": "auto",
                                 "F": 1.7,
                                 "Error metrics": "None",
                                 "Fit all photons": "True"}

        self._bgHistParam = {"Binwidth": 0.0001,
                             "Period": 0,
                             "Y scale": "log",
                             "X scale": "linear",
                             "X unit": "ms",
                             "Show da": "False",
                             "Legend": "True",
                             "Show fit": "True"}

        self._bgTimetraceParam = {"No legend": "False",
                                  "Plot style": {},
                                  "Show da": "False"}

        self._burstSearchParams = {"L": 10,
                                   "m": 20,
                                   "F": 6.0,
                                   "P": "None",
                                   "Dex photon selection": "DAem",
                                   "Aex photon selection": "DAem",
                                   "Max rate": "False",
                                   "Dither": "False"}

        self._plotFretHistEParam = {"Data": "d",
                                    "Binwidth": 0.03,
                                    "Hist style": "bar",
                                    "Weights": "None",
                                    "Add naa": "False",
                                    "Fit from": "kde",
                                    "Show KDE": "False",
                                    "Bandwidth": 0.03}

        self._burstSelectionParam = {"th1": "0",
                                     "th2": np.inf,
                                     "add_naa": "False",
                                     "gamma": 0,
                                     "beta": 0,
                                     "donor_ref": "True",
                                     "add_aex": "True",
                                     "A_laser_weight": 1,
                                     "negate": "False",
                                     "computefret": "True",
                                     "E1": -np.inf,
                                     "E2": np.inf,
                                     "S1": -np.inf,
                                     "S2": np.inf,
                                     "rect": "True",
                                     "bp1": 0,
                                     "bp2": "None",
                                     "time_s1": 0,
                                     "time_s2": "None",
                                     "q": 50,
                                     "low": "False",
                                     "N": 200,
                                     "F": 0,
                                     "P": 0}

        self._exportBurstParam = {"Data": "d",
                                  "Include background": "False",
                                  "Include photon index": "False"}

        self._plotFretHistAJPParams = {"Data": "d",
                                       "Gridsize": 50,
                                       "Cmap": 'alex_light',
                                       "Kind": 'hex',
                                       "Vmax fret": "True",
                                       "Histcolor id": 0}

        self._plotFretHist2DParams = {"Data": "d",
                                      "Vmin": 2,
                                      "Vmax": 0,
                                      "Binwidth": 0.05,
                                      "S max norm": 0.8,
                                      "Interpolation": 'bicubic',
                                      "Cmap": 'hot',
                                      "Under color": 'white',
                                      "Over color": 'white',
                                      "Scatter": "True",
                                      "Scatter ms": 3,
                                      "Scatter color": 'orange',
                                      "Scatter alpha": 0.2,
                                      "Gui sel": "False",
                                      "Cbar ax": "None",
                                      "Grid color": '#D0D0D0'}

    def exitEvent(self):
        fb.plt.close("all")

    def ConvertTypes(self, v):
        if v in ("None", "none"):
            v = None
            return v
        else:
            return v

    def str2bool(self, v):
        if v.lower() in ("True", "true"):
            v = True
            return v
        elif v.lower() in ("False", "false"):
            v = False
            return v
        else:
            print("Parameter should be True or False, apparently it's something else:", v, type(v))

    def LoadFile(self, filename):
        self._d = fb.loader.photon_hdf5(filename)

    def writeCorrF(self):
        self._d.leakage = float(self._corrFParam["Leakage"])
        self._d.dir_ex = float(self._corrFParam["Direct excitation"])
        self._d.gamma = float(self._corrFParam["Gamma"])

    def plotHist(self):
        print(self._info._ALEXhistInfo)
        self._d.add(det_donor_accept=(0, 1),
                    alex_period=float(self._ALEXparam["ALEX period"]),
                    offset=np.int64(self._ALEXparam["Offset"]),
                    D_ON=(float(self._ALEXparam["Donor period start"]), float(self._ALEXparam["Donor period end"])),
                    A_ON=(float(self._ALEXparam["Acceptor period start"]), float(self._ALEXparam["Acceptor period end"])))
        fb.bpl.plot_alternation_hist(self._d)
        fb.plt.show()

    def ApplyPeriods(self):
        fb.loader.alex_apply_period(self._d)
        print("Parameters applied")

    def plotTimetrace(self):
        fb.dplot(self._d,
                 fb.timetrace,
                 binwidth=float(self._timetraceParams["Binwidth"]),
                 tmin=float(self._timetraceParams["T_min"]),
                 tmax=float(self._timetraceParams["T_max"]),
                 show_aa=self.str2bool(self._timetraceParams["Show AexAem"]),
                 legend=self.str2bool(self._timetraceParams["Legend"]))
        fb.plt.show()

    def backgroundEstimation(self):
        self._d.calc_bg(fb.bg.exp_fit,
                        time_s=float(self._backgroundParam["Time"]),
                        tail_min_us='auto',
                        F_bg=float(self._backgroundParam["F"]),
                        error_metrics=self.ConvertTypes(self._backgroundParam["Error metrics"]),
                        fit_allph=self.str2bool(self._backgroundParam["Fit all photons"]))

    def plotBackgroundHist(self):
        fb.dplot(self._d,
                 fb.hist_bg,
                 binwidth=float(self._bgHistParam["Binwidth"]),
                 period=int(self._bgHistParam["Period"]),
                 yscale=self.ConvertTypes(self._bgHistParam["Y scale"]),
                 xscale=self.ConvertTypes(self._bgHistParam["X scale"]),
                 xunit=str(self._bgHistParam["X unit"]),
                 show_da=self.str2bool(self._bgHistParam["Show da"]),
                 legend=self.str2bool(self._bgHistParam["Legend"]),
                 show_fit=self.str2bool(self._bgHistParam["Show fit"]))
        fb.plt.show()

    def plotBackgroundTimetrace(self):
        fb.dplot(self._d,
                 fb.timetrace_bg,
                 nolegend=self.str2bool(self._bgTimetraceParam["No legend"]),
                 plot_style=self._bgTimetraceParam["Plot style"])
        #         show_da=self.str2bool(self._bgTimetraceParam["Show da"]))
        fb.plt.show()

    def burstSearch(self):
        self._d.burst_search(L=int(self._burstSearchParams["L"]),
                             m=int(self._burstSearchParams["m"]),
                             F=float(self._burstSearchParams["F"]),
                             ph_sel=fb.Ph_sel(Dex=self._burstSearchParams["Dex photon selection"], Aex=self._burstSearchParams["Aex photon selection"]),
                             max_rate=self.str2bool(self._burstSearchParams["Max rate"]),
                             dither=self.str2bool(self._burstSearchParams["Dither"]))

    def plotFretHistE(self):
        # self.burstSearch()
        data = getattr(self, "_" + self._plotFretHistEParam["Data"])
        fb.dplot(data,
                 fb.hist_fret,
                 binwidth=float(self._plotFretHistEParam["Binwidth"]),
                 hist_style=self.ConvertTypes(self._plotFretHistEParam["Hist style"]),
                 weights=self.ConvertTypes(self._plotFretHistEParam["Weights"]),
                 add_naa=self.str2bool(self._plotFretHistEParam["Add naa"]),
                 fit_from=self.ConvertTypes(self._plotFretHistEParam["Fit from"]),
                 show_kde=self.str2bool(self._plotFretHistEParam["Show KDE"]),
                 bandwidth=float(self._plotFretHistEParam["Bandwidth"]))
        fb.plt.show()

    def plotFretHistAJP(self):
        data = getattr(self, "_" + self._plotFretHistAJPParams["Data"])
        fb.alex_jointplot(data,
                          gridsize=int(self._plotFretHistAJPParams["Gridsize"]),
                          cmap=self._plotFretHistAJPParams["Cmap"],
                          kind=self._plotFretHistAJPParams["Kind"],
                          vmax_fret=self.str2bool(self._plotFretHistAJPParams["Vmax fret"]),
                          histcolor_id=int(self._plotFretHistAJPParams["Histcolor id"]))
        fb.plt.show()

    def plotFretHist2D(self):
        data = getattr(self, "_" + self._plotFretHist2DParams["Data"])
        fb.dplot(data,
                 fb.hist2d_alex,
                 vmin=float(self._plotFretHist2DParams["Vmin"]),
                 vmax=float(self._plotFretHist2DParams["Vmax"]),
                 binwidth=float(self._plotFretHist2DParams["Binwidth"]),
                 S_max_norm=float(self._plotFretHist2DParams["S max norm"]),
                 interp=self._plotFretHist2DParams["Interpolation"],
                 cmap=self._plotFretHist2DParams["Cmap"],
                 under_color=self._plotFretHist2DParams["Under color"],
                 over_color=self._plotFretHist2DParams["Over color"],
                 scatter=self.str2bool(self._plotFretHist2DParams["Scatter"]),
                 scatter_ms=self._plotFretHist2DParams["Scatter ms"],
                 scatter_color=self._plotFretHist2DParams["Scatter color"],
                 scatter_alpha=float(self._plotFretHist2DParams["Scatter alpha"]),
                 gui_sel=self.str2bool(self._plotFretHist2DParams["Gui sel"]),
                 cbar_ax=self.ConvertTypes(self._plotFretHist2DParams["Cbar ax"]),
                 grid_color=self._plotFretHist2DParams["Grid color"])
        fb.plt.show()

    def exportBurstData(self):
        data = getattr(self, "_" + self._exportBurstParam["Data"])
        Dataframe = fb.bext.burst_data(dx=data,
                                       include_bg=self.str2bool(self._exportBurstParam["Include background"]),
                                       include_ph_index=self.str2bool(self._exportBurstParam["Include photon index"]))
        Dataframe.to_csv(r'f:\Karoline\Code\Fretbursts\burstData.txt', header=None, index=None, sep=' ', mode='a')

    def burstSelection(self, method, parameters):
        method = getattr(fb.select_bursts, method)
        self._ds = self._d.select_bursts(filter_fun=method,
                                         negate=self._burstSelectionParam["negate"],
                                         computefret=self._burstSelectionParam["computefret"],
                                         args=tuple(parameters))
