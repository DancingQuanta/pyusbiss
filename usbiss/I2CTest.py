# from i2c import I2C
import i2c as I2C
import time
import I2CDevice as I2CDevice 

I2Channel = I2C.I2C('COM3', 'H', 100) 
# Check succesfull basic setup
print(I2Channel._usbiss.__repr__)

I2CDevices = I2Channel.scan()

#Scan the I2C channel for devices
for I2CDev in I2CDevices:
    print(I2CDev)


#pca8574 = I2CDevice.I2CDevice(I2Channel, 112)

#print(pca8574.ping())

#pca8574.writeRaw8(0xFF)

#resp = pca8574.readRaw8()

#print (resp)