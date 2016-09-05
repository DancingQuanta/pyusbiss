
"""
Python interface to USB-ISS Multifunction USB Communications Module.
The technical specification can be found here:
    https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm

Some of the code is derived from: https://github.com/waggle-sensor/waggle/
"""

import serial
import struct

__author__ = 'Andrew Tolmie'
__email__ = 'andytheseeker@gmail.com'
__version__ = '0.1.0'

def iss_spi_divisor(sck):
    divisor = (6000000 / sck) - 1

    if int(divisor) != divisor:
        raise ValueError('Nonintegral SCK divisor.')

    return int(divisor)


class USBISS(object):

    def __init__(self, port, mode, **kwargs):
        self.mode = mode
        self.dummy_bytes = kwargs.get('dummy_bytes', 0)

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

        if self.mode == 'spi':
            clk_phase = kwargs.get('clk_phase', 0)
            if 0 <= clk_phase < 4:
                clk_phase = 0x90 + clk_phase
            else:
                error = ("The value of clk_phase, %s, is not "
                         "between 0 and 3" % (clk_phase))
                raise ValueError(error)
            if 'freq' in kwargs:
                freq = kwargs.get('freq')
                sck_divisor = iss_spi_divisor(freq)
                if not 1 <= sck_divisor < 256:
                    error = "The value of sck_divisor, %s, is not between 0 and 255" % (sck_divisor)
                    raise ValueError(error)
            else:
                raise TypeError("Missing argument for frequency for SPI mode")
            self.mode = 1
            set_bytes = [clk_phase, sck_divisor]
            msg = ("Initializing USB-ISS in SPI mode with %s clk_phase and %s "
                   "sck_divisor" % (clk_phase, sck_divisor))
            print(msg)

        # Configure USB-ISS
        self.set_iss_mode(set_bytes)

    def get_iss_info(self):
        """ Get information about the USB-ISS
        Querying will return three bytes;
            - the module ID (7),
            - firmware version (currently 2),
            - the current operating mode.
        """
        self.serial.write(bytearray([0x5A, 0x01]))
        response = struct.unpack('BBB', self.serial.read(3))
        if len(response) == 3:
            mod_id = "The module ID is %s" % (response[0])
            firmware = "The firmware version is %s" % (hex(response[1]))
            mode = "The current operating mode is %s" % (hex(response[2]))
            msg = mod_id + "\n" + firmware + "\n" + mode
            print(msg)
        else:
            raise RuntimeError("Could not get version details")


    def get_iss_serial_no(self):
        """ Get serial number of USB-ISS module
        """
        self.serial.write(bytearray([0x5A, 0x03]))
        # Return 8 bytes serial number
        response = self.serial.read(8)
        msg = "The serial number is %s" % (response)
        print(msg)


    def set_iss_mode(self, set_bytes):
        self.serial.write(bytearray([0x5A, 0x02] + set_bytes))
        response = self.serial.read(2)
        if response[0] == 0:
            if response[1] == 0x05:
                raise RuntimeError('USB-ISS: Unknown Command')
            elif response[1] == 0x06:
                raise RuntimeError('USB-ISS: Internal Error 1')
            elif response[1] == 0x07:
                raise RuntimeError('USB-ISS: Internal Error 2')
            else:
                raise RuntimeError('USB-ISS: Undocumented Error')


    def xfer(self, data):
        self.serial.write(bytearray([0x61] + data))
        response = self.serial.read(1 + len(data))
        status = response[0]
        if status == 0:
            raise RuntimeError('USB-ISS: Transmission Error')
        decoded = [struct.unpack('B', response[i+1])[0] for i in range(0, len(data))]
        return decoded
