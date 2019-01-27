
import time
import i2c as I2C
from i2c_led import led
# from i2c_led import switch

def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    i2c_chan = I2C.I2C('COM3', 'H', 100)
    led1 = led(i2c_chan, 72, 1 )
    led2 = led(i2c_chan, 72, 3)
    # switch1 = switch(i2c_chan, 114, 5)
    while(True):
        led1.on()
        led2.off()
        time.sleep(1)
        led1.off()
        led2.on()
        time.sleep(1)
        # if switch1.ison():
            # pass

test_main()