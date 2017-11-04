"""TestCases.py

    This file creates test cases for seeing how well the SYNAPSE RF200 devices can communicate with each other.
    A run of this program will test the connections by making a random() call to each device. This makes the
    device return a random number. This is merely to test the connection and pass data back and forth.

    This test will create a log file called LogFile.txt and will append to it. It records the data in this format

            THIS IS A X TEST CASE

            Test Case X:    description goes here


            Testing at 1 sec
            For duration 5 seconds or 0.083 min
            sent/received   athlete   time              sentCntr    recCntr

            sent            1         1509786544.37     1           0
            sent            2         1509786544.37     1           0
            received        1         1509786544.47     1           1
            received        2         1509786544.51     1           1
            sent            1         1509786545.37     2           1
            sent            2         1509786545.37     2           1
            received        1         1509786545.43     2           2
            received        2         1509786545.46     2           2
            sent            1         1509786546.37     3           2
            sent            2         1509786546.37     3           2
            received        1         1509786546.44     3           3
            received        2         1509786546.46     3           3
            sent            1         1509786547.37     4           3
            sent            2         1509786547.37     4           3
            received        1         1509786547.41     4           4
            received        2         1509786547.45     4           4

            Test Case X done

    This program will run for a total of 8 minutes. It will send data at the following speeds for the following periods

    every 2 seconds for 1 minute
    every 1 second  for 1 minute
    every 0.5 sec   for 2 minutes
    every 0.25 sec  for 2 minutes
    every 0.125 sec for 2 minutes"""

import logging
import binascii
import sys
import time

from snapconnect import snap

#use this for snapstick sn200
SERIAL_TYPE = snap.SERIAL_TYPE_RS232

# COM3 for windows
SERIAL_PORT = 2

# used to identify the RF200 devices
Athlete_1_NetAddr = '\x5D\xE3\xAB'
Athlete_2_NetAddr = '\x5D\xE5\x10'

# create or append to our logfile
log_file = open("LogFile.txt", "a")

# global variables used to keep track of how many requests have been sent or received for each device
sent_random_ath1 = 0
received_random_ath1 = 0
sent_random_ath2 = 0
received_random_ath2 = 0


