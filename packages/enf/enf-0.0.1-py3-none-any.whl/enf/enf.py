import wave
import os
import csv
import pathlib

import requests
import numpy as np
import pandas as pd

from scipy import signal

def load_wav(fpath):
    """Loads a .wav file and returns the data and sample rate.
    :param fpath: the path to load the file from
    :returns: a tuple of (wav file data as a list of amplitudes, sample rate)
    """
    with wave.open(fpath) as wav_f:
        wav_buf = wav_f.readframes(wav_f.getnframes())
        data = np.frombuffer(wav_buf, dtype=np.int16)
        fs = wav_f.getframerate()

        clip_len_s = len(data) / fs
        print(f"Loaded .wav file, n_samples={len(data)} len_s={clip_len_s}")

        return (data, fs)


def butter_bandpass_filter(data, locut, hicut, fs, order):
    """Passes input data through a Butterworth bandpass filter. Code borrowed from
    https://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html
    :param data: list of signal sample amplitudes
    :param locut: frequency (in Hz) to start the band at
    :param hicut: frequency (in Hz) to end the band at
    :param fs: the sample rate
    :param order: the filter order
    :returns: list of signal sample amplitudes after filtering
    """
    nyq = 0.5 * fs
    low = locut / nyq
    high = hicut / nyq
    sos = signal.butter(order, [low, high], analog=False, btype='band', output='sos')

    return signal.sosfilt(sos, data)


def stft(data, fs):
    """Performs a Short-time Fourier Transform (STFT) on input data.
    :param data: list of signal sample amplitudes
    :param fs: the sample rate
    :returns: tuple of (array of sample frequencies, array of segment times, STFT of input).
        This is the same return format as scipy's stft function.
    """
    window_size_seconds = 16
    nperseg = fs * window_size_seconds
    noverlap = fs * (window_size_seconds - 1)
    f, t, Zxx = signal.stft(data, fs, nperseg=nperseg, noverlap=noverlap)
    return f, t, Zxx


def enf_series(data, fs, nominal_freq, freq_band_size, harmonic_n=1):
    """Extracts a series of ENF values from `data`, one per second.
    :param data: list of signal sample amplitudes
    :param fs: the sample rate
    :param nominal_freq: the nominal ENF (in Hz) to look near
    :param freq_band_size: the size of the band around the nominal value in which to look for the ENF
    :param harmonic_n: the harmonic number to look for
    :returns: a list of ENF values, one per second
    """
    # downsampled_data, downsampled_fs = downsample(data, fs, 300)
    downsampled_data, downsampled_fs = (data, fs)

    locut = harmonic_n * (nominal_freq - freq_band_size)
    hicut = harmonic_n * (nominal_freq + freq_band_size)

    filtered_data = butter_bandpass_filter(downsampled_data, locut, hicut, downsampled_fs, order=10)

    f, t, Zxx = stft(filtered_data, downsampled_fs)

    def quadratic_interpolation(data, max_idx, bin_size):
        """
        https://ccrma.stanford.edu/~jos/sasp/Quadratic_Interpolation_Spectral_Peaks.html
        """
        left = data[max_idx-1]
        center = data[max_idx]
        right = data[max_idx+1]

        p = 0.5 * (left - right) / (left - 2*center + right)
        interpolated = (max_idx + p) * bin_size

        return interpolated

    bin_size = f[1] - f[0]

    max_freqs = []
    for spectrum in np.abs(np.transpose(Zxx)):
        max_amp = np.amax(spectrum)
        max_freq_idx = np.where(spectrum == max_amp)[0][0]

        max_freq = quadratic_interpolation(spectrum, max_freq_idx, bin_size)
        max_freqs.append(max_freq)

    return {
        'downsample': {
            'new_fs': downsampled_fs,
        },
        'filter': {
            'locut': locut,
            'hicut': hicut,
        },
        'stft': {
            'f': f,
            't': t,
            'Zxx': Zxx,
        },
        'enf': [f/float(harmonic_n) for f in max_freqs],
    }


def pmcc(x, y):
    """Calculates the PMCC between x and y data points.
    :param x: list of x values
    :param y: list of y values, same length as x
    :returns: PMCC of x and y, as a float
    """
    return np.corrcoef(x, y)[0][1]


def sorted_pmccs(target, references):
    """Calculates and sorts PMCCs between `target` and each of `references`.
    :param target: list of target data points
    :param references: list of lists of reference data points
    :returns: list of tuples of (reference index, PMCC), sorted desc by PMCC
    """
    pmccs = [pmcc(target, r) for r in references]
    sorted_pmccs = [(idx, v) for idx, v in sorted(enumerate(pmccs), key=lambda item: -item[1])]

    return sorted_pmccs


def search(target_enf, reference_enf):
    """Calculates PMCCs between `target_enf` and each window in `reference_enf`.
    :param target_enf: list of target's ENF values
    :param reference_enf: list of reference's ENF values
    :returns: list of tuples of (reference index, PMCC), sorted desc by PMCC
    """
    n_steps = len(reference_enf) - len(target_enf)
    reference_enfs = (reference_enf[step:step+len(target_enf)] for step in range(n_steps))

    coeffs = sorted_pmccs(target_enf, reference_enfs)
    return coeffs


def gb_reference_data(year, month, day=None):
    """Fetches reference ENF data from Great Britain for the given date. Caches responses locally.
    Not used by the example, but included for reference.
    :param year:
    :param month:
    :param day: the day to filter down to. If not provided then entire month is returned
    :returns: list of ENF values
    """
    cache_dir = "./cache/gb"
    pathlib.Path(cache_dir).mkdir(parents=True, exist_ok=True)

    cache_fpath = os.path.join(cache_dir, f"./{year}-{month}.csv")

    if not os.path.exists(cache_fpath):
        ret = requests.get("https://data.nationalgrideso.com/system/system-frequency-data/datapackage.json")
        ret.raise_for_status()

        ret_data = ret.json()
        csv_resource = next(r for r in ret_data['result']['resources'] if f"{year}-{month}" in r['path'])

        ret = requests.get(csv_resource['path'])
        ret.raise_for_status()
        if ".zip" in csv_resource['path']:
            output = os.path.join(cache_dir, "./downloadedfile.zip")
            with open(output, 'wb') as f:
                f.write(ret.content)
            df = pd.read_csv(output)
            df.to_csv(cache_fpath, index=False) 
        else:
            with open(cache_fpath, 'w') as f:
                f.write(ret.text)

    with open(cache_fpath) as f:
        reader = csv.DictReader(f)

        month_data = [(l['dtm'], float(l['f'])) for l in reader]

    if day:
        formatted_date = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
        return [l for l in month_data if l[0].startswith(formatted_date)]
    else:
        return month_data

def match(presumed_year, presumed_month, path_to_wav):
    nominal_freq = 50
    freq_band_size = 0.2

    ref_data = gb_reference_data(year=presumed_year, month=presumed_month, day=None)
    ref_enf = [tup[1] for tup in ref_data]

    data, fs = load_wav(path_to_wav)

    harmonic_n = 1
    enf_output = enf_series(data, fs, nominal_freq, freq_band_size, harmonic_n=2)
    target_enf = enf_output['enf']

    pmccs = search(target_enf, ref_enf)
    predicted_ts = pmccs[0][0]
    print(f"Predicted timestamp: {ref_data[predicted_ts][0]}")