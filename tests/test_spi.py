#! /usr/bin/env python
# test_spi.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""
Some tests for the SPI protocol controlled by USB-ISS.

Intended to be run on different platforms, to ensure portability of the code.

For all these tests a simple hardware is required.
Shortcut these pin pairs:
    IO2 <-> IO4

This script can be ran with a port identifier as an argument.
"""

import unittest
import sys
from usbiss import spi

# on which port should the tests be performed:
# TODO: Cycle through available ports and attempt connection.
# TODO: Dinguish between platforms.
PORT = 'COM4'

# indirection via bytearray b/c bytes(range(256)) does something else in Pyhton 2.7
bytes_0to255 = list(bytes(bytearray(range(256))))


def segments(data, size=16):
    for a in range(0, len(data), size):
        yield data[a:a + size]


class SpiTestCase(unittest.TestCase):
    """SPI driver test case"""

    def setUp(self):
        self.cxn = spi.SPI(PORT)

    def tearDown(self):
        self.cxn.close()

    def test0_modes(self):
        """
        Test SPI modes
        """
        for i in range(3):
            self.cxn.mode = i
            self.assertEqual(self.cxn.mode, i, "expected a {} which was written before".format(i))
            lookup_table = [0, 2, 1, 3]
            self.cxn._usbiss.get_iss_info()
            usbiss_mode = self.cxn._usbiss.mode - self.cxn._usbiss.SPI_MODE
            self.assertEqual(usbiss_mode, lookup_table[i], "expected a {} which was written before".format(lookup_table[i]))

    def test1_loopback(self):
        """
        Loopback test
        """
        for block in segments(bytes_0to255):
            self.assertEqual(self.cxn.xfer(block), block, "expected a {} which was written before".format(block))


if __name__ == '__main__':
    sys.stdout.write(__doc__)
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    sys.stdout.write("Testing port: {!r}\n".format(PORT))
    sys.argv[1:] = ['-v']
    # When this module is executed from the command-line, it runs all its tests
    unittest.main()
