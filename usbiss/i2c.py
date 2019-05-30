# I2C.py - part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# GdH - based on FT232H.py library from Adafruit for the FT232 (FTDI)

"""I2C support for USB-ISS"""


import time


class I2C(object):
    """I2C operating mode of USBISS"""
    I2C_S_20KHZ    = 0x20
    I2C_S_50KHZ    = 0x30
    I2C_S_100KHZ   = 0x40 
    I2C_S_400KHZ   = 0x50 
    I2C_H_100KHZ   = 0x60
    I2C_H_400KHZ   = 0x70
    I2C_H_1000KHZ  = 0x80
    IO_TYPE        = 0x04
    I2C_TEST       = 0x58



    def __init__(self, usbissdev, handshaking, speed):
        """

        """
        if handshaking not in ('H', 'S'):
            ValueError ('I2C - Handshaking is (H)ardware or (S)oftware/ not %s' % str(handshaking))

        key = str(handshaking)+str(speed)
        OperatingModes = {'H100':self.I2C_H_100KHZ, 
                          'H400':self.I2C_H_400KHZ, 
                          'H1000':self.I2C_H_1000KHZ,
                          'S20':self.I2C_S_20KHZ, 
                          'S50':self.I2C_S_50KHZ, 
                          'S100':self.I2C_S_100KHZ, 
                          'S400':self.I2C_S_400KHZ
                        }
        try:
            setting = OperatingModes[key]
        except KeyError:
            raise ValueError('I2C - This combination of handshaking and speed is not supported : ' + str(handshaking)  + ' '+ str(speed)) 

        self._usbiss = usbissdev
        self._usbiss.mode = [setting, self.IO_TYPE]



    def scan(self):
        """
        Scan the bus for I2C devices. Returns a list of devices
        max 127 devices per bus
        A single byte is returned, zero if no device is detected or non-zero if the device was detected.
         """
        response=[]
        for devadr in range(255): # ToDo : Check range.
            self.write_data([self.I2C_TEST, devadr])
            resp = self.read_data(1)
            resp = self.decode(resp)
            if resp != [0]:
                response.append(devadr)
        return response

    # GdH 5-1-2019 
    def write_data(self, data):
        self._usbiss.write_data(data)
        
    def read_data(self, size):
        ret  = self._usbiss.read_data(size)
        return ret

    def decode(self,data):
        dec = self._usbiss.decode(data)
        return dec




    # I2CDevice
    # 30-12-2018
    # Class for individual I2CDevices using the I2C driver for the USBISS




