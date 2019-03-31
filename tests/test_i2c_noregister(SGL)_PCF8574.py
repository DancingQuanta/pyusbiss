#! /usr/bin/env python
# test_i2c.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Copyright (c) 2019 Geert de Haan <geertwdehaan@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 9-3-2019
Testing the I2C module : USBISS - I2C_SGL command - 
Read/Write single byte for non-registered devices, such as the Philips PCF8574 I/O chip.


Hardware : Testboard met PCF8574, pin 7 connected to pin 0 for loopbacktest
"""
import time
import sys
import unittest
from usbiss import i2c

Port = 'COM3'
Address = 120

class I2CTestCaseSGL_noregister(unittest.TestCase):
    """ I2C driver no register functions testcase """
    I2C_TEST       = 0x58

    def _SetPinOn(self, pin):
        data = self.pcf8574.readRaw8() 
        data |= 1 << (pin)
        data |= self.IODIR
        self.pcf8574.writeRaw8(data)

    def _SetPinOff(self, pin):
        data = self.pcf8574.readRaw8() 
        data &= ~(1 << (pin))
        data |= self.IODIR
        self.pcf8574.writeRaw8(data)

    def _GetPin(self, pin):
        data = data = self.pcf8574.readRaw8() 
        data &= (1 << (pin))
        data  = data >> (pin)
        return data

    def setUp(self):
        self.i2cchannel = i2c.I2C(Port, 'H', 100)
        self.assertIsInstance(self.i2cchannel, i2c.I2C)
        # print(self.i2cchannel._usbiss.__repr__)
        self.pcf8574 = i2c.I2CDevice(self.i2cchannel, Address)
        self.assertIsInstance(self.pcf8574, i2c.I2CDevice)
        self.IODIR = 0x0F

    def tearDown(self):
        self.i2cchannel.close()

    def test1_devicepresent(self):
        # time.sleep(1)
        # resp = self.pcf8574.ping()
        self.i2cchannel.write_data([self.I2C_TEST, Address])
        time.sleep(1)
        resp = self.i2cchannel.read_data(1)
        resp = self.i2cchannel.decode(resp)
        if resp != [0]:
            response = True
        else:    
            response = False
        self.assertEqual(response, True, 'Device not found at i2c Address : %s' % Address)


    def test2_i2cdevice_loopback(self):
        time.sleep(1)
        OUTPUTPIN = 7
        INPUTPIN  = 0
        ON = 1
        OFF = 0
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