import time
import sys
import unittest
from usbiss import i2c

Port = 'COM3'
Address = 120

class I2CBoard_PCF8574A():
    """ I2C driver no register functions testcase """

    def __init__(self):
        self.i2cchannel = i2c.I2C(Port, 'H', 100)
        self.pcf8574 = i2c.I2CDevice(self.i2cchannel, Address)
        # P0 - P3 Inputpins
        # P4 - P7 Outputpins
        self.IODIR = 0x0F


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



def main():
    pcf8574 = I2CBoard_PCF8574A()
    pcf8574._SetPinOn(7)
    # pcf8574._SetPinOff(7)




if __name__ == '__main__':
    main()