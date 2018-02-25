
"""
Python interface to USB-ISS Multifunction USB Communications Module.
The technical specification can be found here:
    https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm

Some of the code is derived from: https://github.com/waggle-sensor/waggle/
"""

import struct
import serial

__author__ = 'Andrew Tolmie'
__email__ = 'andytheseeker@gmail.com'
__version__ = '0.1.2'


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

    module = None
    firmware = None
    iss_mode = None
    cur_iss_mode = None
    serial = None

    ISS_CMD = 0X5A
    ISS_VERSION = 0x01
    ISS_MODE = 0x02
    ISS_SER_NUM = 0x03


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


    def iss_write(self, data):
        """
        Write to USB-ISS
        """
        self.serial.write(bytearray(data))


    def iss_read(self, size):
        """
        Read from USB-ISS
        """
        return self.serial.read(size)


    def decode(self, data):
        decoded = []
        for i in range(0, len(data)):
            unpacked = struct.unpack('B', data[i + 1: i + 2])[0]
            decoded = decoded + [unpacked]
        return decoded


    def get_iss_info(self):
        """ Get information about the USB-ISS
        Querying will return three bytes;
            - the module ID (7),
            - firmware version (currently 2),
            - the current operating mode.
        """
        self.iss_write([self.ISS_CMD, self.ISS_VERSION])
        response = self.iss_read(3)
        if len(response) == 3:
            response = self.decode(response)
            self.module = response[0]
            self.firmware = hex(response[1])
            self.cur_iss_mode = hex(response[2])
        else:
            raise RuntimeError("Could not get version details")


    def get_iss_serial_no(self):
        """ Get serial number of USB-ISS module
        """
        self.iss_write([self.ISS_CMD, self.ISS_SER_NUM])
        # Return 8 bytes serial number
        self.iss_sn = self.iss_read(8)


    def set_iss_mode(self, set_bytes):
        """Set the operating protocol of the USB-ISS
        """
        data = [self.ISS_CMD, self.ISS_MODE] + set_bytes
        self.iss_write(data)
        response = self.iss_read(2)
        if response[0] == 0:
            if response[1] == 0x05:
                raise RuntimeError('USB-ISS: Unknown Command')
            elif response[1] == 0x06:
                raise RuntimeError('USB-ISS: Internal Error 1')
            elif response[1] == 0x07:
                raise RuntimeError('USB-ISS: Internal Error 2')
            else:
                raise RuntimeError('USB-ISS: Undocumented Error')


    def __repr__(self):
        return ("The module ID is {}\n"
                "The firmware version is {}\n"
                "The current operating mode is {}\n"
                "The serial number is {}").format(
                    self.module, self.firmware, self.cur_iss_mode, self.iss_sn
                )
