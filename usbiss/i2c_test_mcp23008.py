# from i2c import I2C
import i2c as I2C
import time
import I2CDevice as I2CDevice 


# MCP23008 Registers



IODIR   = 0x00  # IO Direction
IPOL    = 0x01  # Input polarity
GPINTEN = 0x02  # Interrupt on Change
DEFVAL  = 0x03  # Default Compare (for interrupt)
INTCON  = 0x04  # Interrupt Control
IOCON   = 0x05  # Configuration register for MCP23008
GPPU    = 0x06  # Pull-up register configuration
INTF    = 0x07  # Interrupt Flag Register
INTCAP  = 0x08  # Interrupt Capture Register
GPIO    = 0x09  # Port (GPIO) Register - Write - modifies Output latch (OLAT)
OLAT    = 0x0A  # Output latch register


I2Channel = I2C.I2C('COM3', 'H', 100) 
# Check succesfull basic setup
print(I2Channel._usbiss.__repr__)

def scan():
    I2CDevices = I2Channel.scan()

    #Scan the I2C channel for devices
    for I2CDev in I2CDevices:
        print(I2CDev)



def test_readU16():
    # Also testing the write8 method
    mcp23008 = I2CDevice.I2CDevice(I2Channel, 64)

    # print(mcp23008.ping())
    # test 1 LED brandt op GP0
    mcp23008.write8(IODIR, 0x00)
    mcp23008.write8(GPIO, 0xFF)
    resp = mcp23008.readU16(GPIO) #Leest 2 bytes, GPIO en OLAT, moeten bij desgin hetzelfde zijn
    
    # pca8574.writeRaw8(0)

    # resp = pca8574.readRaw8()

    print (resp)

def test_write16():
    mcp23008 = I2CDevice.I2CDevice(I2Channel, 64)

    # print(mcp23008.ping())
    # test 1 LED brandt op GP0
    mcp23008.write16(IODIR, 0x00FF, False)

    resp = mcp23008.readU16(IODIR, False) #Leest 2 bytes, GPIO en OLAT, moeten bij desgin hetzelfde zijn
    
    # pca8574.writeRaw8(0)

    # resp = pca8574.readRaw8()

    print (resp)

def test_writelist():
    # GdH - 9-2-2019 Test 
    mcp23008 = I2CDevice.I2CDevice(I2Channel, 64)
    # self.i2c.send(b'\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00', self.i2c_addr)
    mcp23008.writeList(IODIR, [0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])       

    registers = mcp23008.readList( IODIR, 11)  
    for i in registers:
        print(i, end=',')  


test_writelist()