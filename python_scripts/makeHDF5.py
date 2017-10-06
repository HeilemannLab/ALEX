######################################################################
# File Name: makeHDF5.py
# Project:
# Version:
# Creation Date: 2017/04/11
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#######################################################################
import phconvert as phc
# import numpy as np
from datetime import datetime
phc.__version__


class makeHDF5():
    def __init__(self, dictionary, data, detectorMask, filename, frequency, duration):
        self._dict = dictionary
        self._frequency = frequency
        self._duration = duration
        self._data = data
        self._detectorMask = detectorMask
        self._filename = filename + '.hdf5'
        self.makeFile()

    def getitem(self, name):
        return self._dict[name]

    def makeFile(self):
        timestamps = self._data         # data goes here, ndarray only counts
        timestamps.sort()

        measurement_specs = dict(
            measurement_type='smFRET-usALEX',
            alex_offset=0,
            alex_period=4,
            alex_excitation_period1=[0, 1],            # Values pair (start-stop range,
                                                       # in timestamps units) identifying photons
                                                       # in the excitation period of wavelength 1
            alex_excitation_period2=[2, 3],           # Values pair (start-stop range,
                                                      # in timestamps units) identifying photons
                                                      # in the excitation period of wavelength 2
            detectors_specs={'spectral_ch1': [1],            # list of donor's detector IDs
                             'spectral_ch2': [0]}            # list of acceptor's detector IDs
        )

        photon_data = dict(
            timestamps=timestamps,
            measurement_specs=measurement_specs,
            detectors=self._detectorMask,     # detector array, which numbers used are specified
                                              # in measurement specs -> detectors_specs
                                              # -> spectral_ch1 and spectral_ch2
            timestamps_specs={'timestamps_unit': 12.5e-9})

        sample = dict(
            buffer_name=self.getitem("buffer_name"),
            sample_name=self.getitem("sample_name"),
            dye_names=self.getitem("dye_names"),   # Comma separates names of fluorophores
            num_dyes=self.getitem("num_dyes"),
        )

        setup = dict(
            # Mandatory fields
            num_pixels=2,                   # using 2 detectors
            num_spots=1,                    # a single confocal excitation
            num_spectral_ch=2,              # donor and acceptor detection
            num_polarization_ch=1,          # no polarization selection
            num_split_ch=1,                 # no beam splitter
            modulated_excitation=False,     # CW excitation, no modulation
            lifetime=False,                 # no TCSPC in detection

            # Optional fields
            excitation_wavelengths=[532e-9, 640e-9],            # List of excitation wavelenghts
            excitation_cw=[True],                               # List of booleans, True if wavelength is CW
            detection_wavelengths=[580e-9, 640e-9],             # Nominal center wavelength each for detection ch
        )

        provenance = dict(
            filename=' ',
            software='Python DataAquisition for usALEX-setup',
            creation_time=self.getitem("datetime"))

        identity = dict(
            author=self.getitem("author"),
            author_affiliation=self.getitem("author_affiliation"),
            creation_time=datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            filename_full=self._filename,
            # filename=os.path.split(self.filename)[1],
            format_name='Photon-HDF5')

        photon_data['measurement_specs'] = measurement_specs

        data = dict(
            acquisition_duration=self._duration,
            description=self.getitem("description"),
            photon_data=photon_data,
            setup=setup,
            identity=identity,
            provenance=provenance,
            sample=sample
        )

        phc.hdf5.save_photon_hdf5(data, h5_fname=self._filename, overwrite=True)
