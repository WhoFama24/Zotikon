"""TestCases.py"""

import logging
import binascii
import sys
import time
import platform

from snapconnect import snap

# use this for snapstick sn200
SERIAL_TYPE = snap.SERIAL_TYPE_RS232

if platform.system() == 'Linux':

    # for beaglebone
    SERIAL_PORT = "/dev/ttyUSB0"

elif platform.system() == 'Windows':

    # COM3 for WINDOWS --do com number minus 1. So COM3 == (3-1) == 2
    SERIAL_PORT = 2

# used to identify the RF200 devices
Athlete_1_NetAddr = '\x5D\xE3\xAB'
Athlete_2_NetAddr = '\x5D\xE5\x10'
Athlete_3_NetAddr = '\x07\xA1\xDE'

log_file = open("LogFile.txt", "a")

# global variables used to keep track of how many requests have been sent or received for each device
sent_random_ath1 = 0
received_random_ath1 = 0
sent_random_ath2 = 0
received_random_ath2 = 0
sent_random_ath3 = 0
received_random_ath3 = 0


class BridgeVersionClient(object):
    def __init__(self):

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

        self.log = logging.getLogger("BridgeVersionClient")

        snapconnect_addr = self.comm.local_addr()
        self.log.info("SNAPconnect Address: %r" % binascii.hexlify(snapconnect_addr))

    def hook_open(self, serial_type, port, addr=None):
        """Callback function invoked when a serial connection is opened."""
        if addr:
            self.bridge_address = addr
            self.log.info("Serial connection opened to %s", binascii.hexlify(addr))
            self.log_display_and_file_for_next_test_speed(1, "5 seconds or 0.083")
            self.reschedule_random_request_events_and_timeout(1, 5, self.stop)

        else:
            self.log.critical("Unable to open serial connection")

        return addr

    def hook_close(self, serial_type, port):
        """Callback function invoked when a serial connection is closed."""
        self.log.info("Serial connection closed")

    def get_random(self, athlete_addr):
        global sent_random_ath1, sent_random_ath2, sent_random_ath3, received_random_ath1, received_random_ath2, \
            received_random_ath3

        athlete_num = 0
        sent_random = 0
        received = 0

        if athlete_addr == Athlete_1_NetAddr:
            athlete_num = 1
            sent_random_ath1 += 1
            sent_random = sent_random_ath1
            received = received_random_ath1
        elif athlete_addr == Athlete_2_NetAddr:
            athlete_num = 2
            sent_random_ath2 += 1
            sent_random = sent_random_ath2
            received = received_random_ath2
        elif athlete_addr == Athlete_3_NetAddr:
            athlete_num = 3
            sent_random_ath3 += 1
            sent_random = sent_random_ath3
            received = received_random_ath3

        log_file.write("sent            " + str(athlete_num) + "         " + str(time.time()) + "     " + str(
            sent_random) + "           " + str(received) + "\n")

        self.comm.rpc(athlete_addr, 'callback', 'log_response', 'random')

        return True

    def log_response(self, response):
        """Callback function invoked when the get_random is returned from an athlete."""
        global sent_random_ath1, sent_random_ath2, sent_random_ath3, received_random_ath1, received_random_ath2, \
            received_random_ath3

        athlete_num = 0
        sent_random = 0
        received = 0

        if self.comm.rpcSourceAddr() == Athlete_1_NetAddr:
            athlete_num = 1
            sent_random = sent_random_ath1
            received_random_ath1 += 1
            received = received_random_ath1
        elif self.comm.rpcSourceAddr() == Athlete_2_NetAddr:
            athlete_num = 2
            sent_random = sent_random_ath2
            received_random_ath2 += 1
            received = received_random_ath2
        elif self.comm.rpcSourceAddr() == Athlete_3_NetAddr:
            athlete_num = 3
            sent_random = sent_random_ath3
            received_random_ath3 += 1
            received = received_random_ath3

        log_file.write("received        " + str(athlete_num) + "         " + str(time.time()) + "     " +
                       str(sent_random) + "           " + str(received) + "\n")

        self.log.info("Response from Athlete " + str(athlete_num))

    def reschedule_random_request_events_and_timeout(self, random_interval, timeout_interval, timeout_func):
        self.event1 = self.comm.scheduler.schedule(random_interval, lambda: self.get_random(Athlete_1_NetAddr))
        self.event2 = self.comm.scheduler.schedule(random_interval, lambda: self.get_random(Athlete_2_NetAddr))
        self.event3 = self.comm.scheduler.schedule(random_interval, lambda: self.get_random(Athlete_3_NetAddr))
        self.timeout = self.comm.scheduler.schedule(timeout_interval, timeout_func)

    def log_display_and_file_for_next_test_speed(self, speed, period):
        self.log.info("Testing at " + str(speed) + " sec")
        log_file.write("\nTesting at " + str(speed) + " sec\nFor duration " + str(period) + " min\n")
        log_file.write("sent/received   athlete   time              sentCntr    recCntr\n\n")

    def stop(self):
        """Stop the SNAPconnect instance."""
        self.comm.close_all_serial()  # Close all serial connections opened with SNAPconnect
        log_file.write("\nTest Case quick done\n\n\n")
        log_file.close()
        sys.exit(0)  # Exit the program


def set_globals_0():
    global sent_random_ath1, sent_random_ath2, sent_random_ath3, received_random_ath1, received_random_ath2, \
        received_random_ath3

    sent_random_ath1 = 0
    sent_random_ath2 = 0
    sent_random_ath3 = 0
    received_random_ath1 = 0
    received_random_ath2 = 0
    received_random_ath3 = 0


if __name__ == "__main__":
    # Configure Python's built-in logging module to display any info or higher level messages

    logging.basicConfig(level=logging.INFO)
    log_file.write("THIS IS A QUICK TEST CASE\n\n")
    log_file.write("Test Case quick:    This is just to run the test quickly to see if the devices are responding\n\n")

    client = BridgeVersionClient()  # Instantiate a client instance

    # Start the SNAPconnect loop, nothing can happen after this point
    client.comm.loop()