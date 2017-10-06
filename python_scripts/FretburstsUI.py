'''######################################################################
# File Name: FretburstsUI.py
# Project: Fretbursts for ALEX
# Version:
# Creation Date: 06/10/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import sys
from PyQt5.QtWidgets import (QGroupBox, QMainWindow, QPushButton, QLineEdit,
                             QFileDialog, QStatusBar, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLabel, QCheckBox, QComboBox, QTextEdit,
                             QMessageBox)

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor


class EmittingStream(QObject):
    """
    This class provides the cloning of the
    rich fretbursts printing volume into the
    info widgets in the main window.
    """
    message = pyqtSignal(str)

    def __init__(self, parent=None):
        super(EmittingStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message + '\n'))

    def flush(self):
        sys.__stdout__.flush()


class FretburstsUI(QMainWindow):
    def __init__(self):
        super(FretburstsUI, self).__init__()
        self._centralBox = QGroupBox()
        self.setCentralWidget(self._centralBox)
        self.setGeometry(500, 300, 900, 500)

        self._paramList = {"E": ["E1", "E2"],
                           "ES": ["E1", "E2", "S1", "S2", "rect"],
                           "ES_ellips": ["E1", "E2", "S1", "S2"],
                           "ES_rect": ["E1", "E2", "S1", "S2"],
                           "brightness": ["th1", "th2", "gamma", "beta", "donor_ref"],
                           "consecutive": ["th1", "th2", "kind"],
                           "na": ["th1", "th2"],
                           "na_bg": ["F"],
                           "na_bg_p": ["P", "F"],
                           "naa": ["th1", "th2", "gamma", "beta", "donor_ref"],
                           "naa_bg": ["F"],
                           "naa_bg_p": ["P", "F"],
                           "nd": ["th1", "th2"],
                           "nd_bg": ["F"],
                           "nd_bg_p": ["P", "F"],
                           "nda_percentile": ["q", "low", "gamma", "add_naa"],
                           "nt_bg": ["F"],
                           "nt_bg_p": ["P", "F"],
                           "peak_phrate": ["th1", "th2"],
                           "period": ["bp1", "bp2"],
                           "sbr": ["th1", "th2"],
                           "single": ["th1"],
                           "size": ["th1", "th2", "add_naa", "beta", "donor_ref", "add_aex", "A_laser_weight"],
                           "str_G": ["gamma", "donor_ref"],
                           "time": ["time_s1", "time_s2"],
                           "topN_max_rate": ["N"],
                           "topN_nda": ["N", "gamma", "add_naa"],
                           "topN_sbr": ["N"],
                           "width": ["th1", "th2"]}
        self._burstSelectionParamList = []

        ###########
        # WIDGETS #
        ###########

        # Statusbar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("idle")

        # ######### Print window group ##########
        # Standart out print widget
        self._printWindow = QTextEdit(self)
        self._printWindow.setReadOnly(True)
        self._myStream = EmittingStream()
        self._myStream.message.connect(self.on_EmittingStream_message)

        sys.stdout = self._myStream

        # Import bursts_analysis(fretbursts) here to catch all output in myStream()
        import fretburstsUI_docu
        import burst_analysis
        self._burstAnalysis = burst_analysis.BurstAnalysis()
        self._info = fretburstsUI_docu.FretburstsUIinfo()
        print(self._info._initialInfo)

        # ######### File group widgets ##########
        # Load file button
        self._getFileButton = QPushButton('Select file', self)
        self._getFileButton.setToolTip('Click here to select a file to analyze')
        self._getFileButton.clicked.connect(self.openFileNameDialog)

        # Show filename button
        self._showFile = QLineEdit(self)
        self._showFile.setReadOnly(True)

        # ######### Correctionfactor group widgets ###########
        # Correctionfactor Combobox
        self._corrFParam = QComboBox(self)
        self._corrFParam.addItems(["Leakage",
                                   "Direct excitation",
                                   "Gamma"])
        self._corrFParam.activated[str].connect(lambda x: self.ComboBox(x, 'corrF'))

        # Correctionfactors values input line
        self._corrFParamValues = QLineEdit(self)
        self._corrFParamValues.setMaxLength(10)
        self._corrFParamValues.setAlignment(Qt.AlignRight)
        self._corrFParamValues.setFont(QFont("Arial", 10))
        self._corrFParamValues.textChanged.connect(self.LineEdit)

        # ######### ALEX parameter group widgets ##########
        # ALEX parameter Combobox
        self._ALEXparam = QComboBox(self)
        self._ALEXparam.addItems(["ALEX period",
                                  "Donor period start",
                                  "Donor period end",
                                  "Acceptor period start",
                                  "Acceptor period end",
                                  "Offset"])
        self._ALEXparam.activated[str].connect(self.ALEXparam)

        # ALEX parameter values input line
        self._ALEXValues = QLineEdit(self)
        self._ALEXValues.setMaxLength(10)
        self._ALEXValues.setAlignment(Qt.AlignRight)
        self._ALEXValues.setFont(QFont("Arial", 10))
        self._ALEXValues.textChanged.connect(self.ALEXValues)

        # ######### ALEX Histogram plot group widgets ##########
        # ALEX Histogram plot button
        self._plotHistButton = QPushButton('Plot ALEX histogram', self)
        self._plotHistButton.setToolTip('Click here to select a file to analyze')
        self._plotHistButton.clicked.connect(self._burstAnalysis.plotHist)

        # Separate Label for checkbox
        self._label5 = QLabel('Apply Parameters?')

        # Checkbox to apply ALEX parameters
        self._checkParams = QCheckBox('', self)
        self._checkParams.stateChanged.connect(self._burstAnalysis.ApplyPeriods)

        # ######### Timetrace plot group widgets ##########
        # Timetrace plot button
        self._plotTimetraceButton = QPushButton('Plot timetrace', self)
        self._plotTimetraceButton.setToolTip('Click here to plot the timetrace')
        self._plotTimetraceButton.clicked.connect(self._burstAnalysis.plotTimetrace)

        # Timetrace parameter Combobox
        self._timetraceParams = QComboBox()
        self._timetraceParams.addItems(["Binwidth",
                                        "T_min",
                                        "T_max",
                                        "Show AexAem",
                                        "Legend"])
        self._timetraceParams.activated[str].connect(self.TimetraceParams)

        # Timetrace parameter's values input line
        self._timetraceParamValues = QLineEdit()
        self._timetraceParamValues.setMaxLength(10)
        self._timetraceParamValues.setAlignment(Qt.AlignRight)
        self._timetraceParamValues.setFont(QFont("Arial", 10))
        self._timetraceParamValues.textChanged.connect(self.TimetraceParamValues)

        # ######### Background estimation group widgets ##########
        # Background parameter Combobox
        self._backgroundParams = QComboBox()
        self._backgroundParams.addItems(["Time",
                                         "F",
                                         "Error metrics",
                                         "Fit all photons"])
        self._backgroundParams.activated[str].connect(self.BackgroundParams)

        # Background estimation parameter's values input line
        self._backgroundParamValues = QLineEdit()
        self._backgroundParamValues.setMaxLength(10)
        self._backgroundParamValues.setAlignment(Qt.AlignRight)
        self._backgroundParamValues.setFont(QFont("Arial", 10))
        self._backgroundParamValues.textChanged.connect(self.BackgroundParamValues)

        # Background estimation Checkbox
        self._checkBGParams = QCheckBox('', self)
        self._checkBGParams.stateChanged.connect(self._burstAnalysis.backgroundEstimation)

        # Seperate label for BG checkbox
        self._label4 = QLabel('Estimate background with these parameters?')

        # Background histogram parameter ComboBox
        self._bgHistParams = QComboBox()
        self._bgHistParams.addItems(["Binwidth",
                                     "Period",
                                     "Y scale",
                                     "X scale",
                                     "X unit",
                                     "Show da",
                                     "Legend",
                                     "Show fit"])
        self._bgHistParams.activated[str].connect(self.BgHistParams)

        # Background histogram parameter input line
        self._bgHistParamValues = QLineEdit()
        self._bgHistParamValues.setMaxLength(10)
        self._bgHistParamValues.setAlignment(Qt.AlignRight)
        self._bgHistParamValues.setFont(QFont("Arial", 10))
        self._bgHistParamValues.textChanged.connect(self.BgHistParamValues)

        # Background histogram plot button
        self._bgHistButton = QPushButton('Plot background histogram', self)
        self._bgHistButton.setToolTip('Click here to plot background histogram')
        self._bgHistButton.clicked.connect(self._burstAnalysis.plotBackgroundHist)

        # Background timetrace parameter Combobox
        self._bgTimetraceParams = QComboBox()
        self._bgTimetraceParams.addItems(["No legend",
                                          "Plot style"])
        #                                  "Show da"]) Apparently tritemio removed this parameter
        self._bgTimetraceParams.activated[str].connect(self.BgTimetraceParams)

        # Background timetrace parameter input line
        self._bgTimetraceParamValues = QLineEdit()
        self._bgTimetraceParamValues.setMaxLength(10)
        self._bgTimetraceParamValues.setAlignment(Qt.AlignRight)
        self._bgTimetraceParamValues.setFont(QFont("Arial", 10))
        self._bgTimetraceParamValues.textChanged.connect(self.BgTimetraceParamValues)

        # Background timetrace plot button
        self._bgTimetraceButton = QPushButton('Plot background timetrace', self)
        self._bgTimetraceButton.setToolTip('Click here to plot background timetrace')
        self._bgTimetraceButton.clicked.connect(self._burstAnalysis.plotBackgroundTimetrace)

        # ######### Burst search ##########
        # Burst search parameter ComboBox
        self._burstSearchParam = QComboBox()
        self._burstSearchParam.addItems(["L",
                                         "m",
                                         "F",
                                         "Dex photon selection",
                                         "Aex photon selection",
                                         "Max rate",
                                         "Dither"])
        self._burstSearchParam.activated[str].connect(self.BurstSearchParams)

        # Burst search parameter values input line
        self._burstSearchParamValues = QLineEdit()
        self._burstSearchParamValues.setAlignment(Qt.AlignRight)
        self._burstSearchParamValues.setFont(QFont("Arial", 10))
        self._burstSearchParamValues.textChanged.connect(self.BurstSearchParamValues)

        # Burstsearch Checkbox
        self._checkBurstSearchParams = QCheckBox('', self)
        self._checkBurstSearchParams.stateChanged.connect(self._burstAnalysis.burstSearch)

        # Seperate label for BG checkbox
        self._label3 = QLabel('Search for bursts with these parameters?')

        # Plot Efficiency only FRET histogram
        # Plot E only FRET histogram parameter Combobox
        self._plotFretHistEParam = QComboBox()
        self._plotFretHistEParam.addItems(["Data",
                                           "Binwidth",
                                           "Hist style",
                                           "Weights",
                                           "Add naa",
                                           "Fit from",
                                           "Show KDE",
                                           "Bandwidth"])
        self._plotFretHistEParam.activated[str].connect(self.PlotFretHistEParams)

        # Plot E only FRET histogram parameters values input line
        self._plotFretHistEParamValues = QLineEdit()
        self._plotFretHistEParamValues.setMaxLength(10)
        self._plotFretHistEParamValues.setAlignment(Qt.AlignRight)
        self._plotFretHistEParamValues.setFont(QFont("Arial", 10))
        self._plotFretHistEParamValues.textChanged.connect(self.PlotFretHistEParamValues)

        # Plot E only FRET histogram Button
        self._plotFretHistEButton = QPushButton('Plot Efficiency FRET histogram', self)
        self._plotFretHistEButton.setToolTip('Click here to plot the E only FRET histogram')
        self._plotFretHistEButton.clicked.connect(self._burstAnalysis.plotFretHistE)

        # ALEX joint plot FRET histogram
        # ALEX joint plot FRET histogram parameter Combobox
        self._plotFretHistAJPParam = QComboBox()
        self._plotFretHistAJPParam.addItems(["Data",
                                             "Gridsize",
                                             "Cmap",
                                             "Kind",
                                             "Vmax fret",
                                             "Histcolor id"])
        self._plotFretHistAJPParam.activated[str].connect(self.PlotFretHistAJPParams)

        # ALEX joint plot FRET histogram parameters values input line
        self._plotFretHistAJPParamValues = QLineEdit()
        self._plotFretHistAJPParamValues.setMaxLength(10)
        self._plotFretHistAJPParamValues.setAlignment(Qt.AlignRight)
        self._plotFretHistAJPParamValues.setFont(QFont("Arial", 10))
        self._plotFretHistAJPParamValues.textChanged.connect(self.PlotFretHistAJPParamValues)

        # ALEX joint plot FRET histogram Button
        self._plotFretHistAJPButton = QPushButton('Plot ALEX joint FRET histogram', self)
        self._plotFretHistAJPButton.setToolTip('Click here to plot the ALEX joint FRET histogram')
        self._plotFretHistAJPButton.clicked.connect(self._burstAnalysis.plotFretHistAJP)

        # Plot 2D FRET histogram
        # Plot 2D FRET histogram parameter Combobox
        self._plotFretHist2DParam = QComboBox()
        self._plotFretHist2DParam.addItems(["Data",
                                            "Vmin",
                                            "Vmax",
                                            "Binwidth",
                                            "S max norm",
                                            "Interpolation",
                                            "Cmap",
                                            "Under color",
                                            "Over color",
                                            "Scatter",
                                            "Scatter ms",
                                            "Scatter color",
                                            "Scatter alpha",
                                            "Gui sel",
                                            "Cbar ax",
                                            "Grid color"])

        self._plotFretHist2DParam.activated[str].connect(self.PlotFretHist2DParams)

        # Plot 2D FRET histogram parameters values input line
        self._plotFretHist2DParamValues = QLineEdit()
        self._plotFretHist2DParamValues.setMaxLength(10)
        self._plotFretHist2DParamValues.setAlignment(Qt.AlignRight)
        self._plotFretHist2DParamValues.setFont(QFont("Arial", 10))
        self._plotFretHist2DParamValues.textChanged.connect(self.PlotFretHist2DParamValues)

        # Plot 2D FRET histogram Button
        self._plotFretHist2DButton = QPushButton('Plot 2D FRET histogram', self)
        self._plotFretHist2DButton.setToolTip('Click here to plot the 2D FRET histogram')
        self._plotFretHist2DButton.clicked.connect(self._burstAnalysis.plotFretHist2D)

        # Burst selection
        # Burst selection method Combobox
        self._burstSelectionMethod = QComboBox()
        self._burstSelectionMethod.addItems(["E",
                                             "ES",
                                             "ES_ellips",
                                             "ES_rect",
                                             "brightness",
                                             "consecutive",
                                             "na",
                                             "na_bg",
                                             "na_bg_p",
                                             "naa",
                                             "naa_bg",
                                             "naa_bg_p",
                                             "nd",
                                             "nd_bg",
                                             "nd_bg_p",
                                             "nda_percentile",
                                             "nt_bg",
                                             "nt_bg_p",
                                             "peak_phrate",
                                             "period",
                                             "sbr",
                                             "single",
                                             "size",
                                             "str_G",
                                             "time",
                                             "topN_max_rate",
                                             "topN_nda",
                                             "topN_sbr",
                                             "width"])
        self._burstSelectionMethod.activated[str].connect(self.BurstSelectionMethod)
        self._label6 = QLabel("Chose a method how to select bursts.")

        # Burst Selection Method parameters combobox
        self._burstSelectionParams = QComboBox()
        self._burstSelectionParams.activated[str].connect(self.BurstSelectionParams)

        # Burst Selection parameter input line
        self._burstSelectionParamValues = QLineEdit()
        self._burstSelectionParamValues.setMaxLength(10)
        self._burstSelectionParamValues.setAlignment(Qt.AlignRight)
        self._burstSelectionParamValues.setFont(QFont("Arial", 10))
        self._burstSelectionParamValues.textChanged.connect(self.BurstSelectionParamValue)

        # Burst selection checkbox
        self._checkSelectionParams = QCheckBox()
        self._checkSelectionParams.stateChanged.connect(self.BurstSelectionParameters)

        # Individual label for Selection checkbox
        self._label7 = QLabel("Select bursts with these parameters?")

        # # Export Burst Data
        # Export Burst Data Parameter Combobox
        self._exportBurstDataParams = QComboBox()
        self._exportBurstDataParams.addItems(["Data",
                                              "Include background",
                                              "Include photon index"])
        self._exportBurstDataParams.activated[str].connect(self.ExportBurstDataParam)

        # Export Burst data parameter input line
        self._exportBurstDataParamValues = QLineEdit()
        self._exportBurstDataParamValues.setMaxLength(10)
        self._exportBurstDataParamValues.setAlignment(Qt.AlignRight)
        self._exportBurstDataParamValues.setFont(QFont("Arial", 10))
        self._exportBurstDataParamValues.textChanged.connect(self.ExportBurstDataParamValues)

        # Export Burst Data Checkbox
        self._ExportSelectionButton = QPushButton("Export selected dataframe")
        self._ExportSelectionButton.clicked.connect(self._burstAnalysis.exportBurstData)

        ###########
        # Layouts #
        ###########

        box1 = QVBoxLayout()
        box1.addWidget(self._getFileButton)
        box1.addWidget(self._showFile)
        group1 = QGroupBox('File')
        group1.setLayout(box1)

        box2 = QHBoxLayout()
        box2.addWidget(self._corrFParam)
        box2.addWidget(self._corrFParamValues)
        group2 = QGroupBox('Correction parameters')
        group2.setLayout(box2)

        box3 = QHBoxLayout()
        box3.addWidget(self._ALEXparam)
        box3.addWidget(self._ALEXValues)
        box4 = QHBoxLayout()
        box4.addWidget(self._label5)
        box4.addWidget(self._checkParams)
        box5 = QVBoxLayout()
        box5.addLayout(box3)
        box5.addWidget(self._plotHistButton)
        box5.addLayout(box4)
        group3 = QGroupBox('Alternation parameters')
        group3.setLayout(box5)

        box6 = QHBoxLayout()
        box6.addWidget(self._timetraceParams)
        box6.addWidget(self._timetraceParamValues)
        box7 = QVBoxLayout()
        box7.addLayout(box6)
        box7.addWidget(self._plotTimetraceButton)
        group4 = QGroupBox('Timetrace')
        group4.setLayout(box7)

        box8 = QHBoxLayout()
        box8.addWidget(self._backgroundParams)
        box8.addWidget(self._backgroundParamValues)
        box21 = QHBoxLayout()
        box21.addWidget(self._label4)
        box21.addWidget(self._checkBGParams)
        box9 = QHBoxLayout()
        box9.addWidget(self._bgHistParams)
        box9.addWidget(self._bgHistParamValues)
        box9.addWidget(self._bgHistButton)
        box22 = QHBoxLayout()
        box22.addWidget(self._bgTimetraceParams)
        box22.addWidget(self._bgTimetraceParamValues)
        box22.addWidget(self._bgTimetraceButton)
        box10 = QVBoxLayout()
        box10.addLayout(box8)
        box10.addLayout(box21)
        box10.addLayout(box9)
        box10.addLayout(box22)
        group5 = QGroupBox('Background Estimation')
        group5.setLayout(box10)

        box11 = QHBoxLayout()
        box11.addWidget(self._burstSearchParam)
        box11.addWidget(self._burstSearchParamValues)
        box12 = QHBoxLayout()
        box12.addWidget(self._label3)
        box12.addWidget(self._checkBurstSearchParams)
        box13 = QVBoxLayout()
        box13.addLayout(box11)
        box13.addLayout(box12)
        group6 = QGroupBox('Burst search')
        group6.setLayout(box13)

        box14 = QHBoxLayout()
        box14.addWidget(self._burstSelectionMethod)
        box14.addWidget(self._label6)
        box15 = QHBoxLayout()
        box15.addWidget(self._burstSelectionParams)
        box15.addWidget(self._burstSelectionParamValues)
        box16 = QHBoxLayout()
        box16.addWidget(self._label7)
        box16.addWidget(self._checkSelectionParams)
        box17 = QVBoxLayout()
        box17.addLayout(box14)
        box17.addLayout(box15)
        box17.addLayout(box16)
        group7 = QGroupBox("Burst selection")
        group7.setLayout(box17)

        box18 = QHBoxLayout()
        box18.addWidget(self._exportBurstDataParams)
        box18.addWidget(self._exportBurstDataParamValues)
        box19 = QVBoxLayout()
        box19.addLayout(box18)
        box19.addWidget(self._ExportSelectionButton)
        group8 = QGroupBox("Export data")
        group8.setLayout(box19)

        box20 = QHBoxLayout()
        box20.addWidget(self._plotFretHistEParam)
        box20.addWidget(self._plotFretHistEParamValues)
        box20.addWidget(self._plotFretHistEButton)
        box23 = QHBoxLayout()
        box23.addWidget(self._plotFretHist2DParam)
        box23.addWidget(self._plotFretHist2DParamValues)
        box23.addWidget(self._plotFretHist2DButton)
        box25 = QHBoxLayout()
        box25.addWidget(self._plotFretHistAJPParam)
        box25.addWidget(self._plotFretHistAJPParamValues)
        box25.addWidget(self._plotFretHistAJPButton)
        box24 = QVBoxLayout()
        box24.addLayout(box20)
        box24.addLayout(box23)
        box24.addLayout(box25)
        group9 = QGroupBox("Fret histogram")
        group9.setLayout(box24)

        grid = QGridLayout()
        grid.addWidget(group1, 0, 0, 2, 2)
        grid.addWidget(group2, 2, 0, 2, 2)
        grid.addWidget(group3, 4, 0, 2, 2)
        grid.addWidget(group4, 0, 2, 2, 2)
        grid.addWidget(group5, 2, 2, 2, 2)
        grid.addWidget(self._printWindow, 6, 0, 4, 6)
        grid.addWidget(group6, 4, 2, 2, 2)
        grid.addWidget(group7, 0, 4, 2, 2)
        grid.addWidget(group9, 2, 4, 2, 2)
        grid.addWidget(group8, 4, 4, 2, 2)
        self._centralBox.setLayout(grid)

    def on_EmittingStream_message(self, message):
        # self._printWindow.clear()
        self._printWindow.moveCursor(QTextCursor.End)
        self._printWindow.insertPlainText(message)

    def openFileNameDialog(self):
        print(self._info._loaderInfo)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self._fileName, _ = QFileDialog.getOpenFileName(self, "Select file", "",
                                                        "photon-HDF5 files (*.hdf5);; Text files (*.txt)",
                                                        options=options)
        if self._fileName:
            self._showFile.setText(self._fileName)
            self.statusBar.showMessage('Selected file is valid')
            self._burstAnalysis.LoadFile(self._fileName)

    def CorrectionFactors(self, text):
        self._correctionValues.setText("")
        print(self._info._correctionInfo[text])
        self._corrFactName = text
        self._correctionValues.setPlaceholderText(str(self._burstAnalysis._correctionF[text]))

    def CorrectionValues(self, text):
        if text:
            self._burstAnalysis._correctionF[self._corrFactName] = str(text)
            self._burstAnalysis.writeCorrF()

    def ALEXparam(self, text):
        self._ALEXValues.setText("")
        print(self._info._ALEXinfo[text])
        self._ALEXName = text
        self._ALEXValues.setPlaceholderText(str(self._burstAnalysis._ALEXparam[text]))

    def ALEXValues(self, text):
        if text:
            self._burstAnalysis._ALEXparam[self._ALEXName] = str(text)

    def TimetraceParams(self, text):
        self._timetraceParamValues.setText("")
        print(self._info._timetraceInfo[text])
        self._timetraceParamName = text
        self._timetraceParamValues.setPlaceholderText(str(self._burstAnalysis._timetraceParams[text]))

    def TimetraceParamValues(self, text):
        if text:
            self._burstAnalysis._timetraceParams[self._timetraceParamName] = str(text)

    def BackgroundParams(self, text):
        self._backgroundParamValues.setText("")
        print(self._info._calcBGinfo[text])
        self._backgroundParamName = text
        self._backgroundParamValues.setPlaceholderText(str(self._burstAnalysis._backgroundParam[text]))

    def BackgroundParamValues(self, text):
        if text:
            self._burstAnalysis._backgroundParam[self._backgroundParamName] = text

    def BgHistParams(self, text):
        self._bgHistParamValues.setText("")
        print(self._info._bgHistInfo[text])
        self._bgHistParamName = text
        self._bgHistParamValues.setPlaceholderText(str(self._burstAnalysis._bgHistParam[text]))

    def BgHistParamValues(self, text):
        if text:
            self._burstAnalysis._bgHistParam[self._bgHistParamName] = text

    def BgTimetraceParams(self, text):
        self._bgTimetraceParamValues.setText("")
        print(self._info._bgTimetraceInfo[text])
        self._bgTimetraceParamName = text
        self._bgTimetraceParamValues.setPlaceholderText(str(self._burstAnalysis._bgTimetraceParam[text]))

    def BgTimetraceParamValues(self, text):
        if text:
            self._burstAnalysis._bgTimetraceParam[self._bgTimetraceParamName] = text

    def BurstSearchParams(self, text):
        self._burstSearchParamValues.setText("")
        print(self._info._burstSearchInfo[text])
        self._burstSearchParamName = text
        self._burstSearchParamValues.setPlaceholderText(str(self._burstAnalysis._burstSearchParams[text]))

    def BurstSearchParamValues(self, text):
        if text:
            self._burstAnalysis._burstSearchParams[self._burstSearchParamName] = text

    def PlotFretHistEParams(self, text):
        self._plotFretHistEParamValues.setText("")
        print(self._info._plotFretHistEInfo[text])
        self._plotFretHistEParamName = text
        self._plotFretHistEParamValues.setPlaceholderText(str(self._burstAnalysis._plotFretHistEParam[text]))

    def PlotFretHistEParamValues(self, text):
        if text:
            self._burstAnalysis._plotFretHistEParam[self._plotFretHistEParamName] = text

    def PlotFretHist2DParams(self, text):
        self._plotFretHist2DParamValues.setText("")
        print(self._info._plotFretHist2DInfo[text])
        self._plotFretHist2DParamName = text
        self._plotFretHist2DParamValues.setPlaceholderText(str(self._burstAnalysis._plotFretHist2DParams[text]))

    def PlotFretHist2DParamValues(self, text):
        if text:
            self._burstAnalysis._plotFretHist2DParams[self._plotFretHist2DParamName] = text

    def PlotFretHistAJPParams(self, text):
        self._plotFretHistAJPParamValues.setText("")
        print(self._info._plotFretHistAJPInfo[text])
        self._plotFretHistAJPParamName = text
        self._plotFretHistAJPParamValues.setPlaceholderText(str(self._burstAnalysis._plotFretHistAJPParams[text]))

    def PlotFretHistAJPParamValues(self, text):
        if text:
            self._burstAnalysis._plotFretHistAJPParams[self._plotFretHistAJPParamName] = text

    def BurstSelectionMethod(self, text):
        self._burstSelectionMethodName = text
        print(self._info._burstSelectionMethodInfo[text])
        self._burstSelectionParams.clear()
        self._burstSelectionParamList = (["negate", "computefret"] + self._paramList[text])
        self._burstSelectionParams.addItems(self._burstSelectionParamList)

    def BurstSelectionParams(self, text):
        self._burstSelectionParamValues.setText("")
        print(self._info._burstSelectionParamInfo[text])
        self._burstSelectionParamName = text
        self._burstSelectionParamValues.setPlaceholderText(str(self._burstAnalysis._burstSelectionParam[text]))

    def BurstSelectionParamValue(self, text):
        if text:
            self._burstAnalysis._burstSelectionParam[self._burstSelectionParamName] = text

    def BurstSelectionParameters(self):
        parameter = []
        for key in self._burstSelectionParamList[2:]:
            parameter.append(self._burstAnalysis._burstSelectionParam[key])
        self._burstAnalysis.burstSelection(self._burstSelectionMethodName, parameter)

    def ExportBurstDataParam(self, text):
        self._exportBurstDataParamValues.setText("")
        print(self._info._exportBurstDataInfo[text])
        self._exportBurstDataParamName = text
        self._exportBurstDataParamValues.setPlaceholderText(str(self._burstAnalysis._exportBurstParam[text]))

    def ExportBurstDataParamValues(self, text):
        if text:
            self._burstAnalysis._exportBurstParam[self._exportBurstDataParamName] = text

    def ComboBox(self, key, text):
        self._param = getattr(self, '_' + key + 'ParamValues')
        self._param.setText("")
        self._infoParam = getattr(self, '_' + key + 'Info')
        print(self._infoParam[text])
        self._name = getattr(self, '_' + key + 'ParamName')
        self._name = text
        self._value = getattr(self._burstAnalysis, '_' + key + 'Param')
        self._param.setPlaceholderText(str(self._value[text]))

    def LineEdit(self, text):
        if text:
            self._value[self._name] = text

    def underConstruction(self):
        print('under Construction')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Do you want to quit? All unsaved data will be lost.", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._burstAnalysis.exitEvent()
            event.accept()
        else:
            event.ignore()