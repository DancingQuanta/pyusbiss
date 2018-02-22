
"""
Python interface to USB-ISS Multifunction USB Communications Module.
The technical specification can be found here:
    https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm

Some of the code is derived from: https://github.com/waggle-sensor/waggle/

GdH - pip install pyserial
"""
#
import struct
import serial


__author__ = 'Andrew Tolmie'
__email__ = 'andytheseeker@gmail.com'
__version__ = '0.1.0'

def iss_spi_divisor(sck):
    divisor = (6000000 / sck) - 1

    if int(divisor) != divisor:
        raise ValueError('Nonintegral SCK divisor.')

    return int(divisor)


class USBISS(object):
    '''
    '''
    pinfunction = [] # I/O mode : PinFunction (adc, OutputL, OutputH, input)
    pinstatus = 0x00   # I/O mode : pinstatus for input and output status
    Vcc = 4.9        # USB-ISS Operating voltage

    def __init__(self, port, iss_mode, **kwargs):
        self.iss_mode = iss_mode

        # Open serial port
        serial_opts = {"port": port,
                       "baudrate": 9600,
                       "parity": serial.PARITY_NONE,
                       "bytesize": serial.EIGHTBITS,
                       "stopbits": serial.STOPBITS_ONE,
                       "xonxoff": False,
                       "timeout": 1}
        self.serial = serial.Serial(**serial_opts)

        self.get_iss_info()
        self.get_iss_serial_no()

        if self.iss_mode == 'spi':
            # Select the SPI mode of USB-ISS's SPI operating mode
            if 'spi_mode' in kwargs:
                spi_mode = kwargs.get('spi_mode', 0)
                if 0 <= spi_mode < 4:
                    # Expose the the SPI mode to external applications
                    # where self.mode is same as spidev.SpiDev.mode
                    if spi_mode == 0:
                        self.mode = 0
                    elif spi_mode == 1:
                        self.mode = 2
                    elif spi_mode == 2:
                        self.mode = 1
                    elif spi_mode == 3:
                        self.mode = 3
                    # Add signal for SPI switch
                    spi_mode = 0x90 + spi_mode
                else:
                    error = ("The value of spi_mode, %s, is not "
                             "between 0 and 3" % (spi_mode))
                    raise ValueError(error)
            else:
                raise TypeError("Missing argument for spi_mode for SPI"
                                "operating mode")
            # Select frequency of USB-ISS's SPI operating mode
            if 'freq' in kwargs:
                freq = kwargs.get('freq')
                sck_divisor = iss_spi_divisor(freq)
                if not 1 <= sck_divisor < 256:
                    error = "The value of sck_divisor, %s, is not between 0 and 255" % (sck_divisor)
                    raise ValueError(error)
            else:
                raise TypeError("Missing argument for frequency for SPI"
                                "operating mode")
            set_bytes = [spi_mode, sck_divisor]
            msg = ("Initializing USB-ISS in SPI mode with %s spi_mode and %s "
                   "sck_divisor" % (spi_mode, sck_divisor))
            print(msg)
            
            self.set_iss_mode(set_bytes)
        # GdH - Add the io mode
        #
        # Format : USB = USBISS(port, 'io', pin1 = 'outputL', pin2 = 'outputH', pin3 = 'input', pin4 = 'adc')
        # ToDo - 27-1-18 - Add an option to indicate the operating voltage for the ADC

        if self.iss_mode == 'io':
            io_type = 0x00000000 # Default all outputL
            # Dict maps type to USBISS controlbyte
            io_types={"input" : 0b10, "outputL" : 0b00, "outputH" : 0b01, "adc" : 0b11}
            # check mode for each pin
            for i in range(1,5):
                searchpin='pin'+str(i)
                if searchpin in kwargs:
                    io_mode = kwargs.get(searchpin)
                    if io_mode == 'outputH':
                        self.SetPinOn(i)
                    io_pinbits = io_types[io_mode]
                    #ToDo
                    io_type = io_type +  io_pinbits * (2**((i-1)*2))
            # IO_MODE for I/O = 0x00
            # IO_TYPE = settings for individual pins
            set_bytes = [0x00, io_type]
            msg = ("Initializing USB-ISS in I/O mode with IO_TYPE %s" % bin(io_type))
            print(msg)
        #
        # Configure USB-ISS, set_bytes is set based on mode
        self.set_iss_mode(set_bytes)

    def open(self):
        """Open Serial port to USB-ISS
        """
        self.serial.open()

    def close(self):
        """Close Serial port to USB-ISS
        """
        self.serial.close()

    def get_iss_info(self):
        """ Get information about the USB-ISS
        Querying will return three bytes;
            - the module ID (7),
            - firmware version (currently 2),
            - the current operating mode.
        """
        self.serial.write(bytearray([0x5A, 0x01]))
        response = struct.unpack('BBB', self.serial.read(3))
        if len(response) == 3:
            mod_id = "The module ID is %s" % (response[0])
            firmware = "The firmware version is %s" % (hex(response[1]))
            mode = "The current operating mode is %s" % (hex(response[2]))
            msg = mod_id + "\n" + firmware + "\n" + mode
            print(msg)
        else:
            raise RuntimeError("Could not get version details")


    def get_iss_serial_no(self):
        """ Get serial number of USB-ISS module
        """
        self.serial.write(bytearray([0x5A, 0x03]))
        # Return 8 bytes serial number
        response = self.serial.read(8)
        msg = "The serial number is %s" % (response)
        print(msg)


    def set_iss_mode(self, set_bytes):
        self.serial.write(bytearray([0x5A, 0x02] + set_bytes))
        response = self.serial.read(2)
        if response[0] == 0:
            if response[1] == 0x05:
                raise RuntimeError('USB-ISS: Unknown Command')
            elif response[1] == 0x06:
                raise RuntimeError('USB-ISS: Internal Error 1')
            elif response[1] == 0x07:
                raise RuntimeError('USB-ISS: Internal Error 2')
            else:
                raise RuntimeError('USB-ISS: Undocumented Error')


    def xfer(self, data):
        # spidev function for transferring bytes to port
        self.serial.write(bytearray([0x61] + data))
        response = self.serial.read(1 + len(data))
        if len(response) != 0:
            status = response[0]
            if status == 0:
                raise RuntimeError('USB-ISS: Transmission Error')

            decoded = [struct.unpack('B', response[i + 1: i + 2])[0] for i in range(0, len(data))]
            
            return decoded
        else:
            raise RuntimeError('USB-ISS: Transmission Error: No bytes received!')

    def SetPinOn(self, pin):
        '''
        Set pin High
        0x63 - set pinstatus. returns 0xFF is succesfull, else 0x00
        '''
        mask = 1 << (pin-1)
        self.pinstatus = self.pinstatus | mask
        self.serial.write(bytearray([0x63] + [self.pinstatus]))
        response = self.serial.read(1)
        if response == 0:
            raise RuntimeError('USB-ISS: SetPinOn - Configuration error ')

    def SetPinOff(self, pin):
        '''
        Set pin Low
        0x63 - reset pinstatus. returns 0xFF is succesfull, exle 0x00
        '''
        mask = 0xFF
        mask = 0 << (pin - 1)
        self.pinstatus = self.pinstatus & mask
        self.serial.write(bytearray([0x63] + [self.pinstatus]))
        response = self.serial.read(1)
        if response == 0:
            raise RuntimeError('USB-ISS: SetPinOff - Configuration error ')

    def GetPin(self, pin):
        '''
        Get de pinstatus for inputpins. Output for all pins 
        in self.pinstatus
        This is used to get the current state of all digital I/O pins.
        Just send the single byte:
        GETPINS command (0x64)
        The response is a single byte indicating the Pin States as defined above.
        '''
        set_bytes = [0x64]
        self.serial.write(set_bytes)
        response = self.serial.read(1)
        self.pinstatus = response[0]
        # print("self.pinstatus", bin(self.pinstatus))
        mask = 1 << (pin-1)
        return(int(self.pinstatus) & mask != 0)

    def GetADC(self, pin):
        '''.
        The GetADC command will convert the requested channel (IO pin number)
        and return the two byte result. The result is the high byte and low byte
        of a 16 bit number.
        The A/D conversion is a 10-bit conversion so the range is 0-1023 for a voltage
        swing of Vss to Vcc on the pin.
        '''
        set_bytes=[0x65, pin]
        self.serial.write(bytearray(set_bytes))
        response = self.serial.read(2)
        print(self.Vcc/1024)
        print(response)
        rcalc =(255*response[0])+response[1]
        return(self.Vcc/1024*rcalc)


