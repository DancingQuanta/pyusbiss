from I2CDevice import I2CDevice

class led(I2CDevice):

    def __init__(self, i2c_channel, i2c_addr, pin):
        self.i2c_channel = i2c_channel
        self.i2c_addr = i2c_addr
        self.pin = pin
        I2CDevice.__init__(self, self.i2c_channel, self.i2c_addr)

    def on(self):
        data = self.readRaw8()       
        data |= 1 << (self.pin - 1)
        self.writeRaw8(data)

    def off(self):
        data = self.readRaw8()
        data &= ~(1 << (self.pin - 1))
        self.writeRaw8(data)

class switch(I2CDevice):
 

    def __init__(self, i2c_channel, i2c_addr, pin):
        self.i2c_channel = i2c_channel
        self.i2c_addr = i2c_addr
        self.pin = pin
        I2CDevice.__init__(self, self.i2c_channel, self.i2c_addr)


    def isOn(self):
        data = self.readRaw8()
        return(data & (1 << (self.pin -1)) !=0)
