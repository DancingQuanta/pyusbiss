#! /usr/bin/env python
# Serial.py partt of usbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

# Geert de Haan 10-3-2019

# Transmit : max 30 Bytes 
# Receive  : max 62 Bytes
# Process : 1 - send Transmit command ( optional with bytes to send)
#           2 - response : ACK or NACK - TxCount - RxCount if RxCount > 0 [RxData 1 .. RxData n ]
# loosely based on pyserial
# close() – This will close the serial port
# readline() – This will read a string from the serial port
# serial_read(size) – This will read n number of bytes from the serial port
# serial_write(data) – This will write the data passed to the function to the serial port
# in_waiting – This variable holds the number of bytes in the buffer
# out waiting - Number of bytes in the out buffer
# USBISS - FIFO - this means that every byte that is read is immediately removed from the
# USBISS buffer, this implies that even in_waiting and out_waiting can only be used once 
# immediately followed by reading the available bytes in the buffer. 
# This is solved by using an own readbuffer that holds all received character


"""Serial support for USB-ISS"""

# from usbiss import usbiss
import time

class SERIAL(object):


    SERIAL_IO   = 0x62 # response ACK (oxFF) or NACK (0x00) - Check on received characters | ACK | TxCount | RxCount
    SERIAL      = 0x01

    def __init__(self, usbissdev, baudrate):
        
        divisor = {
        300		:[0x27,	0x0F],
        1200	:[0x09,	0xC3],
        2400	:[0x04,	0xE1],
        9600	:[0x01,	0x37],
        19200	:[0x00,	0x9B],
        38400	:[0x00,	0x4D],
        57600	:[0x00,	0x33],
        115200	:[0x00,	0x19],
        250000	:[0x00,	0x0B],
        1000000	:[0x00,	0x03]         
        }
        try:
            brhb = divisor[baudrate][0]
            brlb = divisor[baudrate][1]
        except KeyError:
            raise ValueError('Serial - unknown baudrate;  possible values : (300, 1200, 2400 .. 1000000')

        self._usbiss = usbissdev
        self._usbiss.mode = [ self.SERIAL, brhb, brlb, 0b10101010] #Configure all I/O as input by default.
        # ReadBuffer for all incoming characters from the usbiss. All read methodes use this buffer for actual reading the received chars.
        self.buffer=[]
        # Allow the device time to setup
        time.sleep(1)

    def write(self, data):
        # usbiss write function
        self._usbiss.write_data(data)
        
    def read(self, size):
        # usbiss read function
        ret  = self._usbiss.read_data(size)
        return ret

    def close(self):
        self._usbiss.close()

    def decode(self,data):
        dec = self._usbiss.decode(data)
        return dec

    def _GetResponseFrame(self):
        """
        # Read the first three status bytes
        # from the buffer
        # Ack / Nack - rxcount - txcount
        """
        self.write([self.SERIAL_IO])
        time.sleep(.1)
        resp  = self.read(3)
        [ack, txcount, rxcount] = self.decode(resp)
        if ack != 0xFF:
            raise ValueError('Serial - GetResponseFrame - NACK received - Transmissionerror')
        if rxcount > 0:
            time.sleep(.01)
            com = self._serial_read(rxcount)
            #Add to buffer
            self.buffer += com
        return [ack, txcount, len(self.buffer)]

    def serial_write(self, data):
        """
        serial_write
        parameter : string of data to be send over 
        The transmitbuffer is 30 bytes long. if the data
        is longer than 30 the string is send in multple
        blocks.
        """
        writebuffer = list(map(ord, data))
        while(True):
            while(True): 
                # wait unit there are no more characters to send in the USBISS buffer
                outw = self.out_waiting
                if outw > 0:
                    time.sleep(0.5)
                else:
                    break
            if len(writebuffer) == 0:
                return
            # transmitbuffer of max 30 chars
            transmitbuffer = writebuffer[:30]
            writebuffer= writebuffer[30:]
            self._usbiss.write_data([self.SERIAL_IO]+transmitbuffer)
            time.sleep(1)


    def _serial_read(self, size):
        """
        _serial_read - bytes read are no longer available for consequtive
        reads - (FIFO) - For internal use only !
        """
        self.write([self.SERIAL_IO])
        resp  = self.read(size)
        data = self.decode(resp)
        return data
    
    def serial_read(self, size):
        """
        serial_read - return and remove bytes from the readbuffer.
        """
        line=''
        # How many chars in the buffer
        actualsize = len(self.buffer)
        # maximal the avialable chars
        if size > actualsize:
            size = actualsize
        linebuf = self.buffer[:size]
        self.buffer = self.buffer[size:]
        for c in linebuf:
            line += chr(c)
        return line

    def readline(self):
        """
        readline - all data that is available is added to self.buffer. after each read from the
        serial port self.buffer is checked for newlines. If found the function returns the string 
        up until the first newline.
        Subsequently calling readline() will produce the next bufferd lines. 
        """
        while(True):
            rxcount = self.in_waiting 
            if rxcount > 0: 
                for pos, i in enumerate(self.buffer):
                    # look for the \n
                    if i == 10: 
                        line=''
                        linebuf = self.buffer[:pos]
                        self.buffer = self.buffer[pos+1:]
                        for c in linebuf:
                            line += chr(c)
                        return line


    @property
    def in_waiting(self):
        """
        Get the number of bytes in the input buffer.
        """
        [ack, txcount, rxcount] = self._GetResponseFrame()
        return rxcount

    @property
    def out_waiting(self):
        """
        Get the number of bytes in the output buffer
        """
        [ack, txcount, rxcount] = self._GetResponseFrame()
        return txcount


