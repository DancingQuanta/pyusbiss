"""Implements a HD44780 character LCD connected via PCF8574 on I2C."""

# The following import was needed on my OpenMV board
import time

import i2c as I2C
# from lcd_api import LcdApi
from usbiss_i2c_lcd_inheritance import I2cLcd


# import I2CDevice as I2CDevice 
# from I2CDevice import I2CDevice


# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 78

def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    i2c = I2C.I2C('COM3', 'H', 100) 
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
    lcd.putstr("USBISS Lcd_API\n Inheritance")
    time.sleep(3000/1000.0)
    lcd.clear()
    count = 0
    while True:
        lcd.move_to(0, 0)
        # pyb lcd.putstr("%7d" % (millis() // 1000))        
        lcd.putstr("%7d" % (count)) # millis() not available in Python
        time.sleep(1000/1000.0)
        count += 1
        if count % 10 == 3:
            print("Turning backlight off")
            lcd.backlight_off()
        if count % 10 == 4:
            print("Turning backlight on")
            lcd.backlight_on()
        if count % 10 == 5:
            print("Turning display off")
            lcd.display_off()
        if count % 10 == 6:
            print("Turning display on")
            lcd.display_on()
        if count % 10 == 7:
            print("Turning display & backlight off")
            lcd.backlight_off()
            lcd.display_off()
        if count % 10 == 8:
            print("Turning display & backlight on")
            lcd.backlight_on()
            lcd.display_on()

#if __name__ == "__main__":
test_main()
