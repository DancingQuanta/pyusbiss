from pyb import I2C
i2c = I2C(1)                         # create on bus 1
i2c = I2C(1, I2C.MASTER)             # create and init as a master
i2c.init(I2C.MASTER, baudrate=100000)
t=i2c.is_ready(32)
i2c.send(0,32)
t=i2c.recv(1, addr=32, timeout=5000)
print(t)
i2c.send(0xFF, 32)
t=i2c.recv(1, addr=32, timeout=5000)
print(t)