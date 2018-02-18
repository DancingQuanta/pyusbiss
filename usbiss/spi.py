
from . import USBISS

class SPI(USBISS):
    """SPI operating mode of USBISS
    """

    self.mode = None
 

    def __init__(self, port, spi_mode=None, freq=None):

        # Execute baseclass __init__
        super(SPI, self).__init__(port)

        # Select the SPI mode of USB-ISS's SPI operating mode
        try:
            # Emulate spidev.SpiDev.mode through self.mode.
            # self.spi_mode do not corresponds to spidev.SpiDev.mode.
            # self.mode is set with a value from a lookup table.
            # critical because external applications may inspect this value.
            # Serves as a check on value of spi_mode which should be between
            # 0 and 3.
            lookup_table = [0, 2, 1, 3]
            self.mode = lookup_table[spi_mode]

            # Add signal for SPI switch
            spi_mode = 0x90 + spi_mode
        except:
            error = ("The value of spi_mode, %s, is not between 0 and 3" %
                     (spi_mode))
            raise ValueError(error)

        # Select frequency of USB-ISS's SPI operating mode
        try:
            sck_divisor = self.iss_spi_divisor(freq)
        except:
            raise TypeError("Missing argument for frequency for SPI mode")

        # Configure USB-ISS
        self.set_iss_mode([spi_mode, sck_divisor])

    def xfer(self, data):
        """Spidev function for transferring bytes to port
        TODO: enforce rule that up to 63 bytes of data can be sent.
        TODO: enforce rule that there is no gaps in data bytes (what define a gap?)
        """
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
