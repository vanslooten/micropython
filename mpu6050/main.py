from imu import MPU6050
from time import sleep
from machine import Pin, I2C

# Shows Pi is on by turning on LED when plugged in:
LED = Pin("LED", Pin.OUT)
LED.on()

# Make sure to adjust the I2C pins and frequency according to your hardware setup!
# Here we use I2C(1) with SDA on Pin GP10 and SCL on Pin GP11, and a frequency of 400kHz:
i2c = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)
imu = MPU6050(i2c)

# loop forever:
while True:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    temp=round(imu.temperature,2)
    print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",temp,"        ",end="\r")


    sleep(0.2)
