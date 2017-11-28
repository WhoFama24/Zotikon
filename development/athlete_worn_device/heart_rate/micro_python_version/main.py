# Simple heart beat reader for Raspberry pi using ADS1x15 family of ADCs and a pulse sensor - http://pulsesensor.com/.
# The code borrows heavily from Tony DiCola's examples of using ADS1x15 with
# Raspberry pi and WorldFamousElectronics's code for PulseSensor_Amped_Arduino

# Author: Udayan Kumar
# License: Public Domain

from pyb import *
from utime import *
# Import the ADS1x15 module.    # TODO: this will change for micropython and synapse



if __name__ == '__main__':

    adc = ADC(Pin('X11'))    # TODO: this will need to be changed for the micropython board or Synapse
    # initalization
    GAIN = 1    # TODO: this gain may need to change to not attenuate as the signal is very small
    curState = 0
    thresh = 525  # TODO: change for mid point in the waveform which has been at about
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
    skip = False
    counter = 0
    flag = False

    lastTime = int(millis()) #maybe no *1000?

    # Main loop. use Ctrl-c to stop the code
    while True:
        flag = False
        skip = False
        counter += 1

        # read from the ADC
        Signal = adc.read()   #original source used RaspPi code with a gain parameter attempt to port by multiplying by gain which may need adjustment
        #print("Signal before gain: " + str(Signal))
        Signal = Signal * GAIN
        #print("Signal after gain: " + str (Signal))
        # print()
        curTime = int(millis()) #maybe no *1000?

        sampleCounter += curTime - lastTime      #                   # keep track of the time in mS with this variable
        lastTime = curTime
        N = sampleCounter - lastBeatTime     #  # monitor the time since the last beat to avoid noise

        ##  find the peak and trough of the pulse wave
        if Signal < thresh and N > (IBI//5)*3 :  #       # avoid dichrotic noise by waiting 3/5 of last IBI
            if Signal < T :                        # T is the trough
              T = Signal                         # keep track of lowest point in pulse wave
              #print("If 1.")

        if Signal > thresh and  Signal > P:           # thresh condition helps avoid noise
            P = Signal                             # P is the peak
                                                # keep track of highest point in pulse wave

          #  NOW IT'S TIME TO LOOK FOR THE HEART BEAT
          # signal surges up in value every time there is a pulse
        if N > 250 :                                   # avoid high frequency noise
            #print("If 3.")
            if  (Signal > thresh) and  (Pulse == False) and  (N > (IBI//5)*3)  :
                flag = True
                Pulse = True                               # set the Pulse flag when we think there is a pulse
                IBI = sampleCounter - lastBeatTime         # measure time between beats in mS
                lastBeatTime = sampleCounter               # keep track of time for next pulse

                if secondBeat :                        # if this is the second beat, if secondBeat == TRUE
                    secondBeat = False                  # clear secondBeat flag
                # for i in range(0,10):             # seed the running total to get a realisitic BPM at startup
                #   rate[i] = IBI
                i = 0
                while i < 10:
                    rate[i] = IBI
                    i += 1

                if firstBeat :                        # if it's the first time we found a beat, if firstBeat == TRUE
                    firstBeat = False                   # clear firstBeat flag
                    secondBeat = True                   # set the second beat flag
                    # continue                              # IBI value is unreliable so discard it
                    skip = True

        if not skip:
            skip = False
            # if N > 250 :                                   # avoid high frequency noise
                # print("No continue. if N > 250.")
            if  (flag == True)  :
                # print("Never getting into this if statement.")
                # keep a running total of the last 10 IBI values
                runningTotal = 0                  # clear the runningTotal variable

                # for i in range(0,9):                # shift data in the rate array
                #   rate[i] = rate[i+1]                  # and drop the oldest IBI value
                #   runningTotal += rate[i]              # add up the 9 oldest IBI values
                i = 0
                while i < 9:
                    rate[i] = rate[i+1]
                    runningTotal += rate[i]
                    i += 1

                rate[9] = IBI                          # add the latest IBI to the rate array
                runningTotal += rate[9]                # add the latest IBI to runningTotal
                runningTotal //= 10                     # average the last 10 IBI values
                BPM = 60000//runningTotal               # how many beats can fit into a minute? that's BPM!
                heartRate = BPM
                print("BPM: " + str(heartRate))              # PORT FROM: print 'BPM: {}'.format(BPM)

            if Signal < thresh and Pulse == True :   # when the values are going down, the beat is over
                Pulse = False                         # reset the Pulse flag so we can do it again
                amp = P - T                           # get amplitude of the pulse wave
                thresh = amp//2 + T                    # set thresh at 50% of the amplitude
                P = thresh                            # reset these for next time
                T = thresh
                #print("If 4.")

            if N > 2500 :                          # if 2.5 seconds go by without a beat
                thresh = 512                          # set thresh default
                P = 512                               # set P default
                T = 512                               # set T default
                lastBeatTime = sampleCounter          # bring the lastBeatTime up to date
                firstBeat = True                      # set these to avoid noise
                secondBeat = False                    # when we get the heartbeat back
                #print ("no beats found")
                heartRate = 0
                print("no beats found")
            sleep(0.005)
