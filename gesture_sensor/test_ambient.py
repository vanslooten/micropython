from time import sleep

from machine import Pin, I2C

from apds9960.const import *
from apds9960 import uAPDS9960 as APDS9960

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)

apds = APDS9960(i2c)

print("Light Sensor Test")
print("=================")
apds.enableLightSensor()

oval = -1
while True:
    sleep(0.25)
    val = apds.readAmbientLight()
    if val != oval:
        print("AmbientLight={}".format(val))
        oval = val