class BridgeVersionClient(object):
    """This class is used to connect to the snapstick sn200 and communicate with it"""
    def __init__(self):
        """set up inital things for the class such as functions, rpc functions, hooks, and opening the serial port"""

        # You can define what functions can be called remotely on your SNAPconnect instance
        # using the `funcs` argument
        funcs = {
            "get_random": self.get_random
        }

        # Create a SNAP instance
        self.comm = snap.Snap(funcs=funcs)

        # You can also define which functions can be called using `add_rpc_func`
        self.comm.add_rpc_func("log_response", self.log_response)

        # SNAPconnect also provides hooks for certain events, for example when the serial connection
        # is opened or closed
        self.comm.set_hook(snap.hooks.HOOK_SERIAL_OPEN, self.hook_open)
        self.comm.set_hook(snap.hooks.HOOK_SERIAL_CLOSE, self.hook_close)

        # Open a serial connection to your bridge
        self.comm.open_serial(SERIAL_TYPE, SERIAL_PORT)

        # create logger to write to display screen
        self.log = logging.getLogger("BridgeVersionClient")

        snapconnect_addr = self.comm.local_addr()
        self.log.info("SNAPconnect Address: %r" % binascii.hexlify(snapconnect_addr))

    def hook_open(self, serial_type, port, addr=None):
        """Once we open the serial port and have a connection start our random() calls at first interval and period"""
        if addr:
            self.bridge_address = addr
            self.log.info("Serial connection opened to %s", binascii.hexlify(addr))
            self.log_display_and_file_for_next_test_speed(2.0, 1)
            self.reschedule_random_request_events_and_timeout(2, 60, self.interval2)

        else:
            self.log.critical("Unable to open serial connection")

        return addr

    def hook_close(self, serial_type, port):
        """Let us know we are closing the serial port"""
        self.log.info("Serial connection closed")

    def get_random(self, athlete_addr):
        """This function makes a rpc call to the device specified by athlete_addr. It will increment the sent random
        globals for that device and will log data to the LogFile"""
        global sent_random_ath1, sent_random_ath2, received_random_ath1, received_random_ath2

        athlete_num = 0
        sent_random = 0
        received = 0

        # set data for athlete 1
        if athlete_addr == Athlete_1_NetAddr:
            athlete_num = 1
            sent_random_ath1 += 1
            sent_random = sent_random_ath1
            received = received_random_ath1

        # set data for athlete 2
        else:
            athlete_num = 2
            sent_random_ath2 += 1
            sent_random = sent_random_ath2
            received = received_random_ath2

        # log data to file
        log_file.write("sent            " + str(athlete_num) + "         " + str(time.time()) + "     " + str(
            sent_random) + "           " + str(received) + "\n")

        # send out actual command for the device to return the random() function
        self.comm.rpc(athlete_addr, 'callback', 'log_response', 'random')

        # necessary for schedular to not change our timeout period
        return True

    def log_response(self, response):
        """This function is called when the rpc from get random is return from the device we pinged. We are not actually
        doing anything with the response from the device we just want to see that we made a connection. It will then
        increment the received random globals for that device and will log data to the LogFile. This function will also
        make a log to the display screen which lets us know that we are getting some data so we can stop it if something
        is wrong."""
        global sent_random_ath1, sent_random_ath2, received_random_ath1, received_random_ath2

        athlete_num = 0
        sent_random = 0
        received = 0

        # received data for athlete 1
        if self.comm.rpcSourceAddr() == Athlete_1_NetAddr:
            athlete_num = 1
            sent_random = sent_random_ath1
            received_random_ath1 += 1
            received = received_random_ath1

        # received data for athlete 2
        else:
            athlete_num = 2
            sent_random = sent_random_ath2
            received_random_ath2 += 1
            received = received_random_ath2

        # log data to file
        log_file.write("received        " + str(athlete_num) + "         " + str(time.time()) + "     " +
                       str(sent_random) + "           " + str(received) + "\n")

        # log a response to the output screen so that we know we are getting some data
        self.log.info("Response from Athlete " + str(athlete_num))

    def interval2(self):
        """Starts the second interval and period for sending data"""
        set_globals_0()
        self.stop_events()
        self.log_display_and_file_for_next_test_speed(1.0, 1)
        self.reschedule_random_request_events_and_timeout(1, 60, self.interval3)

    def interval3(self):
        """Starts the third interval and period for sending data"""
        set_globals_0()
        self.stop_events()
        self.log_display_and_file_for_next_test_speed(0.5, 2)
        self.reschedule_random_request_events_and_timeout(0.5, 120, self.interval4)

    def interval4(self):
        """Starts the fourth interval and period for sending data"""
        set_globals_0()
        self.stop_events()
        self.log_display_and_file_for_next_test_speed(0.25, 2)
        self.reschedule_random_request_events_and_timeout(0.25, 120, self.interval5)

    def interval5(self):
        """Starts the fifth interval and period for sending data"""
        set_globals_0()
        self.stop_events()
        self.log_display_and_file_for_next_test_speed(0.125, 2)

        # before we go to new intervals on our timeout but for this last one we will stop the program
        self.reschedule_random_request_events_and_timeout(0.125, 120, self.stop)

    def reschedule_random_request_events_and_timeout(self, random_interval, timeout_interval, timeout_func):
        """This function creates the events on a certain time interval that allow us to send data back and forth
        to each device and to create a timer"""

        # make a get random call to each athlete device every random_interval seconds
        self.event1 = self.comm.scheduler.schedule(random_interval, lambda: self.get_random(Athlete_1_NetAddr))
        self.event2 = self.comm.scheduler.schedule(random_interval, lambda: self.get_random(Athlete_2_NetAddr))

        # create a timeout that will go off at timeout_interval and call the timeout_func
        self.timeout = self.comm.scheduler.schedule(timeout_interval, timeout_func)

    def log_display_and_file_for_next_test_speed(self, speed, period):
        """This function handles some common printing of text for each interval and period. It also displays some of it
        to the display screen to let us know we have changed our timing period and interval"""
        self.log.info("Testing at " + str(speed) + " sec")
        log_file.write("\nTesting at " + str(speed) + " sec\nFor duration " + str(period) + " min\n")
        log_file.write("sent/received   athlete   time              sentCntr    recCntr\n\n")

    def stop_events(self):
        """This function will stop sending get random calls to each device and the timeout"""
        self.event1.Stop()
        self.event2.Stop()
        self.timeout.Stop()

    def stop(self):
        """Stop the SNAPconnect instance and finish the test case."""
        self.comm.close_all_serial()  # Close all serial connections opened with SNAPconnect
        log_file.write("\nTest Case X done\n\n\n")
        log_file.close()
        sys.exit(0)  # Exit the program


def set_globals_0():
    """This resets our global variables to 0. This makes it easier to look at between timing interval and period
    situations."""
    global sent_random_ath1, sent_random_ath2, received_random_ath1, received_random_ath2
    sent_random_ath1 = 0
    sent_random_ath2 = 0
    received_random_ath1 = 0
    received_random_ath2 = 0


if __name__ == "__main__":

    # Configure Python's built-in logging module to display any info or higher level messages
    logging.basicConfig(level=logging.INFO)

    # write initial lines to our LogFile
    log_file.write("THIS IS A NEW TEST CASE\n\n")
    log_file.write("Test Case X:    description can go here\n\n")

    # Instantiate a client instance
    client = BridgeVersionClient()

    # Start the SNAPconnect loop, nothing can happen after this point
    client.comm.loop()
