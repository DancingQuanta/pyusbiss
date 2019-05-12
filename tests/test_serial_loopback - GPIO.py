#! /usr/bin/env python
# test_serial_loop - GPIO.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 5-5-2019
Testing the serial module in loopback mode / combined with GPIO features of the USBISS

Hardware : Connect the Rx  (pin 1) and Tx (pin 2) of the USBISS
           Connect the IO3 and IO4 for the GPIO loopback test.
            
Due to the fact that the outgoing buffer is only 30 bytes long this is also the maximum string length 
possible in loopback mode.
For tests longer than 30 chars see the test_serial_otherclient.py 

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
        #initialize the serial port
        _usbissdev = usbiss.USBISS(Port)
        # Initialize the GPIO, only pins 3 and 4 are available if combined with serial mode
        self.serport = serial.SERIAL(_usbissdev, Baudrate)
        self.io2 = gpio.GPIO(_usbissdev, gpio.SERIAL)
        self.io2.setup_pins({3:gpio.OUT, 4: gpio.IN}, {3:gpio.LOW})
        self.assertIsInstance(self.io2, gpio.GPIO)

    def tearDown(self):
        self.serport.close()
        #closed ook de _usbiss in de Serial driver

    def test1_loopback_readline(self):
        """
        Test serial functionality by sending a string out and
        reading it back with readline()
        """
        send = 'Test1 - Loopbacktest\n'
        self.serport.serial_write(send)
        time.sleep(.5) # give USBISS time to send the string
        receive = self.serport.readline()
        self.assertEqual(receive +'\n', send)

    def test2_loopback_read_serial(self):
        """
        Test basic functionality by using serial_read() en serial_write()
        """
        send = 'Test2 - Loopbacktest\n'
        self.serport.serial_write(send)
        time.sleep(1)
        # waiting = connection.in_waiting
        waiting = self.serport.in_waiting
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