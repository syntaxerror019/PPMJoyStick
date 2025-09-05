import numpy as np
from scipy.signal import butter, cheby1, lfilter, medfilt, savgol_filter

FILTER_TYPE = 0
FILTER_ORDER = 4
CUTOFF = 0.1 

#TODO: Implement better filtering options and abilities.

def apply_filter(data, ftype=FILTER_TYPE):
    if ftype == 0:  # No filtering
        return data

    elif ftype == 1:
        N = 5  # window size
        kernel = np.ones(N) / N
        return np.convolve(data, kernel, mode="same")

    elif ftype == 2:
        return medfilt(data, kernel_size=5)

    elif ftype == 3:
        b, a = butter(FILTER_ORDER, CUTOFF, btype='low')
        return lfilter(b, a, data)

    elif ftype == 4:
        b, a = cheby1(FILTER_ORDER, 0.5, CUTOFF, btype='low')
        return lfilter(b, a, data)

    elif ftype == 5:
        return savgol_filter(data, window_length=11, polyorder=3)

    else:
        return data