# gpio.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# GdH - based on FT232H.py library from Adafruit for the FT232 (FTDI)

"""GPIO support for USB-ISS"""



# GPIO Connection modes 
I2C     = 1
SERIAL  = 2
FULL    = 3
# Pin mode (IO_TYPE)
    
OUT  = 0b00
OUTH = 0b01
IN   = 0b10
ADC  = 0b11

LOW  = 0
HIGH = 1 


class GPIO(object):
    """GPIO operating mode of USBISS
       as GPIO is also used in combination with I2C and Serial
       this class does not open an connection to the USBISS itself, but is depending on a
       masterclass to supply the connection
    """

    # USBISS GPIO commands
    
    IO_MODE = 0x00
    IO_CHANGE = 0x10
    IO_SETPINS_CMD = 0x63
    IO_GETPINS_CMD = 0x64
    IO_GETAD_CMD = 0x65
    



    def __init__(self, usbiss_con, con_mode=FULL):
        # Default Configure USB-ISS as IO all pins as input to protect the
        # external circuit and the USBISS from damage.
        self.ControlRegister = 0b10101010 # All inputs
        self.DataRegister = 0x00
        self.con_mode = con_mode
        #if self.con_mode == FULL:
        #    self._usbiss = usbiss.USBISS(usbiss_con)
        #else:
        self._usbiss = usbiss_con 

        self.configure()


    def _check_pins_and_con_mode(self, pin):
        # check if this pin is not reserverd for I2C or SERIAL operation
        # in FULL mode all pins (1-4) can be changed
        if self.con_mode == FULL:
            if pin < 1 or pin > 4:
                raise ValueError('GPIO - Pin must be between 1 and 4')
            return
        i2c_pins_reserved = [3,4]
        serial_pins_reserved = [1,2]
        if self.con_mode == I2C and pin in i2c_pins_reserved:
            raise ValueError ('GPIO - pin %s is reserved for I2C operation' % str(pin))
        if self.con_mode == SERIAL and pin in serial_pins_reserved:
            raise ValueError ('GPIO - pin %s is reserved for Serial operation' % str(pin))


    def configure(self):
        """
        Configure GPIO controller
        """
        self._usbiss.mode = [self.IO_CHANGE, self.ControlRegister]

    def _send_dataregister(self):
        """
        Send the dataregister to the USBISS device
        """
        self._usbiss.write_data([self.IO_SETPINS_CMD, self.DataRegister])
        resp = self._usbiss.read_data(1)
        resp = self._usbiss.decode(resp)
        if resp != [0xFF]:
            raise RuntimeError('USB-ISS: GPIO output - Transmission Error')
        

    def _setup_pin(self, pin, mode):
        """
        Helper function to setup s GPIO pin.
        Mode = IN, OUT, ADC for analog conversions
        """
        if mode not in (IN, OUT, ADC):
            raise ValueError('Mode must be GPIO.IN, GPIO.OUT or GPIO.ADC')
        self._check_pins_and_con_mode(pin) # Check if this pin may be changed in this mode (I2C, SERIAL, FULL)
        for i in range(0, 2):
            if mode & 1 << i:
                self.ControlRegister |= 1 << (pin -1) * 2 + i
            else:
                self.ControlRegister &= ~(1 << (pin - 1) *2 + i)


    def setup(self, pin, mode):

        """
        Set the input or output mode for a specified pin.  Mode should be
        either OUT or IN or ADC.
        """
        self._check_pins_and_con_mode(pin) # Check if this pin may be changed in this mode (I2C, SERIAL, FULL)
        self._setup_pin(pin, mode)
        self.configure()

    def setup_pins(self, pins, values={}):
        """
        Ex : setup_pins({1:gpio.OUT, 2:gpio.OUT, 3:gpio.IN, 4: gpio.IN}, {1:gpio.HIGH, 2:gpio.HIGH})
        Setup multiple pins as inputs or outputs at once.  Pins should be a
        dict of pin name to pin mode (IN or OUT).  Optional starting values of
        pins can be provided in the values dict (with pin name to pin value).
        """
        # pin setup
        for pin, mode in pins.items():
            self._check_pins_and_con_mode(pin) # Check if this pin may be changed in this mode (I2C, SERIAL, FULL)
            self._setup_pin(pin, mode)
        self.configure()
        # pin values
        for pin, value in values.items():
            self._check_pins_and_con_mode(pin) # Check if this pin may be changed in this mode (I2C, SERIAL, FULL)
            self._output_pin(pin, value)
        self._send_dataregister()


    def _output_pin(self, pin, level):
        """
        Helper function to set a pin to a high or low level
        """
        self._check_pins_and_con_mode(pin) 
        if level:
            self.DataRegister |= 1 << (pin-1)
        else:
            self.DataRegister &= ~(1 << (pin - 1))

    def output(self, pin, level):
        """
        Set the specified pin the provided high/low value.  Value should be
        either HIGH/LOW or a boolean (true = high).
        """
        self._check_pins_and_con_mode(pin) 
        self._output_pin(pin, level)
        self._send_dataregister()

    def output_pins(self, pins):
        """Set multiple pins high or low at once.  Pins should be a dict of pin
        name to pin value (HIGH/True for 1, LOW/False for 0).  All provided pins
        will be set to the given values.
        """
        for pin, value in iter(pins.items()):
            self._check_pins_and_con_mode(pin) 
            self._output_pin(pin, value)
        self._send_dataregister()


    def input(self, pin):
        """
        Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        self._check_pins_and_con_mode(pin) 
        self._usbiss.write_data([self.IO_GETPINS_CMD])
        self.DataRegister = int.from_bytes(self._usbiss.read_data(1), byteorder='little')
        return(self.DataRegister & (1 << (pin -1)) !=0)

    def input_pins(self, pins):

        """
        Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        for pin in pins:
            self._check_pins_and_con_mode(pin)   
        self._usbiss.write_data([self.IO_GETPINS_CMD])
        self.DataRegister = int.from_bytes(self._usbiss.read_data(1), byteorder='little')
        # Adafruit - return [((_pins >> pin) & 0x0001) == 1 for pin in pins]
        return [((self.DataRegister >> (pin-1))& 0x0001) for pin in pins]


    def adc(self, pin, vcc):
        """
        Read the analog voltage on the pin. vcc is the provided voltage to
         the USBISS and is used as reference for the pin voltage.
        """
        self._check_pins_and_con_mode(pin)
        self._usbiss.write_data([self.IO_GETAD_CMD, pin])
        adcv = self._usbiss.read_data(2)
        # DEBUG print('ADC 0 {} 1 {}'.format(adcv[0], adcv[1]))
        return(vcc/(1024*(255*adcv[0]+adcv[1])))

    

