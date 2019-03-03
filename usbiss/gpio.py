# gpio.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# GdH - based on FT232H.py library from Adafruit for the FT232 (FTDI)

"""GPIO support for USB-ISS"""

import  usbiss


class GPIO(object):
    """GPIO operating mode of USBISS
    """


    IO_MODE = 0x00
    IO_CHANGE = 0x10
    IO_SETPINS_CMD = 0x63
    IO_GETPINS_CMD = 0x64
    IO_GETAD_CMD = 0x65
    # Pin mode (IO_TYPE)
    OUT  = 0b00
    OUTH = 0b01
    IN   = 0b10
    ADC  = 0b11

    HIGH=1
    LOW=0


    def __init__(self, port):
        # Default Configure USB-ISS as IO all pins as input to protect the
        # external circuit and the USBISS from damage.
        self.ControlRegister = 0b10101010 # All inputs
        self.DataRegister = 0x00
        self._usbiss = usbiss.USBISS(port)

        self._usbiss.set_iss_mode([self.IO_MODE, self.ControlRegister])


    def open(self):
        self._usbiss.open()


    def close(self):
        self._usbiss.close()


    def configure(self):
        """
        Configure GPIO controller
        """
        self._usbiss.set_iss_mode([self.IO_CHANGE, self.ControlRegister])

    def _setup_pin(self, pin, mode):
        """
        Helper function to setup s GPIO pin.
        Mode = IN, OUT, ADC for analog conversions
        """
        if pin < 1 or pin > 4:
            raise ValueError('Pin must be between 1 and 4')
        if mode not in (GPIO.IN, GPIO.OUT, GPIO.ADC):
            raise ValueError('Mode must be GPIO.IN, GPIO.OUT or GPIO.ADC')
        # print('setup - before', format(self.ControlRegister, '08b'))
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
        # print('setup - before', format(self.ControlRegister, '08b'))
        self._setup_pin(pin, mode)
        # print('setup - after', format(self.ControlRegister, '08b'))
        self.configure()

    def setup_pins(self, pins, values={}):
        """Setup multiple pins as inputs or outputs at once.  Pins should be a
        dict of pin name to pin mode (IN or OUT).  Optional starting values of
        pins can be provided in the values dict (with pin name to pin value).
        """
        for pin, mode in pins.items():
            self._setup_pin(pin, mode)
        for pin, value in values.items():
            self._output_pin(pin, value)

    def _output_pin(self, pin, level):
        """
        Helper function to set a pin to a high or low level
        """
        if pin <1 or pin >4:
            raise ValueError('Pin must be between 1 and 4.')
        if level:
            self.DataRegister |= 1 << (pin-1)
        else:
            self.DataRegister &= ~(1 << (pin - 1))

    def output(self, pin, level):
        """
        Set the specified pin the provided high/low value.  Value should be
        either HIGH/LOW or a boolean (true = high).
        """
        self._output_pin(pin, level)
        self._usbiss.write_data([self.IO_SETPINS_CMD, self.DataRegister])
        response = self._usbiss.read_data(1)
        if response != 0xFF:
            raise RuntimeError('USB-ISS: GPIO output - Transmission Error')
        return response


    def output_pins(self, pins):
        """Set multiple pins high or low at once.  Pins should be a dict of pin
        name to pin value (HIGH/True for 1, LOW/False for 0).  All provided pins
        will be set to the given values.
        """
        for pin, value in iter(pins.items()):
            self._output_pin(pin, value)
        self._usbiss.write_data([self.IO_SETPINS_CMD, self.DataRegister])
        response = self._usbiss.read_data(1)
        #TODO - Raise exception when respond != 0xFF or handle in _usbiss.write_data

    def input(self, pin):
        """
        Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        self._usbiss.write_data([self.IO_GETPINS_CMD])
        self.DataRegister = int.from_bytes(self._usbiss.read_data(1), byteorder='little')
        # DEBUG print(type(self.DataRegister))
        # DEBUG print('input {}', format(self.DataRegister, '08b'))
        return(self.DataRegister & (1 << (pin -1)) !=0)

    def input_pins(self, pins):

        """
        Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        if [pin for pin in pins if pin <1 or pin > 4]:
            raise ValueError('Pin must be between 1 and 4.')
        self._usbiss.write_data([self.IO_GETPINS_CMD])
        self.DataRegister = int.from_bytes(self._usbiss.read_data(1), byteorder='little')
        # Adafruit - return [((_pins >> pin) & 0x0001) == 1 for pin in pins]
        return [((self.DataRegister >> (pin-1))& 0x0001) for pin in pins]

        

    def adc(self, pin, vcc):
        """
        Read the analog voltage on the pin. vcc is the provided voltage to
        tot the USBISS and is used as reference 
        """
        self._usbiss.write_data([self.IO_GETAD_CMD, pin])
        adcv = self._usbiss.read_data(2)
        # DEBUG print('ADC 0 {} 1 {}'.format(adcv[0], adcv[1]))
        return(vcc/(1024*(255*adcv[0]+adcv[1])))

    
