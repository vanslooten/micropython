from time import sleep

from machine import Pin, I2C

from apds9960.const import *
from apds9960 import uAPDS9960 as APDS9960

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)

apds = APDS9960(i2c)

print("Light Sensor Test")
print("=================")
apds.enableLightSensor()

old_rgb = None
while True:
    sleep(0.25)
    r = apds.readRedLight()
    g = apds.readGreenLight()
    b = apds.readBlueLight()
    # format color als rgb integer string with integer values between 0 and 255
    #r = map(r, 0, 65535, 0, 255)
    #g = map(g, 0, 65535, 0, 255)
    #b = map(b, 0, 65535, 0, 255)
    rgb = "rgb({},{},{})".format(r, g, b)
    
    if rgb != old_rgb:
        print("Color={}".format(rgb))
        old_rgb = rgb

