"""HeartRateAndTempReadRF200.py
    This file is used to gathering heart rate and temperature on the synapse RF200 devices. In order to set this up
    you should do the following:

    Basic set up:
        make sure that you have your circuits and pieces powered by the same ground and power on the breadboard.

    Temperature:
        Hook up the ds1631 on a bread board. Hook up A0, A1, and A2 to ground for a 000 I2C address. Connect the SDA
        pin to GPIO 17 on the breakout board. connect the SCL pin to GPIO 18 on the breakout board.
        see more at https://developer.synapse-wireless.com/modules/rf200/port-mapping.html#i2c
        You can run ds1631_temp_read or get_data_string() on portal to see this output.

    Heart rate:
        For now all the heart rate function does is read the ADC pin and give a value between 0 and 1023. This is a
        10 bit ADC and has an internal VREF of 1.6 volts. In order to get a valid reading make sure you are using the
        same ground from the volatge you are reading. Hook up the GPIO 11 pin on the breakout board to the voltage
        source you want to read.
        You can run ds1631_temp_read or get_data_string() on portal to see this output.
        see more at https://developer.synapse-wireless.com/modules/atmega/builtins.html#readadc

        The algorithm for heart rate is modified from the following:

            -Simple heart beat reader for Raspberry pi using ADS1x15 family of ADCs and a pulse sensor
            -
            - http://pulsesensor.com/
            -
            -The code borrows heavily from Tony DiCola's examples of using ADS1x15 with
            -Raspberry pi and WorldFamousElectronics's code for PulseSensor_Amped_Arduino
            -
            -Author: Udayan Kumar
            -License: Public Domain


        it can also be found in this repo at development/athlete_worn_device/heart_rate/micro_python/version/main.py"""

from synapse.platforms import *
from synapse.hardTime import *


# used for heartbeat LED
GREEN_LED = GPIO_1

# heart sensor Global Variables
heartRate = 0
GAIN = 1
curState = 0
thresh = 250
P = 220
T = 220
stateChanged = 0
sampleCounter = 0
lastBeatTime = 0
firstBeat = True
secondBeat = False
Pulse = False
IBI = 600
amp = 100
skip = False
counter = 0
flag = False
Signal = 0
N = 0

# use these arrays to handle the upper and lower bytes of the IBI over 10 periods.
# This is passed to the trainer station to calculate heart rate. Synapse does
# not support any larger data types than bytes for lists
rate = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
rate2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


@setHook(HOOK_STARTUP)
def startup():
    """Initialize LED pins to output. Set up I2C and tell the ds1631 to start reading temperature. Start the Hardware
    Timer and initialize our global byte lists."""

    global rate, rate2

    setPinDir(GREEN_LED, True)
    i2cInit(True)
    rate = rate[:]
    rate2 = rate2[:]

    # tell the ds1631 to start calculating temperature
    i2cInit(False)
    i2cWrite(chr(0x90) + chr(0x51), 5, False, False)

    # start HW timer to get current time in heartRate Calculation
    initHwTmr()


@setHook(HOOK_100MS)
def heart_beat_led():
    """Flash GREEN LED every 100ms"""
    writePin(GREEN_LED, not readPin(GREEN_LED))


def get_sample_count():
    global sampleCounter
    return sampleCounter


def get_timer():
    return tmrMs()


def get_adc():
    return readAdc(0)


def get_ibi():
    global IBI
    return IBI


def get_rate():
    global rate, rate2
    i = 0
    return_str = "rate: "
    while i < 10:
        rate_value = rate[i] << 8 | rate2[i]
        return_str += str(rate_value) + " "
        i += 1
    return return_str


def ds1631_temp_read():
    """Reads the DS1631 for a temperature. Record if we get a valid temperature"""

    final = ""
    i2cWrite(chr(0x90) + chr(0xAA), 5, False, True)
    to_send = i2cRead(chr(0x91), 2, 1, False)
    if getI2cResult() == 1:
        count = 0
        for c in to_send:
            if count is 0:

                final += str(ord(c))
                final += "."
                count += 1
            else:
                decimal = ord(c) >> 4

                # TODO format this to handle the decimal correctly
                if decimal > 10:
                    decimal = 95
                    final += str(decimal) + " degrees Celsius."

        return final

    return 0


