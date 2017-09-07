'''######################################################################
# File Name: niconvert_test.py
# Project: ALEX
# Version:
# Creation Date: 06/09/2017
# Created By:
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from pathlib import Path
import numpy as np
import pandas as pd
import numba
import tables
from tqdm import tqdm_notebook, tqdm


def ni96ch_process_spots(fname, out_path=None, chunksize=2**18, num_timestamps=-1, debug=False,
                         close=False, comp_filter=None,
                         progrbar_widget=True):
    """Sort timestamps per-spot and correct overflow in NI-96ch data.
    This function auto-detects whether the file is saved by LabVIEW
    MultiCounterProject (so it has a 3-lines header and timestamps in
    big-endian order) or by LabVIEW FPGA_96ch project (no header, timestamps
    in little-endian order).
    Arguments:
        fname (string or pathlib.Path): name of the input data file.
        out_path (string or pathlib.Path or None): name of the ouput HDF5 file.
            If None, use same name as input file changing the extension to hdf5.
        chunksize (int): input file is read in chunks (i.e. number of 32-bit
            words) of this size.
        num_timestamps (int): read at most `num_timestamps`. If negative read
            the whole file.
        close (bool): wether to close the output pytables file
        debug (bool): perform additional consistency checks.
        inner_loop (function or None): function to use in the inner loop
            for overflow correction of each chunk of timestamp.
        comp_filter (tables.Filters): compression filter for the pytables file.
        progrbar_widget (bool): If true display progress bar as a Jypyter
            notebook widget.
    Returns:
        A tuple of:
        - h5file (pytables file): the handle for the pytables file
        - meta (dict): metadata extracted from the file"""

    if out_path is None:
        outpath = 'Datafile.hdf5'
        # out_path = fname.with_suffix('.hdf5')   # This is great!
    out_path = Path(out_path)

    # Open files
    f1 = tables.open_file('tempAPD1.hdf', 'r')
    num_ts_f1 = f1.root.timestamps.nrows
    f2 = tables.open_file('TempAPD2.hdf', 'r')
    num_ts_2 = f2.root.timestamps.nrows
    f_list = [f1, f2]

    # Output file, hier werden leere arrays erstellt
    if comp_filter is None:
        comp_filter = tables.Filters(complevel=6, complib='zlib')
    h5file = tables.open_file(str(out_path), mode="w", filters=comp_filter)
    h5file.create_earray('/photon_data', 'timestamps',
                         createparents=True, chunkshape=(chunksize,),
                         obj=np.array([], dtype=np.int64))
    h5file.create_earray('/photon_data', 'detectors',
                         chunkshape=(chunksize,),
                         obj=np.array([], dtype=np.uint8))

    # List of empty timestamps arrays in HDF5 file
    timestamps_final, detectors_final = get_photon_data_arr(h5file)

    # Separate channels and correct overflow
    # iter() creates an iterator, progressbar is just a widget but it gets fed with
    # iter_chunksize() method. this one returns a generator (because it contains yield).
    # Conclusing the '_iter' instance is a iterator which iterates over generators.
    progressbar = tqdm_notebook if progrbar_widget else tqdm
    _iter = iter(progressbar(iter_chunksize(num_timestamps, chunksize),
                             total=np.ceil(num_timestamps / chunksize)))

    j = 0
    timestamps = _read_chunk(f, next(_iter), j)         # warum kommt read_chunk 2x vor
    prev_ts_chunks = _inner_loop_spots(timestamps)      # genauso _inner_loop_spots, rand?
    j = 1
    ts_idx = chunksize
    for chunksize in _iter:
        timestamps = _read_chunk(f, chunksize, j)
        ts_idx += chunksize
        ts_chunks = _inner_loop_spots(timestamps)
        last_ts_chunks, last_det_chunks = [], []
        for i, (ts, det) in enumerate(zip(timestamps_m, detectors_m)):
            last_two_ts_chunks = [prev_ts_chunks[i], ts_chunks[i]]
            last_two_det_chunks = [prev_det_chunks[i], det_chunks[i]]
            _fix_order(i, last_two_ts_chunks, last_two_det_chunks)
            ts.append(last_two_ts_chunks[0])
            det.append(last_two_det_chunks[0])
            prev_ts_chunks[i] = last_two_ts_chunks[1]
            prev_det_chunks[i] = last_two_det_chunks[1]
            last_ts_chunks.append(last_two_ts_chunks[1])
            last_det_chunks.append(last_two_det_chunks[1])
            if debug:
                assert (np.diff(ts_chunks[i]) > 0).all()

    # Save the last chunk for each spot
    for i, (ts, det) in enumerate(zip(timestamps_m, detectors_m)):
        ts.append(last_ts_chunks[i])
        det.append(last_det_chunks[i])

    """
    # Compute acquisition duration
    meta['acquisition_duration'] = duration(timestamps_m, ts_unit)
    h5file.flush()
    if close:
        h5file.close()
    """
    return h5file


def get_photon_data_arr(h5file):
    """Return two lists with timestamps and detectors arrays from `h5file`.
    """
    ts = h5file.get_node('/photon_data/timestamps')
    det = h5file.get_node('/photon_data/detectors')   # why is it called A_em
    return ts, det


def iter_chunksize(num_samples, chunksize):
    """Yield `chunksize` enough times to cover `num_samples`.
    """
    for i in range(int(np.ceil(num_samples / chunksize))):
        yield chunksize


def _read_chunk(f, chunksize, i):
    start = i * chunksize
    end = start + chunksize
    timestamps = f.root.timestamps[start:end, 0]
    return timestamps


def _inner_loop_spots(timestamps):
    """Apply overflow correction and create per-spot timestamps/detectors."""
    new_ts = _overflow_correct(timestamps)
    # tm, mask_tm = merge_timestamps(t1, t2)   # macht das sinn?
    return ts_list   # , det_list


def get_spot_ch_map_48spots():
    # A-ch are [0..47] and assumed to be the spot number
    # D-ch are [48..95], the mapping from D-ch to spot number is below in D_ch
    A_ch = np.arange(48)
    D_ch = np.arange(48).reshape(4, 12)[::-1].reshape(48) + 48
    return D_ch, A_ch


def _fix_order(ispot, two_ts_chunks, two_det_chunks):
    """Fix non-sorted timestamps in consecutive chunks of per-spot data.
    Each timestamp-chunk is monotonic but their concatenation may be
    non-monotonic. In the latter case, this function modifies in-place
    the input lists to fix the timestamps (and detectors) order.
    """
    assert len(two_ts_chunks) == 2
    for i in (0, 1):
        assert len(two_ts_chunks[i]) == len(two_det_chunks[i])
    # Check cross-chunk monotonicity
    if two_ts_chunks[1][0] < two_ts_chunks[0][-1]:
        ts_merged = np.hstack(two_ts_chunks)
        det_merged = np.hstack(two_det_chunks)
        sorted_index = ts_merged.argsort(kind='mergesort')
        ts_merged = ts_merged[sorted_index]
        det_merged = det_merged[sorted_index]
        size0 = len(two_ts_chunks[0])
        two_ts_chunks[:] = [ts_merged[:size0], ts_merged[size0:]]
        two_det_chunks[:] = [det_merged[:size0], det_merged[size0:]]


@numba.jit('int64[:](int64[:])', nopython=True, nogil=True)
def _overflow_correct(timestamps):
    """Apply overflow correction to all channels."""
    for i in range(timestamps.size):
        timestamps[i, 0] += (2**32 * timestamps[i, 1])
    return timestamps


def merge_timestamps(t1, t2):
    tm = np.hstack([t1, t2])
    index_sort = tm.argsort(kind='mergesort')  # stable sorting
    tm = tm[index_sort]
    mask_t2 = np.hstack([np.zeros(t1.size, dtype=bool),
                         np.ones(t2.size, dtype=bool)])[index_sort]
    return tm, mask_t2
