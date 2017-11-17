from synapse.platforms import *
from synapse.switchboard import *

GREEN_LED = GPIO_1
YELLOW_LED = GPIO_2

melexisTemp = []
ds1631Temp = []
heartRate = []


@setHook(HOOK_STARTUP)
def startup():
    """Initialize LED pins to output"""
    setPinDir(GREEN_LED, True)
    setPinDir(YELLOW_LED, True)
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


def get_heart_rate():
    """Return heart rate and temperature data collected by this athlete worn device."""

    # global heartRate, ds1631Temp

    return heart_rate_read()


def get_temperature():
    """Return heart rate and temperature data collected by this athlete worn device."""

    # global heartRate, ds1631Temp

    return ds1631_temp_read()


def get_data_string():
    """Return heart rate and temperature data collected by this athlete worn device. This is useful for looking at data
    on Portal."""

    # global heartRate, ds1631Temp

    return "\n\nheart rate: " + str(heart_rate_read()) + "\ntemperature: " + ds1631_temp_read()
