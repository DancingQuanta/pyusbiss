# from i2c import I2C
# import i2c as 
import time
# from usbiss import i2c
# import usbiss
from usbiss import I2C

# import usbiss.i2c
# import I2CDevice as I2CDevice 


# Check on 24LC256 EEPROM


I2Channel = I2C.I2C('COM3', 'H', 100) 
# Check succesfull basic setup
print(I2Channel._usbiss.__repr__)

lc256 = I2C.I2CDevice(I2Channel, 160)

def scan():
    I2CDevices = I2Channel.scan()

    #Scan the I2C channel for devices
    for I2CDev in I2CDevices:
        print(I2CDev)

def ping():
    t = lc256.ping()
    print(t)

def writepattern():
    pat1 = [0x0f]
    pat2= [0xf0]
    for h in range(255):
        for i in range(255):
            if i % 2 == 1:
                data = pat1
            else:
                data = pat2
            lc256.writeMem(h, i, len(data), data)

def readpattern():
    t = lc256.readMem(0x00, 0x00, 64)
    for i in range(255):
        t = lc256.readMem(0x00, i, 1)
        print(t)

#writepattern()
#readpattern()
scan()