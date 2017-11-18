from synapse.platforms import *
from synapse.switchboard import *

GREEN_LED = GPIO_1
YELLOW_LED = GPIO_2

def HelloWorld():
    """This function will pulse the YELLOW LED everytime it is called and return our Hello World
    msg"""
    pulsePin(YELLOW_LED, 50, True)
    return "Hello World"

@setHook(HOOK_STARTUP)
def startup():
    """Initialize LED pins to output"""
    setPinDir(GREEN_LED, True) 
    setPinDir(YELLOW_LED, True)
    crossConnect(DS_TRANSPARENT,DS_STDIO)
    ucastSerial('\x09\x9F\xF8')
    
    
    i2cInit(True)
    
    
@setHook(HOOK_100MS)
def HeartBeatLED():
    """Flash GREEN LED every 100ms"""
    writePin(GREEN_LED, not readPin(GREEN_LED))
    
#@setHook(HOOK_1S)
def sendMessageBack():
    #variable += '1'
    pulsePin(YELLOW_LED, 100, True)
    finalStringToSend = ""
    i2cWrite(chr(0x00)+chr(0x27),1,False,True)
    stringToSend = i2cRead(chr(0x01), 3, 1, False)
    if(getI2cResult() == 1):
        for c in stringToSend:
            finalStringToSend += str(ord(c))
        print "Temperature string is: "+finalStringToSend
    else:
        print "Unsuccessful Temperature Read!"
    