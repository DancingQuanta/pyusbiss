# Test GPIO based on Adafruit library for FT232H
# GdH 25-3-2018
# The original gpio_test for the FT232H has an odd behaviore
# on the input. While reading every third read will be correct, the
# other two return 0xFF
# This testscript is working correctly, so the problem is not the
# preceding time.sleep(1)
  
import time
from gpio import GPIO
usbiss=GPIO('COM3')
print(usbiss._usbiss.__repr__)

usbiss.setup(3, GPIO.IN) # Make pin 3 a digital input.
print('Press Ctrl-C to quit.')
while True:
    time.sleep(1)
    level = usbiss.input(3)
    if level == GPIO.LOW:
        print('Pin D4 is LOW!')
    else:
        print('Pin D4 is HIGH!')