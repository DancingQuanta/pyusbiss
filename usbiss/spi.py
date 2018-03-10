# spi.py, part of pyusbiss
# Copyright (c) 2016, 2018 Andrew Tolmie <andytheseeker@gmail.com>
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""SPI support for USB-ISS"""

from .usbiss import USBISS


class SPI(object):
    """SPI operating mode of USBISS
    """

    def __init__(self, port, mode=0, max_speed_hz=3000000):
        self._usbiss = USBISS(port)

        self.sck_divisor = 1

        # Select the SPI mode of USB-ISS's SPI operating mode
        self.mode = mode

        # Select frequency of USB-ISS's SPI operating mode
        self.max_speed_hz = max_speed_hz

    def open(self):
        self._usbiss.open()

    def close(self):
        self._usbiss.close()

    def configure(self):
        """
        Configure SPI controller
        """

        # Convert official SPI sheme to USBISS scheme
        lookup_table = [0, 2, 1, 3]
        mode = lookup_table[self._mode]
        # Add signal for SPI switch
        iss_mode = self._usbiss.SPI_MODE + mode

        # Configure USB-ISS
        self._usbiss.set_mode([iss_mode, self.sck_divisor])

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
        if 0 <= val < 4:
            self._mode = val
            self.configure()
        else:
            error = "The value of SPI mode, {}, is not between 0 and 3".format(
                val
            )
            raise ValueError(error)

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
        self.configure()

    def iss_spi_divisor(self, sck):
        """Calculate a divisor from input SPI clock speed
        """
        _divisor = (6000000 / sck) - 1
        divisor = int(_divisor)

        if divisor != _divisor:
            raise ValueError('Non-integer SCK divisor.')

        if not 1 <= divisor < 256:
            error = ("The value of sck_divisor, {},"
                     "is not between 0 and 255".format(divisor)
                     )
            raise ValueError(error)
        return divisor

    def exchange(self, data):
        """
        Perform SPI transaction.

        The first received byte is either ACK or NACK.

        TODO: enforce rule that up to 63 bytes of data can be sent.
        TODO: enforce rule that there is no gaps in data bytes (what define a gap?)
        """
        self._usbiss.write_data([self._usbiss.SPI_CMD] + data)
        response = self._usbiss.read_data(1 + len(data))
        if len(response) != 0:
            response = self._usbiss.decode(response)
            status = response.pop(0)
            if status == 0:
                raise RuntimeError('USB-ISS: Transmission Error')
            return response

        else:
            raise RuntimeError('USB-ISS: Transmission Error: No bytes received!')

    def xfer(self, data):
        return self.exchange(data)

    def xfer2(self, data):
        return self.exchange(data)

    def readbytes(self, len):
        """
        Read len bytes from SPI device.
        """
        dummybytes = [0] * len
        return self.exchange(dummybytes)

    def writebytes(self, data):
        """
        Write bytes to SPI device.
        """
        self.exchange(data)
