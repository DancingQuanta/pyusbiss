# Example GPIO based on Adafruit library for FT232H
# For the GPIO the connection to the USBISS is made outside the GPIO class thereby
# enabling using the GPIO class for use in I2C en Serial mode.
# GdH 23-3-20-19
import time
from usbiss import gpio
from usbiss import usbiss

usbiss = usbiss.USBISS('COM3') 
io4=gpio.GPIO(usbiss) 



# io4.setup(1, gpio.OUT)
# io4.setup(3, gpio.IN) # Make pin 3 a digital input.
io4.setup_pins({1:gpio.OUT, 2:gpio.OUT, 3:gpio.IN, 4: gpio.IN}, {1:gpio.HIGH, 2:gpio.HIGH})
time.sleep(20)
print('Press Ctrl-C to quit.')
while True:
    # Set pin C0 to a high level so the LED turns on.
    io4.output(1, gpio.HIGH)
    # Sleep for 1 second.
    time.sleep(1)
    # Set pin C0 to a low level so the LED turns off.
    io4.output(1, gpio.LOW)
    # Sleep for 1 second.
    time.sleep(1)
    io4.output_pins({1:gpio.HIGH,2:gpio.HIGH})
    time.sleep(1)
    io4.output_pins({1:gpio.LOW,2:gpio.LOW})
    # Read the input on pin D4 and print out if it's high or low.
    level = io4.input(3)
    if level == gpio.LOW:
        print('Pin D3 is LOW!')
    else:
        print('Pin D3 is HIGH!')
    # read the inputvalues of pins 3 and 4 and print the result
    levels = io4.input_pins([3,4])
    print(levels)
    