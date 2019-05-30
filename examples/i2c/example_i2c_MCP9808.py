# Based on https://github.com/mercolino/MCP9808
# Adapted for use with th USBISS Device by Geert de Haan 

# import MCP9808.mcp9808 as MCP9808
from usbiss import usbiss
from Devices import mcp9808 as MCP9808
from usbiss import i2c as I2C 
from usbiss import gpio

import time

port = 'COM3'
usbissdev = usbiss.USBISS(port)

io2 = gpio.GPIO(usbissdev, gpio.I2C)
io2.setup(1, gpio.OUT)
io2.output(1, gpio.HIGH)
io2.setup(2, gpio.IN)

i2c_chan = I2C.I2C(usbissdev, 'H', 100)

sensor = MCP9808.MCP9808(i2c_chan, 48)


# Optionally you can override the address and/or bus number:
#sensor = MCP9808.MCP9808(address=0x20, busnum=2)

# Initialize communication with the sensor.
sensor.begin()

# Print the Config Register
sensor.clearConfigReg()
print('Config register: {0:#06X}'.format(sensor.getConfigReg()))

# Print the Resolution Register
print (sensor.getResolution())

# You could change the resolution of the sensor
sensor.setResolution(0.25)

# GdH - Debug self._i2c.reverseByteOrder(new_config)) ******

sensor.setTempHyst(0)

# Set the Window and Critical temperature to use the alert output pin
sensor.setLowerTemp(25.0)
t = sensor.getLowerTemp()
sensor.setUpperTemp(30.00)
sensor.setCritTemp(33.0)

# Enable the Alert pin, Remember that you should use a pullup resistor, for further information
# read the MCP9808 Datasheet
sensor.setAlertCtrl()

print ("Window Temperature: %d - %d" %(sensor.getLowerTemp(), sensor.getUpperTemp()))
print ("Critical Temperature: %d" %(sensor.getCritTemp()))

# Print the Config Register, Note how the config register change by setting the Alert Control pin
print ('Config register: {0:#06X}'.format(sensor.getConfigReg()))

# Loop printing measurements every second.
print ('Press Ctrl-C to quit.')


while True:
	# Check the MCP9808 Alert pin with an usbiss 
	# GPIO input pin
	if io2.input(2) == gpio.LOW:
		print("MCP9808 : Alert pin Low (Open collector) ")
		# Read the 3 bits to know why the alert is set, read the datasheet to kno more
		print ('Sensor Alert Output: {0:#05b}'.format(sensor.getAlertOutput()))
	# Read the temperature	
	temp = sensor.readTempC()
	print ('Temperature: {0:0.3F}*C'.format(temp))

	time.sleep(1.0)
