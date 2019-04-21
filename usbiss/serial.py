# Serial.py partt of usbiss
# Geert de Haan 10-3-2019

# Transmit : max 30 Bytes 
# Receive  : max 62 Bytes
# Process : 1 - send Transmit command ( optional with bytes to send)
#           2 - response : ACK or NACK - TxCount - RxCount if RxCount > 0 [RxData 1 .. RxData n ]
# loosely based on pyserial
# open() – This will open the serial port
# close() – This will close the serial port
# readline() – This will read a string from the serial port
# read(size) – This will read n number of bytes from the serial port
# write(data) – This will write the data passed to the function to the serial port
# in_waiting – This variable holds the number of bytes in the buffer
# out waiting - Number of bytes in the out buffer


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
        self.buffer=[] # Buffer for readline method
        print('DEBUG SERIAL, init ready')

        time.sleep(1)

    def write(self, data):
        self._usbiss.write_data(data)
        
    def read(self, size):
        ret  = self._usbiss.read_data(size)
        return ret

    def close(self):
        self._usbiss.close()

    def decode(self,data):
        dec = self._usbiss.decode(data)
        return dec

    def _GetResponseFrame(self):
        self.write([self.SERIAL_IO])
        time.sleep(.1)
        resp  = self.read(3)
        frame = self.decode(resp)
        return frame

    def serial_write(self, data):
        """
        serial_write
        parameter : string of data to be send over 
        """
        buffer = list(map(ord, data))
        n = 0
        while(True):
            while(True): 
                # wait unit there are no more characters to send in the USBISS buffer
                outw = self.out_waiting
                n+=1
                if outw > 0:
                    time.sleep(0.5)
                    print(str(n), str(outw))
                else:
                    break
            if len(buffer) == 0:
                return
            transmitbuffer = buffer[:30]
            buffer= buffer[30:]
            self._usbiss.write_data([self.SERIAL_IO]+transmitbuffer)
            time.sleep(2) #9600 baud
        #    if len(buffer) == 0:
        #        if n == 1:
        #            outw = self.out_waiting # Necessary to "clean" the controlblock. otherwise in_waiting
        #            print('serial_write - out_waiting fired off', str(outw))
        #        return

    def serial_read(self, size):
        """
        Read the buffer, always read the full buffer
        """
        self.write([self.SERIAL_IO])
        #time.sleep(1)
        resp  = self.read(size)
        data = self.decode(resp)
        return data
    
    def readline(self):
        # buffer =[]
        n = 0 # No of reads

        while(True):
            rxcount = self.in_waiting 
            if rxcount > 0:
                time.sleep(.01)
                com = self.serial_read(rxcount)
                n += 1
                #Add to buffer
                self.buffer += com
            for pos, i in enumerate(self.buffer):
                    #print(chr(i), end='')
                if i == 10: 
                    line=''
                    linebuf = self.buffer[:pos]
                    self.buffer = self.buffer[pos+1:]
                    for c in linebuf:
                        line += chr(c)
                    #return line + ' ' +str(n) + '- ' + str(len(self.buffer))          
                    return line
                    # return line



    @property
    def in_waiting(self):
        """
        Get the number of bytes in the input buffer
        """
        [ack, txcount, rxcount] = self._GetResponseFrame()
        print(rxcount, txcount)
        if ack != 0xFF:
            raise ValueError('Serial - Read - NACK - Transmissionerror')
        return rxcount

    @property
    def out_waiting(self):
        """
        Get the number of bytes in the output buffer
        """
        [ack, txcount, rxcount] = self._GetResponseFrame()
        return txcount


