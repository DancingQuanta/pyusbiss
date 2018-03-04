# spi.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""SPI support for USB-ISS"""

from .usbiss import USBISS


class SPI(USBISS):
    """SPI operating mode of USBISS
    """


    SPI_MODE = 0x90
    SPI_CMD = 0x61


    def __init__(self, port, mode=0, max_speed_hz=3000000):

        self._mode = mode
        self._max_speed_hz = max_speed_hz
        self.sck_divisor = 1

        # Execute baseclass __init__
        super(SPI, self).__init__(port)

        # Select the SPI mode of USB-ISS's SPI operating mode
        self.mode = mode

        # Select frequency of USB-ISS's SPI operating mode
        self.max_speed_hz = max_speed_hz

        # Configure USB-ISS
        self.set_iss_mode([self.iss_mode, self.sck_divisor])

    @property
    def mode(self):
        """
        Property that gets / sets the SPI mode as two bit pattern of Clock
        Polarity and Phase [CPOL|CPHA].

        Emulates spidev.SpiDev.mode with USBISS.SPI.mode.

        Users must use standard SPI mode numbers.
        USBISS.SPI.mode uses standard SPI mode numbers which do not match up
        with USBISS number commands.
        A lookup table will select the correct USBISS number command based on
        chosen SPI mode.
        Serves as a check on the value of the SPI mode which should be between
        0 and 3.
        """
        return self._mode

    @mode.setter
    def mode(self, val):
        try:
            lookup_table = [0, 2, 1, 3]
            self._mode = lookup_table[val]
        except:
            error = "The value of SPI mode, {}, is not between 0 and 3".format(
                val
            )
            raise ValueError(error)

        # Add signal for SPI switch
        self.iss_mode = self.SPI_MODE + self._mode

    @property
    def max_speed_hz(self):
        """
        Property that gets / sets the maximum bus speed in Hz.

        Emulates spidev.SpiDev.max_speed_hz with USBISS.SPI.max_speed_hz.
        """
        return self._max_speed_hz

    @max_speed_hz.setter
    def max_speed_hz(self, val):
        self._max_speed_hz = val
        self.sck_divisor = self.iss_spi_divisor(val)

    def xfer(self, data):
        """
        Perform SPI transaction.

        The first received byte is either ACK or NACK.

        TODO: enforce rule that up to 63 bytes of data can be sent.
        TODO: enforce rule that there is no gaps in data bytes (what define a gap?)
        """
        self.iss_write([self.SPI_CMD] + data)
        response = self.iss_read(1 + len(data))
        if len(response) != 0:
            response = self.decode(response)
            status = response.pop(0)
            if status == 0:
                raise RuntimeError('USB-ISS: Transmission Error')
            return response

        else:
            raise RuntimeError('USB-ISS: Transmission Error: No bytes received!')

    def iss_spi_divisor(self, sck):
        """Calculate a divisor from input SPI clock speed
        """
        _divisor = (6000000 / sck) - 1
        divisor = int(_divisor)

        if divisor != _divisor:
            raise ValueError('Non-integral SCK divisor.')

        if not 1 <= divisor < 256:
            error = "The value of sck_divisor, %s, is not between 0 and 255" % (divisor)
            raise ValueError(error)
        return divisor
