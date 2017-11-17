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

    i2cWrite(chr(0x90) + chr(0xAA), 5, False, True)
    temp_not_formatted = i2cRead(chr(0x91), 2, 1, False)
    if getI2cResult() == 1:
        # ds1631Temp.append(temp_not_formatted)
        return temp_not_formatted


# @setHook(HOOK_1S)
def heart_rate_read():
    """Reads the adc for heart voltage. If we reach a certain threshold then we need to record this as a heartbeat."""

    # global heartRate

    heart_voltage = readADC(0)
    if 0 < heart_voltage < 1023:
        # heartRate.append(heart_voltage)
        return heart_voltage


def get_data():
    """Return heart rate and temperature data collected by this athlete worn device."""

    # global heartRate, ds1631Temp

    return [HeartRateRead(), DS1631TempRead()]

