"""TrainerStation.py

    This file is used to connect to the usb snapstick in order to collect data from the athlete worn devices. This
    function schedules a poll for each device that receives its heart rate and temperature. This program will buffer
    in responses for the WAIT_FOR_INITIAL_BUFFER_SECONDS. It polls devices every DEVICE_POLL_INTERVAL_SECONDS_SECONDS.
    Lastly, it will write to the data base for each device after we wait for the buffer to fill every
    DATABASE_UPDATE_INTERVAL_SECONDS_SECONDS.

    Make sure that the snapstick is not connected to portal or has any program loaded on it. This may cause us to not
    be able to connect to the snapstick."""

import logging
import binascii
import sys
import time
import argparse
import requests
import platform

from influxdb import InfluxDBClient
from snapconnect import snap

# use this for snapstick sn200
SERIAL_TYPE = snap.SERIAL_TYPE_RS232

if platform.system() == 'Linux':

    # for beaglebone
    SERIAL_PORT = "/dev/ttyUSB0"

elif platform.system() == 'Windows':

    # COM3 for WINDOWS --do com number minus 1. So COM3 == (3-1) == 2
    SERIAL_PORT = 2

# edit this for how often to check devices for data
DEVICE_POLL_INTERVAL_SECONDS = 1

# edit this for how long to wait before writing to the database
WAIT_FOR_INITIAL_BUFFER_SECONDS = 5

# edit this for how often to check devices for data
DATABASE_UPDATE_INTERVAL_SECONDS = 1

# edit this for how often to check devices for data
BUFFER_LEN_BEFORE_POP = 5

# used to identify the RF200 devices
Athlete_1_NetAddr = '\x5D\xE3\xAB'
Athlete_2_NetAddr = '\x5D\xE5\x10'
Athlete_3_NetAddr = '\x07\xA1\xDE'

Map_Athlete_Device_To_Address = {Athlete_1_NetAddr: 1,
                                 Athlete_2_NetAddr: 2,
                                 Athlete_3_NetAddr: 3}

DBNAME = 'ZotikonEventTSDB'
DBUSER = 'zotikon_writer'
DBUSR_PWD = 'write'

