from config import *
import numpy as np

def find_trigger(data):
    min_pause = GRACE_PERIOD
    below = rising_edge_trigger

    for i in range(min_pause, len(data)):
        if np.all(data[i - min_pause:i] < below):
            for j in range(i, len(data)):
                if data[j - 1] < rising_edge_trigger <= data[j]:
                    return j
            break
    return 0

def extract_values(trimmed_data):
    pulse_widths = []
    threshold = rising_edge_trigger

    rising_edges = np.where((trimmed_data[:-1] < threshold) & (trimmed_data[1:] >= threshold))[0] + 1
    falling_edges = np.where((trimmed_data[:-1] >= threshold) & (trimmed_data[1:] < threshold))[0] + 1

    if len(falling_edges) > 0 and len(rising_edges) > 0:
        if falling_edges[0] < rising_edges[0]:
            falling_edges = falling_edges[1:]
        for f_edge in falling_edges:
            next_rising = rising_edges[rising_edges > f_edge]
            if len(next_rising) == 0:
                break
            r_edge = next_rising[0]
            width = r_edge - f_edge
            pulse_widths.append(width)

    return pulse_widths
