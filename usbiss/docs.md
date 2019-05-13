# SERIAL

- Based on Pyserial as  protocol library
- Uses local readbuffering  

## Usage

```python
from usbiss import usbiss
from usbiss import serial

Port = 'COM3'

usbissdev = usbiss.USBISS(Port)
serport = serial.SERIAL(usbissdev)

serport.serial_write('Serial write test\n')
```

## Methods



| Method       | Description           |
| --- | --- |
| in_waiting |Returns the number of bytes in the inputbuffer  |
| out_waiting |Returns the number of bytes in the outputbuffer |
| serial_write(data) |Write data to the serial pins of the USBISS     | 
| | - data - data to be send. |
| serial_read(size) | Read size bytes from the USBISS serial
| | - size - number of bytes to read |
|	| Returns - string of size bytes |
| readline() | Read line from the USBISS serial. |
| | Returns - string up until the first \n|

## Extras
The Serial library can be combined with the GPIO library. Pins 3 and 4 are available for I/O

## Tests

Test | Description
----------------------------------- | ---
test_serial_loopback.py |Loopback test by connecting the Rx and Tx pins of the USBISS, the outputbuffer of the USBISS holds a maximum of 30 bytes. It is not possible to send more bytes in this loopback setup
test_serial_loopback - GPIO.py |Same as test_serial_loopback.py but combined with the GPIO functionality of the USBISS.
test_serial_otherclient.py | Loopback test by connecting the Rx and Tx pins to a FTDI device. This Device is used by with the SerialClient.py script to perform the loopback. With this test data that exceeds 30 bytes can be send and tested. 
test_serial_otherclient - GPIO.py | Same as test_serial_otherclient.py but combined with the GPIO functionality of the USBISS. 
