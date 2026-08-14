from time import sleep
from machine import Pin, I2C

from apds9960.const import *
from apds9960 import uAPDS9960 as APDS9960

I2C_ADDR = 0x39
REG_PART_ID = 0x92

led = Pin("LED", Pin.OUT)
led.toggle()
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
print("I2C Scan ...")
scan_results = i2c.scan()
print(scan_results)

for addr in scan_results:
    print(f"Device found at I2C address: {hex(addr)}")
    I2C_ADDR = addr

print(f"Using I2C address: {hex(I2C_ADDR)} to read Part ID...")

# Read 1 byte from the Part ID register (0xFF)
part_id_bytes = i2c.readfrom_mem(I2C_ADDR, REG_PART_ID, 1)
part_id = part_id_bytes[0]

apds = APDS9960(i2c)

dirs = {
    APDS9960_DIR_NONE: "none",
    APDS9960_DIR_LEFT: "left",
    APDS9960_DIR_RIGHT: "right",
    APDS9960_DIR_UP: "up",
    APDS9960_DIR_DOWN: "down",
    APDS9960_DIR_NEAR: "near",
    APDS9960_DIR_FAR: "far",
}

apds.setProximityIntLowThreshold(50)

print("Gesture Test")
print("============")
apds.enableGestureSensor()

while True:
    sleep(0.5)
    if apds.isGestureAvailable():
        motion = apds.readGesture()
        print("Gesture={}".format(dirs.get(motion, "unknown")))

