# Scan for an MPU6050 and read its WHO_AM_I register.

from machine import Pin, I2C

i2c = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)

print("Starting I2C scan...")
scan_results = i2c.scan()
print(scan_results)

MPU6050_ADDRESSES = (0x68, 0x69)
WHO_AM_I_REGISTER = 0x75
EXPECTED_WHO_AM_I = 0x68

mpu_addresses = [addr for addr in scan_results if addr in MPU6050_ADDRESSES]
if not mpu_addresses:
    print("No MPU6050 found at 0x68 or 0x69.")
else:
    for address in mpu_addresses:
        who_am_i = i2c.readfrom_mem(address, WHO_AM_I_REGISTER, 1)[0]
        print(f"MPU6050 address: {hex(address)}")
        print(f"WHO_AM_I: {hex(who_am_i)}")
        if who_am_i == EXPECTED_WHO_AM_I:
            print("MPU6050 identity confirmed.")
        else:
            print("Unexpected WHO_AM_I value; check the sensor type or wiring.")
