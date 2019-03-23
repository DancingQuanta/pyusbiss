#! /usr/bin/env python
# Copyright (c) 2019 Geert de Haan <geertwdehaan@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from usbiss import i2c


Port = 'COM3'
se95Address = 150

#SE95 registers

TEMP    = 0x00  #  2 8-bit data byes to store the measured temp
CONF    = 0x01  # Configuration register: containes a single 9-bit data byte to set an operating condition
THYST   = 0x02  # Hysteresis register: contains two 8-bit data bytes; to store the hysteris limit; bit 7 to bit 0 are also used in OTP test mode to supply OTP write data; default = 75 C
TOS     = 0x03  # Overtemperature shutdown threshold register: contains two8-bit data bytes; to store the overtemperature shutdown limit; default Tos =- 80 C
NU      = 0x04  # Not used
ID      = 0x05  # identification register: contains a single 8-bit data byte for the manufacturer ID code

class SE95(object):

    def __init__(self, i2cchannel, addr ):
        self._se95 = i2c.I2CDevice(i2cchannel, addr)
        

    def GetTemp(self):
        temp = self._se95.readS16BE(TEMP)
        return(temp)

    def GetID(self):
        id = self._se95.readU8(ID)
        return(id)

    def getConf(self):
        conf = self._se95.readU8(CONF)
        return(conf)

    def getAllReg(self):
        AllReg=self._se95.readList(TEMP, 5)
        return(AllReg)


if __name__ == '__main__':
    i2cchannel = i2c.I2C(Port, 'H', 100)
    se95 = SE95(i2cchannel, se95Address)
    AllReg = se95.getAllReg()
    print(AllReg)
    id = se95.GetID()
    temp = se95.GetTemp()
    conf = se95.getConf()
    print('ID = %i' % id)
    print('Temp = %i' % temp)
    print('Conf = %i' % conf)