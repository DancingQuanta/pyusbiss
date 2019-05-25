#! /usr/bin/env python
# test_i2c_eprom_functions.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 1-3-2019
Testing the I2C module functions for reading and writing an EPROM

Hardware :
24LC256 Eprom connected to the USBISS () (no pullup R's)
Address : 160 ((A0..A2) grounded)
"""

import sys
import unittest
from usbiss import usbiss
from usbiss import i2c

Port = 'COM3'
EpromAddress = 160
class I2ctestCase(unittest.TestCase):
    """ I2C driver EPROM functions testcase """

    def setUp(self):
        self._usbissdev = usbiss.USBISS(Port)
        self.i2cchannel = i2c.I2C(self._usbissdev, 'H', 100)
        print(self.i2cchannel._usbiss.__repr__)
        self.eprom = i2c.I2CDevice(self.i2cchannel, EpromAddress)

    def tearDown(self):
        self._usbissdev.close()

    def test1_devicepresent(self):
        self.assertEqual(self.eprom.ping(), True, 'Device not found at i2c Address : %s' % EpromAddress)


    def _writepattern(self):
        pat1 = [0x0f]
        pat2= [0xf0]
        self.writebuf=[]
        for high_Address in range(1):
            for low_Address in range(255):
                if low_Address % 2 == 1:
                    data = pat1
                else:
                    data = pat2
                self.eprom.writeMem(high_Address, low_Address, len(data), data)
                self.writebuf.append(data)

    def _readpattern(self):

        self.readbuf=[]
        for high_Address in range(1):
            for low_Address in range(255):
                data = self.eprom.readMem(high_Address, low_Address, 1)
                self.readbuf.append(data)

    def test2_write_read(self):
        """
        Write a pattern to Eprom, read it back and compare.
        """
        self._writepattern()
        self._readpattern()
        self.assertListEqual(self.writebuf, self.readbuf)


if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()