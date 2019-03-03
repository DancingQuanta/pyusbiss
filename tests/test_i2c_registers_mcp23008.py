#! /usr/bin/env python
# test_i2c_registers_mcp23008.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Copyright (c) 2019 Geert de Haan <geertwdehaan@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 1-3-2019
Testing the I2C module functions for devices with registers. 

Hardware :
MCP23008 IO Expander connected to the USBISS () (no pullup R's)
Address : 64 ((A0..A2) grounded)
"""

import sys
import unittest
from usbiss import i2c

# MCP23008 Registers

IODIR   = 0x00  # IO Direction
IPOL    = 0x01  # Input polarity
GPINTEN = 0x02  # Interrupt on Change
DEFVAL  = 0x03  # Default Compare (for interrupt)
INTCON  = 0x04  # Interrupt Control
IOCON   = 0x05  # Configuration register for MCP23008
GPPU    = 0x06  # Pull-up register configuration
INTF    = 0x07  # Interrupt Flag Register
INTCAP  = 0x08  # Interrupt Capture Register
GPIO    = 0x09  # Port (GPIO) Register - Write - modifies Output latch (OLAT)
OLAT    = 0x0A  # Output latch register

#USBISS parameter
Port = 'COM3'
# I2C parameters
Handshaking ='H'
Speed = 100
# MCP23008 Adress
McpAddress = 64
class I2ctestCase(unittest.TestCase):
    """ I2C driver register functions testcase """

    def _write8read8(self, data):
        """
        helper function for testing the 8 bit register functions
        """
        writebyte = data
        register = IODIR
        self.mcp23008.write8(register, writebyte)
        readbyte = self.mcp23008.readU8(register)
        if readbyte == writebyte:
            return True
        else:
            return False

    def setUp(self):
        self.i2cchannel = i2c.I2C(Port, 'H', 100)
        print(self.i2cchannel._usbiss.__repr__)
        self.mcp23008 = i2c.I2CDevice(self.i2cchannel, McpAddress)

    def tearDown(self):
        self.i2cchannel.close()

    def test1_i2device_ping(self):
        self.assertEqual(self.mcp23008.ping(), True, 'Device not found at i2c Address : %s' % McpAddress)

    # test the write8 and read8 function by writing to a MCP23008 register
    # and reading back the register and comparing the result.
    def test2_i2device_write8(self):
        self.assertTrue(self._write8read8(0b01010101))


 



if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()