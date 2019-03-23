#! /usr/bin/env python
# test_gpio - part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 23-3-2019
Testing gpio module, part of pyusbiss

Hardware :

USBISS 
- Led on pin 1 (configured as output)
- Led on pin 2 (configured as output)
- pin 3 connected to pin 1 (configured as input)
- pin 4 connected to pin 2 (configured as input)
"""


import sys
import unittest
from usbiss import usbiss
from usbiss import gpio



#USBISS parameter
Port = 'COM3'



class GPIOtestCase(unittest.TestCase):
    """ GPIO functions testcase """

    def setUp(self):
        self._usbiss = usbiss.USBISS(Port)
        self.io4 = gpio.GPIO(self._usbiss)
        self.io4.setup_pins({1:gpio.OUT, 2:gpio.OUT, 3:gpio.IN, 4: gpio.IN}, {1:gpio.LOW, 2:gpio.LOW})
        self.assertIsInstance(self._usbiss, usbiss.USBISS)
        self.assertIsInstance(self.io4, gpio.GPIO)

    def tearDown(self):
        self._usbiss.close()

    def test1_loopback_pin1_pin3(self):
        # set pin 1 HIGH, check result on pin 3
        # set pin 1 LOW, check result on pin 3
        pi = 3
        po = 1
        self.io4.output(po, gpio.HIGH)
        pin3val = self.io4.input(pi)
        self.assertEqual(pin3val, gpio.HIGH)   
        self.io4.output(po, gpio.LOW)
        pin3val = self.io4.input(pi)
        self.assertEqual(pin3val, gpio.LOW)

    def test2_loopback_pin2_pin4(self):
        # set pin 2 HIGH, check result on pin 3
        # set pin 2 LOW, check result on pin 4       
        pi = 4
        po = 2
        self.io4.output(po, gpio.HIGH)
        pin4val = self.io4.input(pi)
        self.assertEqual(pin4val, gpio.HIGH)   
        self.io4.output(po, gpio.LOW)
        pin4val = self.io4.input(pi)
        self.assertEqual(pin4val, gpio.LOW)

    def test3_loopback_multipin(self):
        # set pin 1,2 HIGH, check result on pin 3,4
        # set pin 1,2 LOW, check result on pin 3,4
        self.io4.output_pins({1:gpio.HIGH, 2: gpio.HIGH})
        pinval = self.io4.input_pins([3,4])
        self.assertEqual(pinval, [gpio.HIGH, gpio.HIGH])
        self.io4.output_pins({1:gpio.LOW, 2: gpio.LOW})
        pinval = self.io4.input_pins([3,4])
        self.assertEqual(pinval, [gpio.LOW, gpio.LOW])


if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()