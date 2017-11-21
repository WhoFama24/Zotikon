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
import time

# used for heartbeat LED
GREEN_LED = GPIO_1


melexisTemp = []
ds1631Temp = []
heartRate = []


# initialization 
GAIN = 1    # TODO: this gain may need to change 
curState = 0
thresh = 525  # TODO: needs to change for new VREF
P = 512
T = 512
stateChanged = 0
sampleCounter = 0
lastBeatTime = 0
firstBeat = True
secondBeat = False
Pulse = False
IBI = 600
rate = [0]*10
amp = 100
heartRate = 0

lastTime = int(time.time()*1000)

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

# TODO: Needs to run every 0.005s
 @setHook(HOOK_5MS)
def heart_rate_read():
    """Reads the adc for heart voltage. If we reach a certain threshold then we need to record this as a heartbeat."""

    # global heartRate

    Signal = readAdc(0)
    Signal = Signal * GAIN
    curTime = int(time.time()*1000)

    sampleCounter += curTime - lastTime      #                   # keep track of the time in mS with this variable
    lastTime = curTime
    N = sampleCounter - lastBeatTime     #  # monitor the time since the last beat to avoid noise
    #print N, Signal, curTime, sampleCounter, lastBeatTime

    ##  find the peak and trough of the pulse wave
    if Signal < thresh and N > (IBI/5)*3 :  #       # avoid dichrotic noise by waiting 3/5 of last IBI
        if Signal < T :                        # T is the trough
            T = Signal                         # keep track of lowest point in pulse wave 

    if Signal > thresh and  Signal > P:           # thresh condition helps avoid noise
        P = Signal                             # P is the peak
                                            # keep track of highest point in pulse wave

        #  NOW IT'S TIME TO LOOK FOR THE HEART BEAT
        # signal surges up in value every time there is a pulse
    if N > 250 :                                   # avoid high frequency noise
        if  (Signal > thresh) and  (Pulse == False) and  (N > (IBI/5)*3)  :       
            Pulse = True                               # set the Pulse flag when we think there is a pulse
            IBI = sampleCounter - lastBeatTime         # measure time between beats in mS
            lastBeatTime = sampleCounter               # keep track of time for next pulse

            if secondBeat :                        # if this is the second beat, if secondBeat == TRUE
            secondBeat = False                  # clear secondBeat flag
            for i in range(0,10):             # seed the running total to get a realisitic BPM at startup
                rate[i] = IBI                      

            if firstBeat :                        # if it's the first time we found a beat, if firstBeat == TRUE
            firstBeat = False                   # clear firstBeat flag
            secondBeat = True                   # set the second beat flag
            continue                              # IBI value is unreliable so discard it


            # keep a running total of the last 10 IBI values
            runningTotal = 0                  # clear the runningTotal variable    

            for i in range(0,9):                # shift data in the rate array
            rate[i] = rate[i+1]                  # and drop the oldest IBI value 
            runningTotal += rate[i]              # add up the 9 oldest IBI values

            rate[9] = IBI                          # add the latest IBI to the rate array
            runningTotal += rate[9]                # add the latest IBI to runningTotal
            runningTotal /= 10                     # average the last 10 IBI values 
            BPM = 60000/runningTotal               # how many beats can fit into a minute? that's BPM!
            heartRate = BPM
            #print("BPM: {}").format(BPM)          # PORT FROM: print 'BPM: {}'.format(BPM)

    if Signal < thresh and Pulse == True :   # when the values are going down, the beat is over
        Pulse = False                         # reset the Pulse flag so we can do it again
        amp = P - T                           # get amplitude of the pulse wave
        thresh = amp/2 + T                    # set thresh at 50% of the amplitude
        P = thresh                            # reset these for next time
        T = thresh

    if N > 2500 :                          # if 2.5 seconds go by without a beat
        thresh = 512                          # set thresh default
        P = 512                               # set P default
        T = 512                               # set T default
        lastBeatTime = sampleCounter          # bring the lastBeatTime up to date        
        firstBeat = True                      # set these to avoid noise
        secondBeat = False                    # when we get the heartbeat back
        heartRate = 0
    # if 0 < heart_voltage < 1023:
    # heartRate.append(heart_voltage)
    # return heart_voltage

    return heartRate


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