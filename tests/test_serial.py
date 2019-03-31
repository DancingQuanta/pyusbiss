# Test Serial
# GdH - 27-3-2019 
import time
from usbiss import serial


Port='COM3' 
Baudrate = 300


def write_serial(connection):
    string = [0x41, 0x42, 0x43, 0x44]
    connection.serial_write(string)

def read_serial(connection):

    #ser.serial_write([0x41, 0x42, 0x41, 0x42])

    rxcount = connection.in_waiting 
    if rxcount > 0:
        com = connection.serial_read(rxcount)
        # rxcount = 0 na het lezen
        rxcount = connection.in_waiting 
        print(com, rxcount)

def read_serial_char(connection):       
    # gaat niet goed, je kunt niet karakter voor karakter lezen
    # UPDATE gaat wel, maar niet tussendoor meer het controlblok lezen

    rxcount = connection.in_waiting
    for i in range(rxcount):
        #time.sleep(0.5)
        char = connection.serial_read(1)
        #time.sleep(0.5)
        print(char)
        char = connection.serial_read(3)
        print(char)




if __name__ == '__main__':
    ser = serial.SERIAL(Port, Baudrate)
    # setuptime needed by the usbiss
    time.sleep(1)
    n=1
    while(n<=2):
        n+=1
        write_serial(ser)
        time.sleep(0.5) #time needed to send the string)
        read_serial_char(ser)