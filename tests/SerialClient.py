# GdH SerialClient 29-3-2019
# Testprogram for the USBISS Serialdriver
# Used in conjunction with the unittest : test_serial_otherclient.
# Prerequisite is the availability of another COM port on the test machine. A standard FTDI based device can be used
# Connect the tx pin from USBISS serial pins to the rx pin of the other COM port and vica versa.
# Start the program in a separate DosBox 
# ---------------------------------------------------------- 


import serial
import time

clientport = "COM6"
baud = 9600

class testSerial(object):

    def __init__(self):
        self.serialPort = serial.Serial(port = clientport, baudrate=baud,
                           bytesize=8, timeout=5, stopbits=serial.STOPBITS_ONE)



    def test_readline(self):

        serialString = ""                           # Used to hold data coming over UART
        while(True):
            time.sleep(.5)    
            # Wait until there is data waiting in the serial buffer
            if(self.serialPort.in_waiting > 0):

                # Read data out of the buffer until a carraige return / new line is found
                serialString = self.serialPort.readline()
                print(serialString)
                return(serialString)

    def test_sendLine(self, line_to_send):
        self.serialPort.write(line_to_send)





if __name__ == '__main__':
    sc = testSerial()
    while(True):
        # Receive line from the USBISS
        line_received = sc.test_readline()
        time.sleep(1)
        # Send the line back to the USBISS
        sc.test_sendLine(line_received)            