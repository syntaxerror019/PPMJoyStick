####################################
# PPMJoyStick
# v1.0 2025 Miles Hilliard
# www.mileshilliard.com
# Run This File.
####################################

import numpy as np
import sounddevice as sd
import pyqtgraph as pg
from log import logger
from settings import *
from pyqtgraph.Qt import QtCore, QtWidgets
from plyer import notification
from joy import FPVJoystick
import argparse
import signal

samplerate = SAMPLE_RATE
blocksize = BLOCK_SIZE
trigger_threshold = rising_edge_trigger

upper_bound = UPPER_BOUND
lower_bound = LOWER_BOUND

PITCH = RADIO_CH_PITCH
THROTTLE = RADIO_CH_THROTTLE
YAW = RADIO_CH_YAW
ROLL = RADIO_CH_ROLL
SWA = RADIO_CH_SWA
SWB = RADIO_CH_SWB
SWC = RADIO_CH_SWC
SWD = RADIO_CH_SWD

sample_pass = 0

timer = QtCore.QTimer()
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(title="Debug signal")
plot = win.addPlot(title="PPM (Trig.)")
curve = plot.plot(pen='y')
plot.setYRange(y_plot_range[0], y_plot_range[1])
plot.setXRange(x_plot_range[0], x_plot_range[1])

parser = argparse.ArgumentParser(description="PPMJoyStick")
parser.add_argument('--debug', action='store_true', help='Enable debug outputs')
parser.add_argument('--raw', action='store_true', help='Show the raw values from radio.')
args = parser.parse_args()
DEBUG = args.debug
RAW = args.raw

joystick = FPVJoystick(device_id=1)
 
audio_data = np.zeros(blocksize)

def handle_interrupt(sig, frame):
    logger.critical("Exiting...")
    timer.stop()
    app.quit()

def audio_callback(indata, frames, time, status):
    global audio_data
    if status:
        logger.info(status)
    audio_data = indata[:, 0]

def find_trigger(data):
    """Find first rising edge after a long pause below threshold."""
    min_pause = GRACE_PERIOD
    below = trigger_threshold

    # Search for a long pause
    for i in range(min_pause, len(data)):
        # Check if the previous min_pause samples were all below 'below'
        if np.all(data[i - min_pause:i] < below):
            # Now look for a rising edge after the pause
            for j in range(i, len(data)):
                if data[j - 1] < trigger_threshold <= data[j]:
                    return j
            break  # No rising edge found after pause
    return 0  # fallback: no trigger found

def extract_values(trimmed_data):
    pulse_widths = []
    threshold = trigger_threshold

    # Find all rising and falling edges
    rising_edges = np.where((trimmed_data[:-1] < threshold) & (trimmed_data[1:] >= threshold))[0] + 1
    falling_edges = np.where((trimmed_data[:-1] >= threshold) & (trimmed_data[1:] < threshold))[0] + 1

    # Only proceed if we have at least one falling and one rising edge
    if len(falling_edges) > 0 and len(rising_edges) > 0:
        # Ensure the first edge is a falling edge after a rising edge
        if falling_edges[0] < rising_edges[0]:
            falling_edges = falling_edges[1:]
        # Pair up each falling edge with the next rising edge
        for f_edge in falling_edges:
            next_rising = rising_edges[rising_edges > f_edge]
            if len(next_rising) == 0:
                break
            r_edge = next_rising[0]
            width = r_edge - f_edge

            pulse_widths.append(width)

    return pulse_widths

def update():
    global sample_pass

    # Find trigger point
    idx = find_trigger(audio_data)

    if sample_pass > INIT_SAMPLE_PASS:
        logger.critical("No Radio input found.")
        notification.notify(
            title="PPMJoyStick",
            message="No Radio input found.",
            timeout=2  # seconds
        )
        handle_interrupt(None, None)

    if not idx:
        sample_pass += 1
        return

    # Plot a slice of the waveform starting from the trigger point
    window = audio_data[idx:idx + window_plot_range] 

    values = extract_values(window)

    _roll = values[ROLL]
    _pitch = values[PITCH]
    _yaw = values[YAW]
    _throttle = values[THROTTLE]
    _switch_a = values[SWA]
    _switch_b = values[SWB]
    _switch_c = values[SWC]
    _switch_d = values[SWD]

    roll = (_roll - lower_bound) / (upper_bound - lower_bound)
    pitch = (_pitch - lower_bound) / (upper_bound - lower_bound)
    yaw = (_yaw - lower_bound) / (upper_bound - lower_bound)
    throttle = (_throttle - lower_bound) / (upper_bound - lower_bound)
    switch_a = (_switch_a - lower_bound) / (upper_bound - lower_bound)
    switch_b = (_switch_b - lower_bound) / (upper_bound - lower_bound)
    switch_c = (_switch_c - lower_bound) / (upper_bound - lower_bound)
    switch_d = (_switch_d - lower_bound) / (upper_bound - lower_bound)

    if RAW:
        logger.debug(f"Raw val: ROLL({ROLL})={_roll}, PITCH({PITCH})={_pitch}, YAW({YAW})={_yaw}, THROTTLE({THROTTLE})={_throttle}, SWA({SWA})={_switch_a}, SWB({SWB})={_switch_b}, SWC({SWC})={_switch_c}, SWD({SWD})={_switch_d}")
        logger.debug(f"normalized: Roll={roll:.3f}, Pitch={pitch:.3f}, Yaw={yaw:.3f}, Throttle={throttle:.3f}, SwitchA={switch_a:.3f}, SwitchB={switch_b:.3f}, SwitchC={switch_c:.3f}, SwitchD={switch_d:.3f}")
        logger.debug("-" * 40)

    if DEBUG:
        curve.setData(window)

    joystick.set_axis(roll, pitch, yaw, throttle)
    joystick.set_switch(1, switch_a)
    joystick.set_switch(2, switch_b)
    joystick.set_switch(3, switch_c)
    joystick.set_switch(4, switch_d)


def main():


    stream = sd.InputStream(channels=1, samplerate=samplerate,
                            blocksize=blocksize, callback=audio_callback)
    stream.start()

    timer.timeout.connect(update)
    timer.start(10)

    signal.signal(signal.SIGINT, handle_interrupt)

    win.hide()

    if DEBUG:
        win.show()

    notification.notify(
        title="PPMJoyStick",
        message="We're live!",
        timeout=3
    )
        
    app.exec_()



if __name__ == "__main__":
    main()