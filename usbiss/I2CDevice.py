# I2CDevice
# 30-12-2018
# Class for individual I2CDevices using the I2C driver for the USBISS
import time



class I2CDevice(object):

    I2C_SGL    = 0x53 # Read/Write single byte for non-registered devices, such as the Philips PCF8574 I/O chip.
    I2C_AD0    = 0x54 # Read/Write multiple bytes for devices without internal address or where address does not require resetting.
    I2C_AD1    = 0x55 # Read/Write 1 byte addressed devices (the majority of devices will use this one)
    I2C_AD2    = 0x56 # Read/Write 2 byte addressed devices, eeproms from 32kbit (4kx8) and up. 
    I2C_DIRECT = 0x57 # Used to build your own custom I2C sequences.
    I2C_TEST   = 0x58 # Used to check for the existence of an I2C device on the bus. (V5 or later firmware only)

    def __init__(self, usbissdevice, addr):
        """
        ToDo : 
        handshaking : Hardware of Software
        Speed Software : 20, 50, 100, 400
        Speed Hardware : 100, 400, 10000
        24-12-18 - POC -->  with Hardware 100Khz --> I2C_H_100KHZ
        """

        
        self._usbissi2c = usbissdevice
        self._addr    = addr # 8 bits adress !
    
    def ping(self):
            self._usbissi2c.write_data([self.I2C_TEST, self._addr])
            resp = self._usbissi2c.read_data(1)
            resp = self._usbissi2c.decode(resp)
            if resp != [0]:
                response = True
            else:    
                response = False
            return response

    def _address_byte(self, read=True):
        """Return the address byte with the specified R/W bit set.  If read is
        True the R/W bit will be 1, otherwise the R/W bit will be 0.
        """

        if read:
            return (self._addr << 1) | 0x01
        else:
            return self._addr << 1

    def readRaw8(self):
        """
        Read single byte for non-registered devices, such as the Philips PCF8574 I/O chip.
        ADAFruit - Read an 8-bit value on the bus (without register).
        """

        readadr = self._addr+1
        # readadr = 0x41
        self._usbissi2c.write_data([self.I2C_SGL, readadr]) # ToDo - Readadress !
        # time.sleep(0.1)
        resp = self._usbissi2c.read_data(1) # Reads 1 byte / 8 bits
        resp = self._usbissi2c.decode(resp)
        return resp 
    
    def writeRaw8(self, value):
        """
        Write single byte for non-registered devices, such as the Philips PCF8574 I/O chip.
        """
        # Write is op het basisadres
        self._usbissi2c.write_data([self.I2C_SGL, self._addr, value])
        resp = self._usbissi2c.read_data(1)
        resp = self._usbissi2c.decode(resp)
        if resp == [0]:
            raise RuntimeError("I2CDevice - writeRaw8 - TransmissionError")

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""
        self._usbissi2c.write_data([self.I2C_AD1, self._addr, register, 1 , value])
        resp = self._usbissi2c.read_data(1)
        resp = self._usbissi2c.decode(resp)
        if resp == [0]:
            raise RuntimeError("I2CDevice - write8 - TransmissionError")

    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""
        self._usbissi2c.write_data([self.I2C_AD1, self._addr, register, 2 , value])
        resp = self._usbissi2c.read_data(1)
        resp = self._usbissi2c.decode(resp)
        if resp == [0]:
            raise RuntimeError("I2CDevice - write8 - TransmissionError")
        pass

    def writeList(self, register, data):
        """Write bytes to the specified register."""
        pass

    def readList(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        pass

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        pass

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        pass

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        pass

    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        pass

    def readU16LE(self, register):
        """Read an unsigned 16-bit value from the specified register, in little
        endian byte order."""
        pass

    def readU16BE(self, register):
        """Read an unsigned 16-bit value from the specified register, in big
        endian byte order."""
        pass

    def readS16LE(self, register):
        """Read a signed 16-bit value from the specified register, in little
        endian byte order."""
        pass

    def readS16BE(self, register):
        """Read a signed 16-bit value from the specified register, in big
        endian byte order."""
        pass
