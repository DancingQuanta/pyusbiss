# MCP9808 driver for USBISS I2C
# 27-4-2019
# Geert de Haan

#import i2c as I2C
#import time

#MCP9808 registers
CONFIG = 1 # Configuration register 
TUPPER = 2 # Alert Temperature Upper Boundary Trip register
TLOWER = 3 # Alert Temperature Lower Boundary Trip register 
TCRIT  = 4 # Critical Temperature Trip register 
TA     = 5 # Temperature register
MANID  = 6 # Manufacturer ID register
DEVID  = 7 # Device ID/Revision register
RESOL  = 8 # Resolution Register

# MCP9808 Config register bit
ALERT_MOD = 0 # Alert output mode bit
ALERT_POL = 1 # Alert output polarity bit
ALERT_SEL = 2 # Alert output select bit
ALERT_CNT = 3 # Alert output control bit
ALERT_STAT = 4 # Alert output status bit
INT_CLEAR = 5 # Interrupt clear bit
WIN_LOCK = 6 # TUPPER and TLOWER Window lock bit
CRIT_LOCK = 7 # TCRIT lock bit

import time
from usbiss import i2c as I2C 



class mcp9808(I2C.I2CDevice):

    def __init__(self, i2c_channel, i2c_addr = 48): 
        self._i2c_channel = i2c_channel
        self._i2c_addr = i2c_addr
        I2C.I2CDevice.__init__(self, self._i2c_channel, self._i2c_addr)

    
    def readtemp(self):
        # Send 0x05
        # Read 2 bytes
        ret = self.readList(TA, 2)
        u = (ret[0] & 0x0f) << 4
        l = ret[1] / 16

        if ret[0] & 0x10 == 0x10:
            temp = (u + l) - 256.0
        else:
            temp = u + l
        return(temp)

    def settemp(self, treg, value):
        # input : -20
        pass

if __name__ == '__main__':
        i2c_chan = I2C.I2C('COM3', 'H', 100)
        t = mcp9808(i2c_chan, 48)
        while(True):
            temp = t.readtemp() 
            print(temp)
            time.sleep(1)