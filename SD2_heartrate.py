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
TIMEOUT = 2500   # timeout after 2.5 seconds
thresh = 512     # TODO: Needs to be tweaked for typical half of peak signal value
rateIndex = 0    # used to place new IBIs into IBI virtual array, replacing old data with new
numOfIBIs = 0    # keep up with how many valid IBIs are in the virtual array
IBI = 0          # time in ms In Between Beats
hfNoise = 250    # check time against this value to make sure signal isn't noise
heartRate = 0

# STATE MACHINE
# S0_NO_BEAT_DETECTED: state on startup, if beat is detected, start timer
# S1_WAIT_BEAT: Caclulates time between beats and averages total
S0_NO_BEAT_DETECTED = 0
S1_WAIT_BEAT = 1
currentState = S0_NO_BEAT_DETECTED

# use these signed 16-bit ints to store IBI values
rate0 = 0
rate1 = 0
rate2 = 0
rate3 = 0
rate4 = 0
rate5 = 0
rate6 = 0
rate7 = 0
rate8 = 0
rate9 = 0

# Inputs: action determines whether to modify the value at index
# or return the value, index is the location in the virtual array
# from indices 0-9 inclusive, and value is needed if action is MODIFY. 
# If action is RETURN, value can be anything.
# Outputs: MODIFY->no output on success; RETURN-> 
MODIFY = 0
RETURN = 1
def f_ai16_rate(action, index, value):
    global rate0,rate1,rate2,rate3, rate4,rate5,rate6,rate7,rate8,rate9
    if action == RETURN:
        if index == 0:
            return rate0
        elif index == 1:
            return rate1
        elif index == 2:
            return rate2
        elif index == 3:
            return rate3
        elif index == 4:
            return rate4
        elif index == 5:
            return rate5
        elif index == 6:
            return rate6
        elif index == 7:
            return rate7
        elif index == 8:
            return rate8
        elif index == 9:
            return rate9
        else:
            return -2
    elif action == MODIFY:
        if index == 0:
            rate0 = value
        elif index == 1:
            rate1 = value
        elif index == 2:
            rate2 = value
        elif index == 3:
            rate3 = value
        elif index == 4:
            rate4 = value
        elif index == 5:
            rate5 = value
        elif index == 6:
            rate6 = value
        elif index == 7:
            rate7 = value
        elif index == 8:
            rate8 = value
        elif index == 9:
            rate9 = value
        else:
            return -3
    else:
        return -1


@setHook(HOOK_STARTUP)
def startup():
    """Initialize LED pins to output. Set up I2C and tell the ds1631 to start reading temperature. Start the Hardware
    Timer and initialize our global byte lists."""

    global heartRate

    setPinDir(GREEN_LED, False)

    # dont touch this. this sets it to where we can change the value
    
    setPinDir(GPIO_12, True)

    # change this to true or false to keep the pin high or low for the duration of the program
    writePin(GPIO_12, False)

    i2cInit(True)

    # tell the ds1631 to start calculating temperature
    i2cInit(False)
    i2cWrite(chr(0x90) + chr(0x51), 5, False, False)

    # start HW timer to get current time in heartRate Calculation
    initHwTmr()


#@setHook(HOOK_100MS)
#def heart_beat_led():
    #"""Flash GREEN LED every 100ms"""
    #writePin(GREEN_LED, not readPin(GREEN_LED))

def get_timer():
    return tmrMs()


def get_adc():
    return readAdc(0)


def get_ibi():
    global IBI
    return IBI


def get_rate():
    global heartRate
    return heartRate


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
    global TIMEOUT, rateIndex, numOfIBIs, IBI, hfNoise, heartRate, S0_NO_BEAT_DETECTED, S1_WAIT_BEAT, currentState, thresh
    signal = readAdc(0)
    timeSinceBeat = tmrMs() # timer needs to be reset before this runs for the first time

    # TIMEOUT CONDITION
    if timeSinceBeat >= TIMEOUT:
        currentState = S0_NO_BEAT_DETECTED
        resetTmr()

        # clear the array used to caclulate the running total
        i = 0
        while i < 10:
            f_ai16_rate(MODIFY, i, 0)
            i += 1
    

    # S0_NO_BEAT_DETECTED
    if currentState == S0_NO_BEAT_DETECTED:
        runningTotal = 0
        numOfIBIs = 0
        rateIndex = 0
        thresh = 220                                # thresh may need adjusting
        heartRate = 0
        rateIndex = 0

        if signal > thresh:
            currentState = S1_WAIT_BEAT
            resetTmr()

    # S1_WAIT_BEAT
    elif currentState == S1_WAIT_BEAT:
        if tmrMs() > hfNoise:                       # nothing can be recorded until 250 ms after a beat
            if signal > thresh:                     # if enough time has elapsed since the last beat, check for beat
                IBI = timeSinceBeat                 # capture time In Between Beats
                resetTmr()                          # start timing for the next beat
                f_ai16_rate(MODIFY, rateIndex, IBI) # add IBI to rate array
                if numOfIBIs < 10:                  # if array isn't full, increment number of IBIs in array
                    numOfIBIs += 1
                
                # add all of the IBIs together
                runningTotal = 0
                i = 0
                while i < numOfIBIs:
                    runningTotal += f_ai16_rate(RETURN, i, None)
                    i += 1

                BP30s = 30000 / runningTotal        # caclulate beats per half minute to meet signed 16 bit constraint
                heartRate = 2 * BP30s               # convert to beats per minute
                rateIndex = (rateIndex + 1) % 10    # increment index and wrap if needed to replace old data
                
    else:
        currentState = S0_NO_BEAT_DETECTED



def get_data_string_formatted_for_portal():
    """Return heart rate and temperature data collected by this athlete worn device. This is useful for looking at data
    on Portal. All it does is put some new lines in the response to make it easier to look at on portal."""

    global heartRate
    return "\n\nheart rate: " + str(heartRate) + "\ntemperature: " + str(ds1631_temp_read())


def get_data_string():
    """Return heart rate and temperature data collected by this athlete worn device. In order to pass multiple values
    over one function it seems easiest to pass it as a string. Passing it as a list does not work."""

    global heartRate
    return heartRate + " " + str(ds1631_temp_read())
