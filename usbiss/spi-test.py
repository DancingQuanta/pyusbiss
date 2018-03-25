from spi import SPI
t=SPI('COM3', 1, 25000)
print(t._usbiss.__repr__)