# GdH - SPI mode - Andrew Tolmie
# t=USBISS('COM3', 'spi',spi_mode = 1, freq = 25000)
#p=t.xfer([0x45])
#print(type(p))
#for a in p:
#    print(a)
'''
# GdH - I/O mode - Geert de Haan Test
'''
# Init Test
# t=USBISS('COM3',  "io", pin1="outputL", pin2="outputH", pin3="input", pin4="adc")
# t.SetPinOn(1)
#t.SetPinOff(2)
#
# Testing 1 - 
#
# All pins as OutputL
# t=USBISS('COM3',  "io", pin1="outputL", pin2="outputL", pin3="outputL", pin4="outputL")
# pin switching as fast as possible
# while True:
#    t.SetPinOn(2)
#    t.SetPinOff(2)
#
# Results - 2,9Khz (2,4 KHz - 3 KHz), 4,32 V
# Jitter is immense
# Testing 2 -
#
# All Pin 1 as Input, Pin2 has a Led connected
# t=USBISS('COM3',  "io", pin1="input", pin2="outputL", pin3="outputL", pin4="outputL")
# while True:
#    inp = t.GetPin(1)
#    if inp:
#        t.SetPinOn(2)
#    else:
#        t.SetPinOff(2)
#
# Testing 3 - 
#
# Closed loop - Pin as Output connected to input, controls output
# Check timing with scope
#
# Testing 4 - Check on Timing stability
#
# Create a puls with a fixed time
# Check timingdelta's with Picoscope and DS1054Z
#
# Test 5 - ADC
# 
# Determine max aquisition frequency
#
# Test 6 - ADC Accuracy
#
# Supply reference voltages - Check conversionresult
t=USBISS('COM3',  "io", pin1="input", pin2="outputL", pin3="adc", pin4="outputL")

Voltage = t.GetADC(3)
print('Voltage = ', Voltage)