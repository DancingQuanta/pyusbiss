# IO - Based on Vlieland Brainwave
#

# gpio.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# GdH - based on FT232H.py library from Adafruit for the FT232 (FTDI)

"""I2C support for USB-ISS"""

from usbiss import USBISS


class I2C(object):
    """I2C operating mode of USBISS
    I2C_S_20KHZ     0x20
    I2C_S_50KHZ     0x30
    I2C_S_100KHZ    0x40 
    I2C_S_400KHZ    0x50 
    I2C_H_100KHZ    0x60
    I2C_H_400KHZ    0x70
    I2C_H_1000KHZ   0x80
    """
    I2C_S_50KHZ  = 0x30
    I2C_S_100KHZ = 0x40 
    I2C_H_100KHZ = 0x60
    IO_TYPE = 0x04
    I2C_TEST = 0x58



    def __init__(self, port, handshaking, speed):
        """
        ToDo : 
        handshaking : Hardware of Software
        Speed Software : 20, 50, 100, 400
        Speed Hardware : 100, 400, 10000
        24-12-18 - POC -->  with Hardware 100Khz --> I2C_H_100KHZ
        """
        self._usbiss = USBISS(port)
        self._usbiss.set_iss_mode([self.I2C_H_100KHZ, self.IO_TYPE])


    def open(self):
        #Doel?
        self._usbiss.open()


    def close(self):
        #Doel?
        self._usbiss.close()




    def scan(self):
        """
        Scan the bus for I2C devices. Returns a list of devices
        max 127 devices per bus
        I2C_TEST - Adress
        0x58 - devAdr
        A single byte is returned, zero if no device is detected or non-zero if the device was detected.
         """
        response=[]
        for devadr in range(127): # ToDo : Check range.
            self._usbiss.write_data([self.I2C_TEST, devadr])
            resp = self._usbiss.read_data(1)
            resp = self._usbiss.decode(resp)
            if resp != [0]:
                response.append(devadr)
        return response
        #ToDo : convert to : List Comprehension
        # ToDo : Check if we need to wait 500mS for a response and otherwise raise an error.

    # GdH 5-1-2019 - is dit een goede oplossing ? ToDo !
    def write_data(self, data):
        self._usbiss.write_data(data)
        
    def read_data(self, size):
        ret  = self._usbiss.read_data(size)
        return ret

    def decode(self,data):
        dec = self._usbiss.decode(data)
        return dec




        


    

