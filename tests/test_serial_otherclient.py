#! /usr/bin/env python
# test_i2c.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Created by Geert de Haan
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 19-4-2019
Testing the serial module with client serial program.

Hardware : Connect the Rx  (pin 2) and Tx (pin 3) with an external FTDI device 
(usbiss.Rx --> FTDI.Tx, usbiss.Tx --> FTDI.Rx) and start the 
tests\SerialClient.py program in a separate DosBox (python SerialClient.py)

"""

import sys
import time
import unittest
from usbiss import usbiss
from usbiss import serial

Port = 'COM3'
Baudrate = 9600

class I2ctestCase(unittest.TestCase):


    def setUp(self):
        self._usbissdev = usbiss.USBISS(Port)
        self.serport = serial.SERIAL(self._usbissdev, Baudrate)

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


if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()