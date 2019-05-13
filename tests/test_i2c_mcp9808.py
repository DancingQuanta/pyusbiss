#! /usr/bin/env python
# test_i2c_eprom_functions.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Copyright (c) 2019 Geert de Haan <geertwdehaan@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 1-3-2019
Testing the I2C module functions for reading an MCP9808

Hardware :
24LC256 Eprom connected to the USBISS () (no pullup R's)
Address : 180 ((A0..A2) grounded)
"""

import sys
import unittest
from usbiss import i2c

Port = 'COM3'
Address = 0
class I2ctestCase(unittest.TestCase):
    """ I2C driver EPROM functions testcase """

    def setUp(self):
        self.i2cchannel = i2c.I2C(Port, 'H', 100)
        print(self.i2cchannel._usbiss.__repr__)
        self.mcp9808 = i2c.I2CDevice(self.i2cchannel, Address)

    def tearDown(self):
        self.i2cchannel.close()

    def test1_devicepresent(self):
        self.assertEqual(self.mcp9808.ping(), True, 'Device not found at i2c Address : %s' % Address)



if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()