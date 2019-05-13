
import i2c as I2C
import time



# SE95 Registers



TEMP    = 0x00  #  2 8-bit data byes to store the measured temp
CONF    = 0x01  # Configuration register: containes a single 9-bit data byte to set an operating condition
THYST   = 0x02  # Hysteresis register: contains two 8-bit data bytes; to store the hysteris limit; bit 7 to bit 0 are also used in OTP test mode to supply OTP write data; default = 75 C
TOS     = 0x03  # Overtemperature shutdown threshold register: contains two8-bit data bytes; to store the overtemperature shutdown limit; default Tos =- 80 C
NU      = 0x04  # Not used
ID      = 0x05  # identification register: contains a single 8-bit data byte for the manufacturer ID code
GPPU    = 0x06  # Pull-up register configuration



I2Channel = I2C.I2C('COM3', 'H', 100) 
# Check succesfull basic setup
print(I2Channel._usbiss.__repr__)

lc256 = I2CDevice.I2CDevice(I2Channel, 160)

def scan():
    I2CDevices = I2Channel.scan()

    #Scan the I2C channel for devices
    for I2CDev in I2CDevices:
        print(I2CDev)

def ping():
    t = lc256.ping()
    print(t)

def readconf():
    t = se95.readU8(CONF)
    print(t)



writepattern()
#readpattern()