#! /usr/bin/env python
# test_i2c_registers_mcp23008.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Copyright (c) 2019 Geert de Haan <geertwdehaan@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 1-3-2019
Testing the I2C module functions for devices with registers. USBISS (I2C_AD1)

Hardware :
MCP23008 IO Expander connected to the USBISS () (no pullup R's)
Address : 64 ((A0..A2) grounded)
Test 6 - Connect pin 7 (output) with pin 6 (input) for the loopbacktest
"""

import sys
import time
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
Handshaking ='S'
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

    def _write16read16BE(self, data, little_endian):
        """
        helper function for testing the 16 bit register functions
        """
        write2bytes = data
        register = IODIR
     
        # Write the 2 bytes Big Endian
        self.mcp23008.write16(register, write2bytes, little_endian)
        readbytes = self.mcp23008.readU16(register, little_endian)
        if readbytes == write2bytes:
            return True
        else:
            return False

    def _writeListreadList(self, data):
        """
        helper function for testing the 16 writelist register functions
        """
        writebytesarray = data
        register = IODIR
     
        # Write the list of bytes to a register and read back the register content.
        self.mcp23008.writeList(register, writebytesarray)
        readbytesarray = self.mcp23008.readList(register, 3)
        if readbytesarray == writebytesarray:
            return True
        else:
            return False

    def _SetPinOn(self, pin):
        data = self.mcp23008.readU8(GPIO) 
        data |= 1 << (pin)
        self.mcp23008.write8(GPIO,data)

    def _SetPinOff(self, pin):
        data = self.mcp23008.readU8(GPIO) 
        data &= ~(1 << (pin))
        self.mcp23008.write8(GPIO, data)

    def _GetPin(self, pin):
        data = data = self.mcp23008.readU8(GPIO) 
        data &= (1 << (pin))
        data  = data >> (pin)
        return data

    def setUp(self):
        self.i2cchannel = i2c.I2C(Port, Handshaking, Speed)
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

    # test the write16 and read16 functions with big - and little Endian
    def test3_i2cdevice_write16_BE(self):
        self.assertTrue(self._write16read16BE(0xFF00, False))
    
    def test4_i2cdevice_write16_LE(self):
        self.assertTrue(self._write16read16BE(0xFF00, True))

    # test the writelist function by writing a list to the MCP23008 registers and reading it back
    def test5_i2cdevice_writelist(self):
        self.assertTrue(self._writeListreadList([0xFF, 0x00, 0xFF]))
 
    # test I2C module by writing to MCP23008 pin and reading back the result
    # Connect pin 7 (output) with pin 6 (input)
    def test6_i2cdevice_loopback(self):
        OUTPUTPIN = 7
        INPUTPIN  = 6
        ON = 1
        OFF = 0
        self.mcp23008.write8(IODIR, 0b01111111)
        # Set OUTPUTPIN off and check te result
        self._SetPinOff(OUTPUTPIN)
        pinstat = self._GetPin(INPUTPIN)
        self.assertEqual(pinstat, OFF)
        # Set OUTPUTPIN off and check te result
        self._SetPinOn(OUTPUTPIN)
        pinstat = self._GetPin(INPUTPIN)
        self.assertEqual(pinstat, ON)
        # if a LED is connected to the OUTPUTPIN.
        time.sleep(2)
        # Set OUTPUTPIN off and check te result
        self._SetPinOff(OUTPUTPIN)
        pinstat = self._GetPin(INPUTPIN)
        self.assertEqual(pinstat, OFF)



if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()