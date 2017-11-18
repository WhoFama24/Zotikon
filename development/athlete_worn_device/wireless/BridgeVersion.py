"""BridgeVersion.py"""

import logging
import binascii
import sys

from snapconnect import snap


SERIAL_TYPE = snap.SERIAL_TYPE_RS232
SERIAL_PORT = 2  # COM3 for windows


class BridgeVersionClient(object):
    def __init__(self):
        self.bridge_address = None  # Set a default value for the bridge address
        self.bridge_version = "Unknown"  # Set a default value for the bridge version

        # You can define what functions can be called remotely on your SNAPconnect instance
        # using the `funcs` argument
        funcs = {
            "major_callback": self.major_callback,
            "minor_callback": self.minor_callback
        }

        # Create a SNAP instance
        self.comm = snap.Snap(funcs=funcs)

        # You can also define which functions can be called using `add_rpc_func`
        self.comm.add_rpc_func("patch_callback", self.patch_callback)

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
            self.get_version()
        else:
            self.log.critical("Unable to open serial connection")

        return addr

    def hook_close(self, serial_type, port):
        """Callback function invoked when a serial connection is closed."""
        self.log.info("Serial connection closed")

    def get_version(self):
        """Start the RPC chain to retrieve the bridge SNAPcore version."""
        self.comm.rpc(self.bridge_address, 'callback', 'major_callback', 'getInfo', 5)

    def major_callback(self, major_version):
        """Callback function invoked when the major version is returned from the bridge."""
        self.bridge_version = str(major_version) + "."
        self.comm.rpc(self.bridge_address, 'callback', 'minor_callback', 'getInfo', 6)

    def minor_callback(self, minor_version):
        """Callback function invoked when the minor version is returned from the bridge."""
        self.bridge_version += str(minor_version) + "."
        self.comm.rpc(self.bridge_address, 'callback', 'patch_callback', 'getInfo', 7)

    def patch_callback(self, patch_version):
        """Callback function invoked when the patch version is returned from the bridge."""
        self.bridge_version += str(patch_version)
        self.log.info("Bridge SNAPcore version: %s" % self.bridge_version)
        self.stop()

    def stop(self):
        """Stop the SNAPconnect instance."""
        self.comm.close_all_serial()  # Close all serial connections opened with SNAPconnect
        sys.exit(0)  # Exit the program


if __name__ == "__main__":
    # Configure Python's built-in logging module to display any info or higher level messages

    logging.basicConfig(level=logging.INFO)

    client = BridgeVersionClient()  # Instantiate a client instance

    # Start the SNAPconnect loop, nothing can happen after this point
    client.comm.loop()
