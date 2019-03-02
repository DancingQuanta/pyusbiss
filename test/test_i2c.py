#! /usr/bin/env python
# test_i2c.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Copyright (c) 2019 Geert de Haan <geertwdehaan@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 2-3-2019
Testing the I2C module 

Hardware : for the scantest (test 14) the USBISS should be connected to a I2C bus with at least one device for a succesfull test
"""

import sys
import unittest
from usbiss import i2c

Port = 'COM3'
McpAddress = 160
class I2ctestCase(unittest.TestCase):
    """ I2C driver register functions testcase """

    def _scan_devices(self):
        i2cchannel = i2c.I2C(Port, 'H', 100)
        return(i2cchannel.scan())

    def setUp(self):
        pass

    def tearDown(self):
        pass 

    def test1_parameters_H(self):
        self.assertIsNotNone(i2c.I2C(Port, 'H', 100))

    def test2_parameters_H(self):
        self.assertIsNotNone(i2c.I2C(Port, 'S', 100))

    def test3_parameters_handshaking_invalid(self):
        with self.assertRaises(ValueError):
            i2c.I2C(Port, 'P', 100)

    def test4_parameters_Hardware_100khz(self):
        self.assertIsNotNone(i2c.I2C(Port, 'H', 100))

    def test5_parameters_Hardware_400khz(self):
        self.assertIsNotNone(i2c.I2C(Port, 'H', 400))

    def test6_parameters_Hardware_1000khz(self):
        self.assertIsNotNone(i2c.I2C(Port, 'H', 1000))
 
    def test7_parameters_Software_20khz(self):
        self.assertIsNotNone(i2c.I2C(Port, 'S', 20))

    def test8_parameters_Software_50khz(self):
        self.assertIsNotNone(i2c.I2C(Port, 'S', 50))

    def test9_parameters_Software_100khz(self):
        self.assertIsNotNone(i2c.I2C(Port, 'S', 100))

    def test10_parameters_Software_400khz(self):
        self.assertIsNotNone(i2c.I2C(Port, 'S', 400))

    def test11_parameters_Software_20khz(self):
        self.assertIsNotNone(i2c.I2C(Port, 'S', 20))

    def test12_parameters_Hardware_invalidspeed(self):
        with self.assertRaises(ValueError):
            i2c.I2C(Port, 'H', 50)

    def test13_parameters_Hardware_invalidspeed(self):
        with self.assertRaises(ValueError):
            i2c.I2C(Port, 'S', 1000)

    def test14_scan_i2c_devices(self):
        self.assertNotEqual(len(self._scan_devices()), 0, "I2C Scan : no devices found")
        print(self._scan_devices())

if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()