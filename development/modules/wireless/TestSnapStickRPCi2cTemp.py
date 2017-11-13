from synapse.switchboard import *

RED_LED = 5
GRN_LED = 6

Athlete_1_NetAddr = '\x5D\xE3\xAB'
Athlete_2_NetAddr = '\x5D\xE5\x10'

def TurnOnGreenLed():
    writePin(GRN_LED, False)
def TurnOffGreenLed():
    writePin(GRN_LED, True)
    
def TurnOnRedLed():
    writePin(RED_LED, False)
def TurnOffRedLed():
    writePin(RED_LED, True)
    
def DetermineHelloWorld(msg):
    """This function will turn off the RED LED on the snapstick and pulse the GREEN LED for
    50 MS if we Recieved a Hello World Message from the other device that we are going to RPC"""
    if(msg == "Hello World"):
        TurnOffRedLed();
        pulsePin(6, 50, False);
        TurnOnRedLed();

@setHook(HOOK_STARTUP)
def init():
    setPinDir(GRN_LED, True)
    setPinDir(RED_LED, True)
    
    TurnOnRedLed();
    TurnOffGreenLed();
    
    initUart(1, 19200) # <= put your desired baudrate here!
    #flowControl(1, True, True)# <= set flow control to True or False as needed
    crossConnect(DS_UART1, DS_TRANSPARENT)

@setHook(HOOK_1S)
def requestString():
    myNum = '0'
    #rpc(Athlete_1_NetAddr, "sendMessageBack")
    rpc(Athlete_2_NetAddr, "sendMessageBack")

#def requestData():
 #   """Requests a Hello World Message from a device every second"""
    #if(rpc(Athlete_1_NetAddr, "callback","printRtnVal", "DetermineHelloWorld", "HelloWorld")):
    #    print "Message send was Successful\n"
    


