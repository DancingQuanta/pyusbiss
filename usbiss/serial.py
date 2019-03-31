# Serial.py partt of usbiss
# Geert de Haan 10-3-2019

# Transmit : max 30 Bytes 
# Receive  : max 62 Bytes
# Process : 1 - send Transmit command ( optional with bytes to send)
#           2 - response : ACK or NACK - TxCount - RxCount if RxCount > 0 [RxData 1 .. RxData n ]
# based on pyserial
# open() – This will open the serial port
# close() – This will close the serial port
# readline() – This will read a string from the serial port
# read(size) – This will read n number of bytes from the serial port
# write(data) – This will write the data passed to the function to the serial port
# in_waiting – This variable holds the number of bytes in the buffer


"""Serial support for USB-ISS"""

from usbiss import usbiss
import time

class SERIAL(object):


    SERIAL_IO   = 0x62 # response ACK (oxFF) or NACK (0x00) - Check on received characters | ACK | TxCount | RxCount
    SERIAL      = 0x01

    def __init__(self, port, baudrate):
        
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
            raise ValueError('Serial - unknown baudrate possible : (300, 1200, 2400 .. 1000000')

        self._usbiss = usbiss.USBISS(port)
        self._usbiss.mode = [ self.SERIAL, brhb, brlb, 0b10101010] #Configure I/O as input.

    def write(self, data):
        self._usbiss.write_data(data)
        
    def read(self, size):
        ret  = self._usbiss.read_data(size)
        return ret

    def readline(self):
        """
        read a string from the serial port
        """
        pass

    def decode(self,data):
        dec = self._usbiss.decode(data)
        return dec

    def _GetResponseFrame(self):
        self.write([self.SERIAL_IO])
        resp  = self.read(3)
        frame = self.decode(resp)
        return frame

    def serial_write(self, data):
        """
        """
        # Controleer out_waiting
        # Bereken ruimte
        # schrijf max ruimte weg
        # Haal blok van de data af 
        # alle data verzonden ?
        # Nee (Herhaal)
        # Ja Stop 
        self._usbiss.write_data([self.SERIAL_IO]+data)

    def serial_read(self, size):
        """
        """
        self.write([self.SERIAL_IO])
        resp  = self.read(size)
        data = self.decode(resp)
        return data
        

    @property
    def in_waiting(self):
        """
        Get the number of bytes in the input buffer
        """
        [ack, txcount, rxcount] = self._GetResponseFrame()
        return rxcount

    @property
    def out_waiting(self):
        """
        Get the number of bytes in the output buffer
        """
        [ack, txcount, rxcount] = self._GetResponseFrame(self)
        return txcount


