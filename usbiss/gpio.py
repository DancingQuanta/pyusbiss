# gpio.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""GPIO support for USB-ISS"""

from usbiss import USBISS


class GPIO(object):
    """GPIO operating mode of USBISS
    """


    IO_MODE = 0x00
    IO_CHANGE = 0x10
    IO_SETPINS_CMD = 0x63
    IO_GETPINS_CMD = 0x64
    IO_GETAD_CMD = 0x65
    # Pin mode (IO_TYPE)
    OUT  = 0b00
    OUTH = 0b01
    IN   = 0b10
    ADC  = 0b11

    HIGH=1
    LOW=0


    def __init__(self, port):
        # Default Configure USB-ISS as IO all pins as input to protect the
        # external circuit and the USBISS from damage.
        self.ControlRegister = 0b10101010 # All inputs
        self.DataRegister = 0x00
        self._usbiss = USBISS(port)

        self._usbiss.set_iss_mode([self.IO_MODE, self.ControlRegister])


    def open(self):
        self._usbiss.open()


    def close(self):
        self._usbiss.close()


    def configure(self):
        """
        Configure GPIO controller
        """
        self._usbiss.set_iss_mode([self.IO_CHANGE, self.ControlRegister])


    def setup(self, pin, mode):
        """
        Configure Pin
        """
        # print('setup - before', format(self.ControlRegister, '08b'))
        for i in range(0, 2):
            if mode & 1 << i:
                self.ControlRegister |= 1 << (pin -1) * 2 + i
            else:
                self.ControlRegister &= ~(1 << (pin - 1) *2 + i)
        # print('setup - after', format(self.ControlRegister, '08b'))
        self.configure()


    def output(self, pin, level):
        """
        """
        if level:
            self.DataRegister |= 1 << (pin-1)
        else:
            self.DataRegister &= ~(1 << (pin - 1))
        self._usbiss.write_data([self.IO_SETPINS_CMD, self.DataRegister])


    def input(self, pin):
        """
        """
        self._usbiss.write_data([self.IO_GETPINS_CMD])
        self.DataRegister = self._usbiss.read_data(1)
        # print('input ', format(self.DataRegister, '08b'))
        return(self.DataRegister & 1 << (pin -1) !=0)
