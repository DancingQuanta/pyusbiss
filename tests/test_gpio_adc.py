# Test GPIO based on Adafruit library for FT232H
import time
from gpio import GPIO
usbiss=GPIO('COM3')
print(usbiss._usbiss.__repr__)

usbiss.setup(1, GPIO.OUT)
usbiss.setup(3, GPIO.IN) # Make pin 3 a digital input.
usbiss.setup(2, GPIO.ADC)
print('Press Ctrl-C to quit.')
while True:
    # Set pin C0 to a high level so the LED turns on.
    usbiss.output(1, GPIO.HIGH)
    # Sleep for 1 second.
    time.sleep(1)
    # Set pin C0 to a low level so the LED turns off.
    usbiss.output(1, GPIO.LOW)
    # Sleep for 1 second.
    time.sleep(1)
    # Read the input on pin D4 and print out if it's high or low.
    level = usbiss.input(3)
    if level == GPIO.LOW:
        print('Pin D4 is LOW!')
    else:
        print('Pin D4 is HIGH!')
    vin = usbiss.adc(2, 5)
    print('Voltage on pin 2 {}'.format(vin))
    