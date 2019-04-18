#! /usr/bin/env python
# test_i2c.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Copyright (c) 2019 Geert de Haan <geertwdehaan@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Geert de Haan / 17-4-2019
Testing the serial module in loopback mode

Hardware : Connect the Rx  (pin 2) and Tx (pin 3). 
Due to the fact that the outgoing buffer is only 30 bytes this is also the maximum string length 
possible in loopback mode.
"""

import sys
import time
import unittest
from usbiss import serial

Port = 'COM3'
Baudrate = 9600

class I2ctestCase(unittest.TestCase):


    def setUp(self):
        self.serport = serial.SERIAL(Port, Baudrate)

    def tearDown(self):
        self.serport.close()

    def test1_loopback_readline(self):
        send = 'Test1 - Loopbacktest\n'
        self.serport.serial_write(send)
        time.sleep(.5) # give USBISS time to send the string
        receive = self.serport.readline()
        self.assertEqual(receive +'\n', send)

    def test2_loopback_read_serial(self):
        send = 'Test2 - Loopbacktest\n'
        self.serport.serial_write(send)
        time.sleep(1)
        # waiting = connection.in_waiting
        waiting = self.serport.in_waiting
        if waiting==0:
            self.assertEqual('Error' , 'Nothing to receive')
        else:
            time.sleep(.1)
            resp = self.serport.serial_read(waiting)
            receive = ''.join(map(chr, resp))
            self.assertEqual(receive , send)


if __name__ == '__main__':
    sys.stdout.write(__doc__)
    unittest.main()