class BridgeVersionClient(object):
    """This class is used to connect to the snapstick sn200 and communicate with it"""

    def __init__(self, connected_to_beagle_bone, event):
        """set up initial things for the class such as functions, rpc functions, hooks, and opening the serial port"""

        # You can define what functions can be called remotely on your SNAPconnect instance
        # using the `funcs` argument
        funcs = {
            "get_data": self.get_data
        }

        # Create a SNAP instance
        self.comm = snap.Snap(funcs=funcs)

        # You can also define which functions can be called using `add_rpc_func`
        self.comm.add_rpc_func("update_device", self.update_device)

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

        self.connected_to_beagle_bone = connected_to_beagle_bone
        # global variable to buffer in a few seconds worth of data from the athlete worn devices
        self.buffer = [[], [], []]
        self.event_name = event

    def hook_open(self, serial_type, port, addr=None):
        """Once we open the serial port and have a connection start our random() calls at first interval and period"""

        if addr:
            self.bridge_address = addr
            self.log.info("Serial connection opened to %s", binascii.hexlify(addr))
            self.schedule_get_data_request_events_and_timeout()

        else:
            self.log.critical("Unable to open serial connection")

        return addr

    def hook_close(self, serial_type, port):
        """Let us know we are closing the serial port"""

        self.log.info("Serial connection closed")

    def get_data(self, athlete_addr):
        """This function makes a rpc call to the device specified by athlete_addr. It will get the heart rate and
        temperature from that device."""

        # send out actual command for the device to return the random() function
        self.comm.rpc(athlete_addr, 'callback', 'update_device', 'get_data_string')

        # necessary for schedular to not change our timeout period
        return True

    def update_device(self, heart_rate_and_temp):
        """This function is called when the rpc from get_data() is return from the device we pinged. We need to take
        the data that we are given and eventually write it to our database."""
        global Map_Athlete_Device_To_Address

        # get a single digit number based on the address of the device
        athlete_num = Map_Athlete_Device_To_Address[self.comm.rpcSourceAddr()]
        data_list = heart_rate_and_temp.split()

        running_total = 0
        i = 0
        print "data: ",
        while i < 10:
            print data_list[i] + " ",
            running_total += int(data_list[i])
            i += 1

        if running_total is 0:
            heart_rate = 0
        else:
            heart_rate = 60000 / (running_total / 10) - 5

        if heart_rate > 220:
            heart_rate = 0

        print "Athlete " + str(athlete_num) + ":        heartRate: " + str(heart_rate) + "\n"

        # update the buffer in the appropriate number for our data
        t = int(time.time())
        self.buffer[athlete_num - 1].append([str(athlete_num), str(heart_rate), str(data_list[1]), str(t)])

    def schedule_get_data_request_events_and_timeout(self):
        """This function creates the events on a certain time interval that allow us to send data back and forth
        to each device and to create a timer"""
        global DEVICE_POLL_INTERVAL_SECONDS, WAIT_FOR_INITIAL_BUFFER_SECONDS

        # make a get random call to each athlete device every random_interval seconds
        self.event1 = self.comm.scheduler.schedule(DEVICE_POLL_INTERVAL_SECONDS,
                                                   lambda: self.get_data(Athlete_1_NetAddr))
        self.event2 = self.comm.scheduler.schedule(DEVICE_POLL_INTERVAL_SECONDS,
                                                   lambda: self.get_data(Athlete_2_NetAddr))
        self.event3 = self.comm.scheduler.schedule(DEVICE_POLL_INTERVAL_SECONDS,
                                                   lambda: self.get_data(Athlete_3_NetAddr))

        # this timeout will let us collect data for the amount of seconds passed in before we update the database
        self.timeout = self.comm.scheduler.schedule(WAIT_FOR_INITIAL_BUFFER_SECONDS, self.start_update_database)

    def start_update_database(self):
        """This function will stop sending get random calls to each device and the timeout"""
        global DATABASE_UPDATE_INTERVAL_SECONDS

        self.timeout.Stop()
        self.update = self.comm.scheduler.schedule(DATABASE_UPDATE_INTERVAL_SECONDS, self.update_database)

    def update_database(self):
        """This function will write data to the database."""
        global USER, PWD, DBNAME, DBUSER, DBUSR_PWD, EVENT, WAIT_FOR_INITIAL_BUFFER_SECONDS, \
            DEVICE_POLL_INTERVAL_SECONDS

        # TODO insert logic get correct bpm and temp to write to data base for every device

        # only write to data base if we are connect to the beagle-bone
        # if self.connected_to_beagle_bone:
        #     client = InfluxDBClient(self.host, self.port, USER, PWD, DBNAME)
        #     client.switch_user(DBUSER, DBUSR_PWD)

        # self.print_buffer()

        # loop through our buffer and write off one of the data points if it is filled
        for athlete in self.buffer:
            while len(athlete) >= BUFFER_LEN_BEFORE_POP:

                # only write to data base if we are connect to the beagle-bone
                if self.connected_to_beagle_bone:
                    self.post(str(athlete[0][0]), str(athlete[0][1]), str(athlete[0][2]), str(athlete[0][3]))

                # remove the data entry we just wrote from the buffer
                athlete.pop(0)

        # self.print_buffer()

        # necessary for schedular to not change our timeout period
        return True

    def post(self, athNum, heartRate, temperature, time):
        """This function writes the data that was received from the athlete worn devices to the database."""

        body = self.event_name + ",playerId=" + athNum + " heartRate=" + heartRate + ",temperature=" + temperature + " " + time
        url = "http://192.168.7.2/influxdb/write"
        requests.post(url, data=body, params={"db": "ZotikonEventTSDB"}, headers={"Content-Type": "text/plain"})

    def print_buffer(self):
        """This function will display the buffer in a format that is easy to read."""

        count = 1
        for athlete in self.buffer:
            print "Length of Athlete " + str(count) + ": " + str(len(athlete))
            for update in athlete:
                print '{:<2} {:<5} {:<6} {}'.format(str(update[0]), str(update[1]), str(update[2]), str(update[3]))
            count += 1
        print

    def stop(self):
        """Stop the SNAPconnect instance and finish the test case."""
        self.timeout.Stop()
        self.event1.Stop()
        self.event2.Stop()
        self.event3.Stop()
        self.update.Stop()
        self.comm.close_all_serial()
        sys.exit(0)


def parse_args():
    """Parse the args."""

    parser = argparse.ArgumentParser(
        description='arguments used to connect from the synapse network to the beaglebone database')

    parser.add_argument('--event', type=str, required=False, default="Event_test",
                        help='chooses the event for the database')

    # if you don't include this argument it will be false, if you do include it it will be true
    parser.add_argument('--conbb', action='store_true', default=False,
                        help='Include this if you are connected to the beagle-bones'
                             ' wifi and want to write to the database')
    return parser.parse_args()


def main(connected_to_beagle_bone=False, event="Event_test"):
    """Instantiate a connection to the InfluxDB."""

    # Configure Python's built-in logging module to display any info or higher level messages
    logging.basicConfig(level=logging.INFO)

    # Instantiate a client instance
    client = BridgeVersionClient(connected_to_beagle_bone, event)

    # Start the SNAPconnect loop, nothing can happen after this point
    client.comm.loop()


if __name__ == "__main__":
    args = parse_args()
    main(connected_to_beagle_bone=args.conbb, event=args.event)

