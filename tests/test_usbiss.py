#! /usr/bin/env python
# test_i2c_registers_mcp23008.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Copyright (c) 2019 Geert de Haan <geertwdehaan@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 3-3-2019
Testing usbiss.py module

Hardware :

USBISS
"""
#USBISS Commands
ISS_CMD         =   0x5A
ISS_MODE        =   0x02

#USBISS Operating modes
IO_MODE         =   0x00
IO_CHANGE       =   0x10
I2C_S_20KHZ     =   0x20
I2C_S_50KHZ     =   0x30
I2C_S_100KHZ    =   0x40 
I2C_S_400KHZ    =   0x50 
I2C_H_100KHZ    =   0x60
I2C_H_400KHZ    =   0x70
I2C_H_1000KHZ   =   0x80
SPI_MODE        =   0x90
SERIAL          =   0x01
# IO_MODE : Pinsettings
IO_TYPE         =   0x04
# Test incorrect mode
INCORRECT_MODE  =   0xAA
# query for serial, firmware and mode
ISS_VERSION     = 0x01

import sys
import unittest
from usbiss import usbiss



#USBISS parameter
Port = 'COM3'

# TODO : check the real mode instead of the getter. (3-3-2019)

class I2ctestCase(unittest.TestCase):
    """ I2C driver register functions testcase """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1_basicfunctionality(self):
        self.assertIsNotNone(usbiss.USBISS(Port))

    def test2_check_iomode(self):
        _usbiss = usbiss.USBISS(Port)
        _usbiss.mode = [IO_MODE]
        curmod = _usbiss.mode
        self.assertEqual([IO_MODE], curmod)
 
    def test_operating_modes(self):
        _usbiss = usbiss.USBISS(Port)
        for opmode in [IO_MODE, IO_CHANGE, I2C_S_20KHZ]:
            with self.subTest(opmode = [opmode]):
                _usbiss.mode = [opmode]
                curmod = _usbiss.mode
                self.assertEqual([opmode], curmod)

    def test_incorrect_operating_mode(self):
        _usbiss = usbiss.USBISS(Port)
        _usbiss.mode = [INCORRECT_MODE]
        curmod = _usbiss.mode
        self.assertEqual([INCORRECT_MODE], curmod)

    def test_latest_firmware(self):
        latest_firmware = 0x08
        _usbiss = usbiss.USBISS(Port)
        _usbiss.write_data([ISS_CMD, ISS_VERSION])
        response = _usbiss.read_data(3)
        response = _usbiss.decode(response)
        # module = response[0]
        firmware = response[1]
        # mode = response[2]
        self.assertEqual(firmware, latest_firmware, 'Latest version = %i' % latest_firmware)

if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()