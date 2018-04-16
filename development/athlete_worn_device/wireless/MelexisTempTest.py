from synapse.platforms import *
from synapse.switchboard import *

GREEN_LED = GPIO_1


@setHook(HOOK_STARTUP)
def startup():
    """Initialize LED pins to output"""
    setPinDir(GREEN_LED, True) 
    setPinDir(GPIO_17, True)
    setPinDir(GPIO_18, True)
    writePin(GPIO_17, True)
    writePin(GPIO_18, True)
    
    #i2cInit(False) #initialize i2c without pullups
    
    
@setHook(HOOK_10MS)
def HeartBeatLED():
    """Flash GREEN LED every 100ms"""
    writePin(GREEN_LED, not readPin(GREEN_LED))
    

def test_writing_i2c_pins():
    MSB = 0
    LSB = 0
    
    #start
    writePin(GPIO_17, False)
    writePin(GPIO_18, False)
   
    #Byte 1
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 0)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 0)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #ACK
    setPinDir(GPIO_17, False)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    setPinDir(GPIO_17, True)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #Byte 2
    writePin(GPIO_17, 0)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 0)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 0)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 0)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)    
    
    #ACK
    writePin(GPIO_17, 0)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #Restart
    writePin(GPIO_17, True)
    writePin(GPIO_18, True)
    writePin(GPIO_17, False)
    writePin(GPIO_18, False)
    
    #Byte 3
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 0)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 0)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    writePin(GPIO_17, 1)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #ack
    setPinDir(GPIO_17, False)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #read bit
    setPinDir(GPIO_17, True)
    writePin(GPIO_17, False)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    setPinDir(GPIO_17, False)
    if readPin(GPIO_17):
        LSB += 128
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        LSB += 64
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        LSB += 32
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        LSB += 16
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        LSB += 8
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        LSB += 4
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        LSB += 2
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    LSB += readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #ACK
    setPinDir(GPIO_17,True)
    writePin(GPIO_17, False)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #read byte 2
    setPinDir(GPIO_17,False)
    if readPin(GPIO_17):
        MSB += 128
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        MSB += 64
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        MSB += 32
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        MSB += 16
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        MSB += 8
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        MSB += 4
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    if readPin(GPIO_17):
        MSB += 2
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    MSB += readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #ACK
    setPinDir(GPIO_17,True)
    writePin(GPIO_17, False)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #read byte 3
    setPinDir(GPIO_17,False)
    readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    readPin(GPIO_17)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #ACK
    setPinDir(GPIO_17,True)
    writePin(GPIO_17, False)
    writePin(GPIO_18, True)
    writePin(GPIO_18, False)
    
    #leave them high
    writePin(GPIO_17, True)
    writePin(GPIO_18, True)
    
    #calculate temp from data
    total = (MSB * 256 + LSB)
    Kelvin = (total) / 50
    Leftover = total - (Kelvin * 50)
    decimal = Leftover * 2
    Celcius = Kelvin - 273
        
    #bigstr =   "   total: " + str(total) + "   Kelvin: " + str(Kelvin) + "   Leftover: " + str(Leftover) + "   decimal: " + str(decimal) + "   Celcius: " + str(Celcius)
    #return bigstr
    
    if decimal < 10:
        decimal = "0" + str(decimal)
    
    return "Celcius: " + str(Celcius) + "." + str(decimal)
    