class I2CDevice(object):
    """
    """
    I2C_SGL    = 0x53 # Read/Write single byte for non-registered devices, such as the Philips PCF8574 I/O chip.
    I2C_AD0    = 0x54 # Read/Write multiple bytes for devices without internal address or where address does not require resetting.
    I2C_AD1    = 0x55 # Read/Write 1 byte addressed devices (the majority of devices will use this one)
    I2C_AD2    = 0x56 # Read/Write 2 byte addressed devices, eeproms from 32kbit (4kx8) and up. 
    I2C_DIRECT = 0x57 # Used to build your own custom I2C sequences.
    I2C_TEST   = 0x58 # Used to check for the existence of an I2C device on the bus. (V5 or later firmware only)

    def __init__(self, usbissdevice, addr):

        self._usbissi2c = usbissdevice
        self._addr      = addr # 8 bits Address !
        self._addr_read = addr + 1
    
    def ping(self):
            """
            ping the Device, returns True the device is available at the specified Address
            """
            self._usbissi2c.write_data([self.I2C_TEST, self._addr])
            resp = self._usbissi2c.read_data(1)
            resp = self._usbissi2c.decode(resp)
            if resp != [0]:
                response = True
            else:    
                response = False
            return response

    def readRaw8(self):
        """
        Read single byte for non-registered devices, such as the Philips PCF8574 I/O chip.
         """

        self._usbissi2c.write_data([self.I2C_SGL, self._addr_read]) 
        # time.sleep(0.1)
        resp = self._usbissi2c.read_data(1) # Reads 1 byte / 8 bits
        resp = self._usbissi2c.decode(resp)
        if len(resp) > 0:
            return resp[0]
        else: 
            return resp

    def writeRaw8(self, value):
        """
        value : 1 byte to write

        Write single byte for non-registered devices, such as the Philips PCF8574 I/O chip.
        """
        # Write is op het basisadres
        value = value & 0xFF
        self._usbissi2c.write_data([self.I2C_SGL, self._addr, value])
        resp = self._usbissi2c.read_data(1)
        resp = self._usbissi2c.decode(resp)
        if resp != [1]:
            raise RuntimeError("I2CDevice - writeRaw8 - TransmissionError")

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        self._usbissi2c.write_data([self.I2C_AD1, self._addr_read, register, 1]) 
        resp = self._usbissi2c.read_data(1) # Reads 1 byte / 8 bits
        resp = self._usbissi2c.decode(resp)
        if len(resp) > 0:
            return resp[0]
        else: 
            return resp

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        result = self.readU8(register)
        if result > 127:
            result -= 256
        return result

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        self._usbissi2c.write_data([self.I2C_AD1, self._addr, register, 1 , value])
        resp = self._usbissi2c.read_data(1)
        resp = self._usbissi2c.decode(resp)
        if resp != [1]:
            raise RuntimeError("I2CDevice - write8 - TransmissionError")

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        self._usbissi2c.write_data([self.I2C_AD1, self._addr_read, register, 2]) 
        resp = self._usbissi2c.read_data(2) # Reads 1 byte / 8 bits
        resp = self._usbissi2c.decode(resp)
        if little_endian:
            return (resp[-1] << 8) | resp[-2]
        else:
            return (resp[-2] << 8) | resp[-1]


    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = self.readU16(register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    def write16(self, register, value,  little_endian=True):
        """Write a 16-bit value to the specified register."""
        value = value & 0xFFFF
        value_low  = value & 0xFF
        value_high = (value >> 8) & 0xFF
        if little_endian:
            value = [value_low, value_high]
        else:
            value = [value_high, value_low]

        self._usbissi2c.write_data([self.I2C_AD1, self._addr, register, 2 ]+value)
        resp = self._usbissi2c.read_data(1)
        resp = self._usbissi2c.decode(resp)
        if resp != [1]:
            raise RuntimeError("I2CDevice - write16 - TransmissionError")
    
    def readList(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        self._usbissi2c.write_data([self.I2C_AD1, self._addr_read, register, length]) 
        resp = self._usbissi2c.read_data(length)
        resp = self._usbissi2c.decode(resp)
        if len(resp) > 0:
            return resp
        else: 
            return resp

    def writeList(self, register, data):
        """Write bytes to the specified register."""
        # Data is a bytearray
        length = len(data)
        self._usbissi2c.write_data([self.I2C_AD1, self._addr, register, length] + data)
        # ToDo check op data, concatenaten van de list tot een reeks getallen ? Testen !!!
        resp = self._usbissi2c.read_data(1)
        resp = self._usbissi2c.decode(resp)
        if resp != [1]:
            raise RuntimeError("I2CDevice - writeList - TransmissionError")


    def readU16LE(self, register):
        """Read an unsigned 16-bit value from the specified register, in little
        endian byte order."""
        return self.readU16(register, little_endian=True)

    def readU16BE(self, register):
        """Read an unsigned 16-bit value from the specified register, in big
        endian byte order."""
        return self.readU16(register, little_endian=False)

    def readS16LE(self, register):
        """Read a signed 16-bit value from the specified register, in little
        endian byte order."""
        return self.readS16(register, little_endian=True)

    def readS16BE(self, register):
        """Read a signed 16-bit value from the specified register, in big
        endian byte order."""
        return self.readS16(register, little_endian=False)

    # These functions (writeMem, readMem) are not part of the Adafruit protocol library. Specific for the USBISS device


    def readMem(self, AddressHighByte, AddressLowByte, length):
        """
        AddressHighByte, AddressLowByte : Address of the memory location within the EPROM.
        lenght                        : no of bytes to receive

        Read 2 byte addressed devices, eeproms from 32kbit (4kx8) and up.
        The maximum number of data bytes requested should not exceed 64 so as not to overflow the USB-ISS's internal buffer.
        """
        if length > 64:
            raise ValueError("I2CDevice - readMem - max 64 bytes exceeded.")

        self._usbissi2c.write_data([self.I2C_AD2, self._addr_read, AddressHighByte, AddressLowByte, length]) 

        resp = self._usbissi2c.read_data(length)
        resp = self._usbissi2c.decode(resp)
        return resp

    def writeMem(self, AddressHighByte, AddressLowByte, length, data):
        """
        AddressHighByte, AddressLowByte : Address of the memory location within the EPROM.
        lenght                        : length of the transmitted data
        data                          : bytearray of data

        Write 2 byte addressed devices, eeproms from 32kbit (4kx8) and up. 
        The maximum number of data bytes should not exceed 59 so as not to overflow the USB-ISS's 64 byte internal buffer.
        """
        if length > 59:
            raise ValueError("I2CDevice - writeMem - max 59 bytes exceeded.")
        
        self._usbissi2c.write_data([self.I2C_AD2, self._addr, AddressHighByte, AddressLowByte, length] + data) 

        # Avoid transmission errors.
        time.sleep(0.05)

        resp = self._usbissi2c.read_data(1)
        resp = self._usbissi2c.decode(resp)
        if resp != [1]:
            raise RuntimeError("I2CDevice - writeList - TransmissionError - " + str(AddressHighByte) + '-' + str(AddressLowByte)) 

    

