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

        see more at https://developer.synapse-wireless.com/modules/atmega/builtins.html#readadc"""

from synapse.platforms import *
from synapse.switchboard import *

# used for heartbeat LED
GREEN_LED = GPIO_1

melexisTemp = []
ds1631Temp = []
heartRate = []


@setHook(HOOK_STARTUP)
def startup():
    """Initialize LED pins to output. Set up I2C and tell the ds1631 to start reading temperature"""
    setPinDir(GREEN_LED, True)
    i2cInit(True)

    # tell the ds1631 to start calculating temperature
    i2cInit(False)
    i2cWrite(chr(0x90) + chr(0x51), 5, False, False)


@setHook(HOOK_100MS)
def heart_beat_led():
    """Flash GREEN LED every 100ms"""
    writePin(GREEN_LED, not readPin(GREEN_LED))


# @setHook(HOOK_1S)
def melexis_temp_read():
    """Not implemented"""
    pass


# @setHook(HOOK_1S)
def ds1631_temp_read():
    """Reads the DS1631 for a temperature. Record if we get a valid temperature"""

    # global ds1631Temp

    finalStringToSend = ""
    i2cWrite(chr(0x90) + chr(0xAA), 5, False, True)
    stringToSend = i2cRead(chr(0x91), 2, 1, False)
    if getI2cResult() == 1:
        count = 0
        for c in stringToSend:
            if (count == 0):

                finalStringToSend += str(ord(c))
                finalStringToSend += "."
                count += 1
            else:
                finalStringToSend += str(ord(c) >> 4) + " degrees Celsius."

        # ds1631Temp.append(finalStringToSend)

        return finalStringToSend

    return 0


# @setHook(HOOK_1S)
def heart_rate_read():
    """Reads the adc for heart voltage. If we reach a certain threshold then we need to record this as a heartbeat."""

    # global heartRate

    heart_voltage = readAdc(0)
    # if 0 < heart_voltage < 1023:
    # heartRate.append(heart_voltage)
    # return heart_voltage

    return heart_voltage


def get_data_string_formatted_for_portal():
    """Return heart rate and temperature data collected by this athlete worn device. This is useful for looking at data
    on Portal. All it does is put some new lines in the response to make it easier to look at on portal."""

    # global heartRate, ds1631Temp

    return "\n\nheart rate: " + str(heart_rate_read()) + "\ntemperature: " + ds1631_temp_read()


def get_data_string():
    """Return heart rate and temperature data collected by this athlete worn device. In order to pass multiple values
    over one function it seems easiest to pass it as a string. Passing it as a list does not work."""

    # global heartRate, ds1631Temp

    return str(heart_rate_read()) + " " + str(ds1631_temp_read())
