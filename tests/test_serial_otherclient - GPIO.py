#! /usr/bin/env python
# test_i2c.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Created by Geert de Haan
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 19-4-2019
Testing the serial module with client serial program / combined with GPIO features of the USBISS

Hardware : Connect the Rx  (pin 2) and Tx (pin 3) with an external FTDI device 
(usbiss.Rx --> FTDI.Tx, usbiss.Tx --> FTDI.Rx) and start the 
tests\SerialClient.py program in a separate DosBox (python SerialClient.py)

This test demonstrates that the usbiss can use both the serial and gpio at the same time.
"""

import sys
import time
import unittest
from usbiss import usbiss
from usbiss import serial
from usbiss import gpio

Port = 'COM3'
Baudrate = 9600

class I2ctestCase(unittest.TestCase):


    def setUp(self):
        self._usbissdev = usbiss.USBISS(Port)
        #initialize the serial port
        self.serport = serial.SERIAL(self._usbissdev, Baudrate)
        # Initialize the GPIO, only pins 3 and 4 are available in combined witrh serial mode
        self.io2 = gpio.GPIO(self._usbissdev, gpio.SERIAL)
        # Configure Pin3 as Out, Pin4 as IN, set Pin3 as Low
        self.io2.setup_pins({3:gpio.OUT, 4: gpio.IN}, {3:gpio.LOW})
        self.assertIsInstance(self.io2, gpio.GPIO)

    def tearDown(self):
        self._usbissdev.close()

    def test1_loopback_readline(self):
        #testing the
        send = 'Test1 - Loopbacktest max 60 chars, the USBISS inputbuffer\n'
        self.serport.serial_write(send)
        time.sleep(.5) # give USBISS time to send the string
        receive = self.serport.readline()
        self.assertEqual(receive +'\n', send)

    def test2_loopback_read_serial(self):
        send = 'Test2 - Loopbacktest with a longer string then 30 chars\n'
        self.serport.serial_write(send)
        time.sleep(.5)
        #waiting for the data to come back. USBISS
        n = 0
        waiting = 0
        while(n<5 and waiting == 0):
            waiting = self.serport.in_waiting
            n+=1
            time.sleep(.5)
        if waiting==0:
            self.assertEqual('Error' , 'Nothing to receive')
        else:
            time.sleep(.1)
            receive = self.serport.serial_read(waiting)
            self.assertEqual(receive , send)

    def test3_loopback_gpio(self):
        # set pin 3 HIGH, check result on pin 4
        # set pin 3 LOW, check result on pin 4
        pi = 4
        po = 3
        self.io2.output(po, gpio.HIGH)
        pin4val = self.io2.input(pi)
        self.assertEqual(pin4val, gpio.HIGH)   
        self.io2.output(po, gpio.LOW)
        pin4val = self.io2.input(pi)
        self.assertEqual(pin4val, gpio.LOW)

if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()