# scan for I2C devices and read the Part ID register to identify the sensor variant

from machine import Pin, I2C

i2c = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)

print("Starting I2C scan...")
scan_results = i2c.scan()
print(scan_results)

I2C_ADDR = 0x57
REG_PART_ID = 0xFF

# determine the sensor address by getting the result of the I2C scan
for addr in scan_results:
    print(f"Device found at I2C address: {hex(addr)}")
    I2C_ADDR = addr

print(f"Using I2C address: {hex(I2C_ADDR)} to read Part ID...")

# Read 1 byte from the Part ID register (0xFF)
part_id_bytes = i2c.readfrom_mem(I2C_ADDR, REG_PART_ID, 1)
part_id = part_id_bytes[0]

print(f"Part ID read: {hex(part_id)}")
