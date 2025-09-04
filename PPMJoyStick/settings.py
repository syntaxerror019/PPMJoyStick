####################################
# PPMJoyStick
# v1.0 2025 Miles Hilliard
# www.mileshilliard.com
# Configuration File.
####################################

# Please note that defaults are tuned for the 
# FlySky FS-16X controller (TX) radio and they
# may need to be adjusted and/or fine-tuned
# according to your system, setup, and controller.
# This simply provides a baseline to start.

# Set the upper and lower bounds for your controller.
# These are the raw "Sample" values coming into
# your PC's audio line-in.
# To find yours, you may need to use --debug
UPPER_BOUND = 69
LOWER_BOUND = 25

# Configure radio channels here.
# The number corresponds to the index of which
# the value was extracted from in the buffer.
# To find yours, you may need to use --debug
RADIO_CH_ROLL = 8
RADIO_CH_PITCH = 0
RADIO_CH_YAW = 2
RADIO_CH_THROTTLE = 1
RADIO_CH_SWA = 3
RADIO_CH_SWB = 4
RADIO_CH_SWC = 5
RADIO_CH_SWD = 6

# Default works. Change if you have several
# VJOY devices hooked up.
VJOY_DEVICE_ID = 1

# Most likely this values is fine.
# If you are experiencing unreliable readings,
# you may need to use --raw to find yours.
rising_edge_trigger = 0.7

# Allow some time to pass inbetween frames 
# being sent from the radio -> PC
GRACE_PERIOD = 80 # minimumm samples/frame

# Here are the six available filter methods
# that are available by default.
# Each one has its perks, but some may prove
# to function better or more reliably for you.
# Experiment to find the best one for you.
# ------
# 0 - No filtering
# 1 - Boxcar filter (basic averaging of samples)
# 2 - Median Filter
# 3 - Low-pass Filter (Butterworth)
# 4 - Low-pass Filter (Chebyshev)
# 5 - Savitzky–Golay Filter (Not ideal)
FILTER_TYPE = 0

# Plot settings are trivial.
# Only work with these when using the
# --debug flag.
y_plot_range = (-1,1)
x_plot_range = (-10, 800)

window_plot_range = 1024
refresh_rate_plot = 10

# Don't touch these unless you know what
# you are doing or need a custom config.
SAMPLE_RATE = 44100
BLOCK_SIZE = 2048

INIT_SAMPLE_PASS = 20