@setHook(HOOK_10MS)
def heart_rate_read():
    """Reads the adc for heart voltage. This needs to be updated next semester in Design 2. For now, this calculates an
    list of IBI's that are sent to the monitoring station to calculate heart rate. This array is calculated using 2 byte
    arrays since this is what synapse supports. The calculation is done on the monitoring side because we have to divide
    by some large numbers that synapse does not support. For more information on this algorithm, see if information at
    the top of this document and go to the original source."""

    global N, Signal, GAIN, curState, thresh, P, T, stateChanged, sampleCounter, lastBeatTime, firstBeat,\
        secondBeat, Pulse, IBI, rate, amp, heartRate, skip, flag, rate2

    flag = False
    skip = False

    # read from the ADC
    Signal = readAdc(0)
    time_elapsed = tmrMs()
    sampleCounter += time_elapsed     # keep track of the time in mS with this variable
    resetTmr()

    if sampleCounter < 0:
        sampleCounter = time_elapsed
        lastBeatTime = 0

    N = sampleCounter - lastBeatTime                 # monitor the time since the last beat to avoid noise

    # find the peak and trough of the pulse wave
    if Signal < thresh and N > (IBI/5)*3:           # avoid dichrotic noise by waiting 3/5 of last IBI
        if Signal < T:                               # T is the trough
            T = Signal                               # keep track of lowest point in pulse wave

    if Signal > thresh and Signal > P:              # thresh condition helps avoid noise
        P = Signal                                   # P is the peak

    # NOW IT'S TIME TO LOOK FOR THE HEART BEAT
    # signal surges up in value every time there is a pulse
    if N > 250:
        if (Signal > thresh) and not Pulse and (N > (IBI/5)*3):
            flag = True
            Pulse = True                            # set the Pulse flag when we think there is a pulse
            IBI = sampleCounter - lastBeatTime      # measure time between beats in mS
            lastBeatTime = sampleCounter            # keep track of time for next pulse

            if secondBeat:                          # if this is the second beat, if secondBeat == TRUE
                secondBeat = False                  # clear secondBeat flag

            i = 0
            while i < 10:                           # initially seed the array with the first value
                rate[i] = chr((IBI >> 8) & 0xFF)
                rate2[i] = chr(IBI & 0xFF)
                i += 1

            if firstBeat:                           # if it's the first time we found a beat, if firstBeat == TRUE
                firstBeat = False                   # clear firstBeat flag
                secondBeat = True                   # set the second beat flag
                skip = True                         # IBI value is unreliable so discard it

    if not skip:
        skip = False
        if flag:
            i = 0
            while i < 9:                            # shift data in the rate array
                rate[i] = rate[i+1]
                rate2[i] = rate2[i+1]               # and drop the oldest IBI value
                i += 1

            rate[9] = (IBI >> 8) & 0xFF             # add the latest IBI to the rate array
            rate2[9] = IBI & 0xFF                   # this array is sent to the trainer station to do Heart Rate

        if Signal < thresh and Pulse:               # when the values are going down, the beat is over
            Pulse = False                           # reset the Pulse flag so we can do it again
            amp = P - T                             # get amplitude of the pulse wave
            thresh = amp/2 + T                      # set thresh at 50% of the amplitude
            P = thresh                              # reset these for next time
            T = thresh

        if N > 2500:                                # if 2.5 seconds go by without a beat
            thresh = 250                            # set thresh default
            P = 220                                 # set P default
            T = 220                                 # set T default
            lastBeatTime = sampleCounter            # bring the lastBeatTime up to date
            firstBeat = True                        # set these to avoid noise
            secondBeat = False                      # when we get the heartbeat back


def get_data_string_formatted_for_portal():
    """Return heart rate and temperature data collected by this athlete worn device. This is useful for looking at data
    on Portal. All it does is put some new lines in the response to make it easier to look at on portal."""

    global rate, rate2
    i = 0
    return_str = ""
    while i < 10:
        rate_value = rate[i] << 8 | rate2[i]
        return_str += str(rate_value) + " "
        i += 1

    return "\n\nheart rate IBI array: " + return_str + "\ntemperature: " + str(ds1631_temp_read())


def get_data_string():
    """Return heart rate and temperature data collected by this athlete worn device. In order to pass multiple values
    over one function it seems easiest to pass it as a string. Passing it as a list does not work."""

    global rate, rate2
    i = 0
    return_str = ""
    while i < 10:
        rate_value = rate[i] << 8 | rate2[i]
        return_str += str(rate_value) + " "
        i += 1

    return return_str + " " + str(ds1631_temp_read())
