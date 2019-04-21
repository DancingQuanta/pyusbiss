# Test Serial
# GdH - 27-3-2019 
import time
from usbiss import serial


Port='COM3' 
Baudrate = 9600


def write_serial(connection):
    serialString = 'The Quick Bron Fox Jumps Over The Lazy Dog this a very long string of characters.\n' 
    #serialString='Hello World where the Quick  Pi'
    

    connection.serial_write(serialString)

def loopback(connection):
    # serial_write
    # readline
    connection.serial_write('The Quick Bron Fox Jumps Over The Lazy Dog this a very long string of characters.\n')
    time.sleep(.5)
    resp = connection.readline()
    print('Response = ', resp)

def loopback2(connection):
    string = 'Hello World\n'
    connection.serial_write(string)
    time.sleep(.5)
    # waiting = connection.in_waiting
    waiting = connection.in_waiting
    if waiting==0:
        print('Nothing to receive')
        return
    while(waiting > 0):
        time.sleep(.1)
        resp = connection.serial_read(waiting)
        respasc = ''.join(map(chr, resp))
        print('Resp = ', resp)
        print('Resp = ', respasc)
        time.sleep(.1)
        waiting = connection.in_waiting

if __name__ == '__main__':
    print(__name__)
    ser = serial.SERIAL(Port, Baudrate)
    # setuptime needed by the usbiss
    #print('pre-sleep')
    #time.sleep(.5)
    #print('init')
    #n=0
    #while(True):
        #write_serial(ser)
        #time.sleep(1)
        #res = read_serial(ser)
        #write_serial(ser)
        #time.sleep(5)
        #print(n)

     #   l = ser.readline()
        
     #   print(l)
    loopback(ser)
        
            