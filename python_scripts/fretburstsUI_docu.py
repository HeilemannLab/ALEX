'''######################################################################
# File Name: fretburstsUI_docu
# Project:
# Version:
# Creation Date:
# Created By:
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''


class FretburstsUIinfo():
    def __init__(self):
        self._one = 1
        self._initialInfo = "Choose a file first. Then follow the steps downwards. Don't forget to check the 'Apply parameters?' checkbox."

        self._loaderInfo = "Load a data file saved in Photon-HDF5 format version 0.3 or higher. Photon-HDF5 is a format for a wide range of timestamp-based single molecule data. For more info please see: http://photon-hdf5.org/"

        self._corrFInfo = {"Gamma": "Gamma >>> Gamma correction factor (compensates DexDem and DexAem unbalance).",
                                "Direct excitation": "Direct excitation >>> Direct excitation correction factor.",
                                "Leakage": "Leakage >>> Spectral leakage (bleed-through) of Donor emission in the Acceptor channel."}

        self._ALEXinfo = {"ALEX period": "ALEX period >>> Duration of the alternation period in timestamp units. Put in an integer.",
                          "Donor period start": "Donor period start >>> Start of the donor excitation period in timestamps units. Put in an integer.",
                          "Donor period end": "Donor period end >>> End of the donor excitation period in timestamp units. Put in an integer.",
                          "Acceptor period start": "Acceptor period start >>> Start of the acceptor excitation period in timestamp units. Put in an integer.",
                          "Acceptor period end": "Acceptor period end >>> End of the acceptor excitation period in timestamp units. Put in an integer.",
                          "Offset": "Offset >>> Time between alterantion start and start of timestamping. Put in an integer."}

        self._ALEXhistInfo = "Info >>> If you're satisfied with the alternation histogram, click the 'Apply parameters?' checkbox, before you continue with the analysis. This is a crucial step!"

        self._timetraceInfo = {"Binwidth": "Binwidth >>> The bin width (seconds) of the timetrace histogram. Default is 0.001",
                               "T_min": "T min >>> Min and max time (seconds) to include in the timetrace. Note that a long time range and a small binwidth can require a significant amount of memory. Default is 0.",
                               "T_max": "T max >>> Min and max time (seconds) to include in the timetrace. Note that a long time range and a small binwidth can require a significant amount of memory. Default is 200",
                               "Show AexAem": "Show AexAem >>> True/False. If True (default), plot a timetrace for the AexAem photons. If False, plot timetraces only for DexDem and DexAem streams.",
                               "Legend": "Legend >>> True/False. Whether to show the legend or not. Default is False"}

        self._calcBGinfo = {"Min tail": "Min tail >>> Min threshold in us for photon waiting times to use in background estimation. If float is the same threshold for 'all', DD, AD and AA photons and for all the channels. If a 3 or 4 element tuple, each value is used for 'all', DD, AD or AA photons, same value for all the channels. If 'auto', the threshold is computed for each stream ('all', DD, DA, AA) and for each channel as bg_F * rate_ml0. rate_ml0 is an initial estimation of the rate performed using bg.exp_fit() and a fixed threshold (default 250us).",
                            "Time": "Time >>> Compute background each time seconds. Default is 60.",
                            "F": "F >>> It's the factor by which the initial background estimation if multiplied to compute the threshold. Default is 2.",
                            "Error metrics": "Error metrics >>> Specifies the error metric to use. Valid values are 'KS' or 'CM'. 'KS' (Kolmogorov-Smirnov statistics) computes the error as the max of deviation of the empirical CDF from the fitted CDF. 'CM' (Crames-von Mises) uses the L^2 distance. If None, no error metric is computed (returns None). Default is None.",
                            "Fit all photons": "Fit all photons >>> True/False. If True (default) the background for the all-photon is fitted. If False it is computed as the sum of backgrounds in all the other streams."}

        self._bgHistInfo = {"Binwidth": "Binwidth >>> Histogram bin width in seconds. Default is 0.0001",
                            "Period": "Period >>> The background period to use for plotting the histogram. The background period is a time-slice of the measurement from which timestamps are taken. If period is None (default) the time-windows is the full measurement.",
                            "Y scale": "Y scale >>> Scale for the y-axis. Valid values include 'log' and 'linear'. Default 'log'.",
                            "X scale": "X scale >>> Scale for the x-axis. Valid values include 'log' and 'linear'. Default 'linear'.",
                            "X unit": "Xunit >>> Unit used for the x-axis. Valid values are 's', 'ms', 'us', 'ns'. Default 'ms'.",
                            "Show da": "Show da >>> True/False. If False (default) do not plot the AexDem photon stream. Ignored when the measurement is not ALEX.",
                            "Legend": "Legend >>> True/False. If True (default) plot a legend.",
                            "Show fit": "Show fit >>> True/False. If True shows the fitted background rate as an exponential distribution."}

        self._bgTimetraceInfo = {"No legend": "No legend >>> True/False. Default False.",
                                 "Plot style": "Plot style >>> Default is {}.",
                                 "Show da": "Show da >>> True/False. Default False."}

        self._burstSearchInfo = {"L": "L >>> Minimum number of photons in burst. If None (default) L = m is used.",
                                 "m": "m >>> Number of consecutive photons used to compute the photon rate. Typical values 5-20. Default 10.",
                                 "F": "F >>> Defines how many times higher than the background rate is the minimum rate used for burst search ('min rate = F * bg. rate'), assuming that 'P = None' (default). Typical values are 3-9. Default 6.",
                                 "Dex photon selection": "Dex photon selection >>> Defines the 'photon selection' (or stream) to be used for Dex burst search. Default: DAem (all photons). Not specifying a keyword argument is equivalent to setting it to None. \nExamples:\n - 'Ph_sel(Dex='DAem', Aex='DAem')' selects all photons (ACBS).\n - 'Ph_sel(Dex='DAem')' selects only donor and acceptor photons emitted during donor excitation. These are all the photons for non-ALEX data.\n - 'Ph_sel(Dex='Aem', Aex='Aem')' selects all the photons detected from the acceptor-emission channel.\n - 'Ph_sel(Dex='DAem', Dex='Aem')' selects all photons detected from A+D em channel(Dex) AND Aem channel(Aex), (DCBS).",
                                 "Aex photon selection": "Photon selection >>> Defines the 'photon selection' (or stream) to be used for Aex burst search. Default: DAem. Not specifying a keyword argument is equivalent to setting it to None. \nExamples:\n - 'Ph_sel(Dex='DAem', Aex='DAem')' selects all photons (ACBS).\n - 'Ph_sel(Dex='DAem')' selects only donor and acceptor photons emitted during donor excitation. These are all the photons for non-ALEX data.\n - 'Ph_sel(Dex='Aem', Aex='Aem')' selects all the photons detected from the acceptor-emission channel.\n - 'Ph_sel(Dex='DAem', Dex='Aem')' selects all photons detected from A+D em channel(Dex) AND Aem channel(Aex), (DCBS).",
                                 "Max rate": "Max rate >>> True/False. If True compute the max photon rate inside each burst using the same `m` used for burst search. If False (default) skip this step.",
                                 "Dither": "Dither >>> True/False. If True applies dithering corrections to burst counts. Default False. Add dithering (uniform random noise) to burst counts (nd, na,...). The dithering amplitude is the range -0.5*lsb .. 0.5*lsb.."}

        self._plotFretHistEInfo = {"Data": "Data >>> Select the raw burst search data with 'd' (default), or if you did a burst selection, type 'ds'.",
                                   "Binwidth": "Binwidth >>> Bin width for the histogram. Default is 0.03",
                                   "Hist style": "Hist style >>> If 'bar' (default) use a classical bar histogram, otherwise do a normal line plot of bin counts vs bin centers",
                                   "Weights": "Weights >>> Kind of burst-size weights. Possible weights are: 'size' burst size, 'size_min' burst size - min(burst size), 'size2' (burst size)^2, 'sqrt' sqrt(burst size), 'inv_size' 1/(burst size), 'inv_sqrt' 1/sqrt(burst size), 'cum_size' CDF_of_burst_sizes(burst size), 'cum_size2' CDF_of_burst_sizes(burst size)^2, 'brightness' the burst size divided by the burst width. If None returns uniform weights..",
                                   "Add naa": "Add naa >>> True/False. If True adds 'naa' to the burst size. Default is False",
                                   "Fit from": "Fit from >>> Determines how to obtain the fit value. If 'kde'(default) the fit value is the KDE peak. Otherwise it must be the name of a model parameter that will be used as fit value.",
                                   "Show KDE": "Show KDE >>> True/False. If True shows the KDE curve. Default is False.",
                                   "Bandwidth": "Bandwidth >>> Bandwidth used to compute the KDE. If None the KDE is not computed. Default is 0.03."}

        self._burstSelectionMethodInfo = {"E": "E >>> Select bursts with E between E1 and E2.",
                                          "ES": "ES >>> Select bursts with E between E1 and E2 and S between S1 and S2. When rect is True the selection is rectangular otherwise is elliptical.",
                                          "ES_ellips": "ES_ellips >>> Select bursts with E-S inside an ellipsis inscribed in E1, E2, S1, S2.",
                                          "ES_rect": "ES_rect >>> Select bursts inside the rectangle defined by E1, E2, S1, S2.",
                                          "brightness": "brightness >>> Select bursts with size/width between th1 and th2 (cps).",
                                          "consecutive": "consecutive >>> Select consecutive bursts with th1 <= separation <= th2 (in sec.).",
                                          "na": "na >>> Select bursts with (na >= th1) and (na <= th2).",
                                          "na_bg": "na_bg >>> Select bursts with (na >= bg_ad*F).",
                                          "na_bg_p": "na_bg_p >>> Select bursts w/ AD signal using P{F*BG>=na} < P.",
                                          "naa": "naa >>> Select bursts with (naa >= th1) and (naa <= th2). The naa quantity can be optionally corrected using gamma and beta factors.",
                                          "naa_bg": "naa_bg >>> Select bursts with (naa >= bg_aa*F).",
                                          "naa_bg_p": "naa_bg_p >>> Select bursts w/ AA signal using P{F*BG>=naa} < P.",
                                          "nd": "nd >>> Select bursts with (nd >= th1) and (nd <= th2).",
                                          "nd_bg": "nd_bg >>> Select bursts with (nd >= bg_dd*F).",
                                          "nd_bg_p": "nd_bg_p >>> Select bursts w/ DD signal using P{F*BG>=nd} < P.",
                                          "nda_percentile": "nda_percentile >>> Select bursts with SIZE >= q-percentile (or <= if low is True) gamma and add_naa are passed to fretbursts.burstlib.Data.burst_sizes_ich() to compute the burst size.",
                                          "nt_bg": "nt_bg >>> Select bursts with (nt >= bg*F).",
                                          "nt_bg_p": "nt_bg_p >>> Select bursts w/ signal using P{F*BG>=nt} < P.",
                                          "peak_phrate": "peak_phrate >>>  Select bursts with peak phtotons rate between th1 and th2 (cps). Note that this function requires to compute the peak photon rate first using fretbursts.burstlib.Data.calc_max_rate().",
                                          "period": "period >>> Select bursts from period bp1 to period bp2 (included).",
                                          "sbr": "sbr >>> Select bursts with SBR between th1 and th2.",
                                          "single": "single >>> Select bursts that are at least th millisec apart from the others.",
                                          "size": "size >>> Select bursts with burst sizes (i.e. counts) between th1 and th2. The burst size is the number of photon in a burst. By default it includes all photons during donor excitation (Dex). To add AexAem photons to the burst size use add_naa=True.",
                                          "str_G": "str_G >>> A string indicating gamma value and convention for burst size correction.",
                                          "time": "time >>> Select the burst starting from time_s1 to time_s2 (in seconds).",
                                          "topN_max_rate": "topN_max_rate >>> Select N bursts with the highest max burst rate.",
                                          "topN_nda": "topN_nda >>> Select the N biggest bursts in the channel. Gamma and add_naa are passed to fretbursts.burstlib.Data.burst_sizes_ich() to compute the burst size.",
                                          "topN_sbr": "topN_sbr >>> Select the top N bursts with hightest SBR.",
                                          "width": "width >>> Select bursts with (width >= th1) and (width <= th2), in ms."}
        self._burstSelectionParamInfo = {"th1": "th1 >>> Select bursts with th1 <= size <= th2. Default th2 = inf (i.e. no upper limit).",
                                         "th2": "th2 >>> Select bursts with th1 <= size <= th2. Default th2 = inf (i.e. no upper limit).",
                                         "add_naa": "add_naa >>> True/False. When True, add AexAem photons when computing burst burst size. Default False.",
                                         "gamma": "gamma >>> Arguments used to compute gamma- and beta-corrected burst sizes. Coefficient for gamma correction of burst sizes. Default: 1. If donor_ref == True (default) the gamma corrected burst size is computed according to: 1) nd + na / gamma. Otherwise, if donor_ref == False, the gamma corrected burst size is: 2) nd * gamma  + na. With the definition (1) the corrected burst size is equal to the raw burst size for zero-FRET or D-only bursts (that's why is donor_ref). With the definition (2) the corrected burst size is equal to the raw burst size for 100%-FRET bursts. In an ALEX measurement, use add_naa = True to add counts from AexAem stream to the returned burst size. The argument gamma and beta are used to correctly scale naa so that it become commensurate with the Dex corrected burst size. In particular, when using definition (1) (i.e. donor_ref = True), the total burst size is: (nd + na/gamma) + naa / (beta * gamma). Conversely, when using definition (2) (donor_ref = False), the total burst size is: (nd * gamma + na) + naa / beta.",
                                         "beta": "beta >>> Arguments used to compute gamma- and beta-corrected burst sizes. If donor_ref == True (default) the gamma corrected burst size is computed according to: 1) nd + na / gamma. Otherwise, if donor_ref == False, the gamma corrected burst size is: 2) nd * gamma  + na. With the definition (1) the corrected burst size is equal to the raw burst size for zero-FRET or D-only bursts (that's why is donor_ref). With the definition (2) the corrected burst size is equal to the raw burst size for 100%-FRET bursts. In an ALEX measurement, use add_naa = True to add counts from AexAem stream to the returned burst size. The argument gamma and beta are used to correctly scale naa so that it become commensurate with the Dex corrected burst size. In particular, when using definition (1) (i.e. donor_ref = True), the total burst size is: (nd + na/gamma) + naa / (beta * gamma). Conversely, when using definition (2) (donor_ref = False), the total burst size is: (nd * gamma + na) + naa / beta.",
                                         "donor_ref": "donor_ref >>> Select the convention for naa correction. If donor_ref == True (default) the gamma corrected burst size is computed according to: 1) nd + na / gamma. Otherwise, if donor_ref == False, the gamma corrected burst size is: 2) nd * gamma  + na. With the definition (1) the corrected burst size is equal to the raw burst size for zero-FRET or D-only bursts (that's why is donor_ref). With the definition (2) the corrected burst size is equal to the raw burst size for 100%-FRET bursts. In an ALEX measurement, use add_naa = True to add counts from AexAem stream to the returned burst size. The argument gamma and beta are used to correctly scale naa so that it become commensurate with the Dex corrected burst size. In particular, when using definition (1) (i.e. donor_ref = True), the total burst size is: (nd + na/gamma) + naa / (beta * gamma). Conversely, when using definition (2) (donor_ref = False), the total burst size is: (nd * gamma + na) + naa / beta.",
                                         "add_aex": "add_aex >>> PAX-only. Whether to add signal from Aex laser period to the burst size. Default True. When True, burst size include add photons detected during the Aex.",
                                         "A_laser_weight": "A_laser_weight >>> PAX-only. Weight of A-ch photons during Aex period (AexAem) due to the A laser. Default 1. Weight of the fraction of AexAem photons due to A laser. Since the D laser is present in both alternation periods, you may want to use 2 in order to make counts caused by the D laser and counts caused by the A laser commensurable. Using 2 is an extension of the beta correction for PAX.",
                                         "negate": "negate >>>True/False. If True, negates (i.e. take the complementary) of the selection returned by filter_fun. Default False.",
                                         "computefret": "computefret >>> True/False. If True (default) recompute donor and acceptor counts, corrections and FRET quantities (i.e. E, S) in the new returned object.",
                                         "E1": "E1 >>> Default -inf.",
                                         "E2": "E2 >>> Default -inf.",
                                         "S1": "S1 >>> Default -inf.",
                                         "S2": "S1 >>> Default -inf.",
                                         "rect": "rect >>> True/False. When `rect` is True the selection is rectangular otherwise is elliptical.",
                                         "bp1": "Default 0",
                                         "bp2": "Default None",
                                         "time_s1": "",
                                         "time_s2": "",
                                         "q": "",
                                         "False": "",
                                         "N": "N >>> Select the N biggest bursts in the channel",
                                         "F": "",
                                         "P": ""}
        self._exportBurstDataInfo = {"Include background": "Include background >>> True/False. If True includes additional columns for burst background (see above). Default False.",
                                     "Include photon index": "Include photon index >>> True/False. If True includes additional two columns for index of first and last timestamp in each burst. Default False.",
                                     "Data": "Data >>> Select the raw burst search data with 'd' (default), or if you did a burst selection, type 'ds'."}

        self._plotFretHistAJPInfo = {"Data": "Data >>> Select the raw burst search data with 'd' (default), or if you did a burst selection, type 'ds'.",
                                     "Gridsize": "Gridsize >>> The grid size for the 2D histogram (hexbin)",
                                     "Cmap": "Cmap >>> FRETbursts defines these custom colormaps: 'alex_light' (default) and 'alex_dark'. More option: see cmap_styles.txt.",
                                     "Kind": "Kind >>> Kind of plot for the 2-D distribution. Valid values: 'hex'(default) for hexbin plots, 'kde' for kernel density estimation, 'scatter' for scatter plot.",
                                     "Vmax fret": "Vmax fret >>> True/False. If True (default), the colormap max value is equal to the max bin counts in the FRET region (S < 0.8). If False the colormap max is equal to the max bin counts.",
                                     "Histcolor id": "histcolor id >>> The colormap passes as `cmap` is divided in 12 colors. `histcolor_id` is the index of the color to be used for the marginal 1D histogram. Default 0."}

        self._plotFretHist2DInfo = {"Data": "Data >>> Select the raw burst search data with 'd' (default), or if you did a burst selection, type 'ds'.",
                                    "Vmin": "Vmin >>> Default 2.",
                                    "Vmax": "Vmax >>> Default 0.",
                                    "Binwidth": "Binwidth >>> Default 0.05.",
                                    "S max norm": "S max norm >>> Default 0.8.",
                                    "Interpolation": "Interpolation >>> Default 'bicubic'.",
                                    "Cmap": "Cmap >>> Default 'hot'. More options: see cmap_styles.txt.",
                                    "Under color": "Under color >>> Default 'white'.",
                                    "Over color": "Over color >>> Default 'white'.",
                                    "Scatter": "Scatter >>> True/False. Default True.",
                                    "Scatter ms": "Scatter ms >>> Default 3.",
                                    "Scatter color": "Scatter color >>> Default 'orange'.",
                                    "Scatter alpha": "Scatter alpha >>> Default 0.2.",
                                    "Gui sel": "Gui sel >>> True/False. Default False.",
                                    "Cbar ax": "Cbar ax >>> Default None.",
                                    "Grid color": "Grid color >>> Default '#D0D0D0'."}