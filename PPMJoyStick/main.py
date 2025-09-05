####################################
# ppmjoystick
# v1.0 2025 miles hilliard
# www.mileshilliard.com
# run this file
####################################

import os
import signal
import numpy as np
import sounddevice as sd
from pyqtgraph.Qt import QtCore
from plyer import notification

from log import logger
from adfilter import apply_filter
from config import *
from audio import find_trigger, extract_values
from plot import Plot
from joy import FPVJoystick
from args import Parse

upper = UPPER_BOUND
lower = LOWER_BOUND

PITCH, THROTTLE, YAW, ROLL = RADIO_CH_PITCH, RADIO_CH_THROTTLE, RADIO_CH_YAW, RADIO_CH_ROLL
SWA, SWB, SWC, SWD = RADIO_CH_SWA, RADIO_CH_SWB, RADIO_CH_SWC, RADIO_CH_SWD

sample_pass = 0
stream = None

args = Parse()
DEBUG = args.arguments().debug
RAW = args.arguments().raw

timer = QtCore.QTimer()
plot = Plot(x_plot_range, y_plot_range)
joystick = FPVJoystick(device_id=1)
audio_data = np.zeros(BLOCK_SIZE)

def audio_callback(indata, frames, time, status):
    global audio_data
    if status:
        logger.info(status)
    raw = indata[:, 0]
    audio_data = apply_filter(raw, FILTER_TYPE)

def handle_interrupt(sig, frame):
    logger.critical("exiting...")
    timer.stop()
    if stream:
        stream.stop()
        stream.close()
    joystick.reset()
    os._exit(0)

def update():
    global sample_pass
    idx = find_trigger(audio_data)

    if sample_pass > INIT_SAMPLE_PASS:
        logger.critical("no radio input found.")
        if not DISABLE_NOTIFICATIONS:
            notification.notify(
                title="ppmjoystick",
                message="no radio input found.",
                timeout=2
            )
        handle_interrupt(None, None)

    if not idx:
        sample_pass += 1
        return

    window = audio_data[idx:idx + window_plot_range]
    values = extract_values(window)

    _roll, _pitch, _yaw, _throttle = values[ROLL], values[PITCH], values[YAW], values[THROTTLE]
    _swa, _swb, _swc, _swd = values[SWA], values[SWB], values[SWC], values[SWD]

    norm = lambda v: (v - lower) / (upper - lower) # nomalize to 0-1 

    roll, pitch, yaw, throttle = map(norm, (_roll, _pitch, _yaw, _throttle))
    swa, swb, swc, swd = map(norm, (_swa, _swb, _swc, _swd))

    if RAW:
        logger.info(
            f"raw: roll({_roll}), pitch({_pitch}), yaw({_yaw}), throttle({_throttle}), "
            f"swa({_swa}), swb({_swb}), swc({_swc}), swd({_swd})"
        )
        logger.info(
            f"normalized: roll={roll:.3f}, pitch={pitch:.3f}, yaw={yaw:.3f}, "
            f"throttle={throttle:.3f}, swa={swa:.3f}, swb={swb:.3f}, "
            f"swc={swc:.3f}, swd={swd:.3f}"
        )
        logger.info("-" * 40)

    if DEBUG:
        plot.update(window)

    joystick.set_axis(roll, pitch, yaw, throttle)
    joystick.set_switch(1, swa)
    joystick.set_switch(2, swb)
    joystick.set_switch(3, swc)
    joystick.set_switch(4, swd)

def main():
    global stream
    stream = sd.InputStream(
        channels=1,
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        callback=audio_callback
    )
    stream.start()

    signal.signal(signal.SIGINT, handle_interrupt)

    timer.timeout.connect(update)
    timer.start(10)

    plot.hide()
    if DEBUG:
        plot.show()

    if not DISABLE_NOTIFICATIONS:
        notification.notify(
            title="ppmjoystick",
            message="we're live!",
            timeout=3
        )

    plot.run()

if __name__ == "__main__":
    main()
