# usbiss.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Python interface to USB-ISS Multifunction USB Communications Module.
The technical specification can be found here:
    https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm

Some of the code is derived from: https://github.com/waggle-sensor/waggle/
"""

import struct
import serial


class USBISSError(IOError):
    """Base class error for all USB-ISS devices"""


class USBISS(object):
    """Base class for USB-ISS.
    The main purpose of the base class is to manage serial connection between
    the host and USB-ISS.

    The base class will be the parent class of child classes that manages a
    connection between USB-ISS and a device. A child class will set the
    connection protocol and mimic the methods and properties of usual
    interface libraries. The mimicry will allows an instance of a child class
    to be used without any modification of the application using the instance.
    This is because the application expect the methods or properties of an
    library used to facilitate an connection.
    """

    # USBISS identification and configuration
    module = None
    firmware = None
    _mode = None
    serial = None

    # USBISS command bytes
    ISS_CMD = 0X5A
    ISS_VERSION = 0x01
    ISS_SET_MODE = 0x02
    ISS_SER_NUM = 0x03

    # SPI command bytes
    SPI_MODE = 0x90
    SPI_CMD = 0x61

    def __init__(self, port):

        # Open serial port
        serial_opts = {"port": port,
                       "baudrate": 9600,
                       "parity": serial.PARITY_NONE,
                       "bytesize": serial.EIGHTBITS,
                       "stopbits": serial.STOPBITS_ONE,
                       "xonxoff": False,
                       "timeout": 1}
        self.serial = serial.Serial(**serial_opts)

        self.get_iss_info()
        self.get_iss_serial_no()

    def open(self):
        """Open Serial port to USB-ISS
        """
        self.serial.open()

    def close(self):
        """Close Serial port to USB-ISS
        """
        self.serial.close()

    def write_data(self, data):
        """
        Write to USB-ISS
        """
        self.serial.write(bytearray(data))

    def read_data(self, size):
        """
        Read from USB-ISS
        """
        return self.serial.read(size)

    def decode(self, data):
        decoded = []
        for i in range(0, len(data)):
            unpacked = struct.unpack('B', data[i: i + 1])[0]
            decoded = decoded + [unpacked]
        return decoded

    def get_iss_info(self):
        """ Get information about the USB-ISS
        Querying will return three bytes;
            - the module ID (7),
            - firmware version (currently 2),
            - the current operating mode.
        """
        self.write_data([self.ISS_CMD, self.ISS_VERSION])
        response = self.read_data(3)
        if len(response) == 3:
            response = self.decode(response)
            self.module = response[0]
            self.firmware = response[1]
            self._mode = response[2]
        else:
            raise USBISSError("Could not get version details")

    def get_iss_serial_no(self):
        """ Get serial number of USB-ISS module
        """
        self.write_data([self.ISS_CMD, self.ISS_SER_NUM])
        # Return 8 bytes serial number
        self.iss_sn = self.read_data(8)

    @property
    def mode(self):
        """
        The configuration byte of USB-ISS that controls the operating protocol
        and its additional parameters.

        :getter: A configuration byte
        :setter: The configuration byte
        :type: int (0xnn)
        """
        return self._mode

    @mode.setter
    def mode(self, set_bytes):
        """Set the operating protocol of the USB-ISS with additional
        parameters for the  protocol
        """
        self._mode = set_bytes
        data = [self.ISS_CMD, self.ISS_SET_MODE] + set_bytes
        self.write_data(data)
        response = self.read_data(2)
        if response[0] == 0:
            error_dict = {
                0x05: 'Unknown Command',
                0x06: 'Internal Error 1',
                0x07: 'Internal Error 2'
            }
            try:
                raise USBISSError(error_dict[response(1)])
            except KeyError:
                raise USBISSError('Undocumented Error')

    def __repr__(self):
        return ("The module ID is {}\n"
                "The firmware version is {}\n"
                "The current operating mode is {}\n"
                "The serial number is {}").format(
                    self.module, self.firmware, self._mode, self.iss_sn
                )
